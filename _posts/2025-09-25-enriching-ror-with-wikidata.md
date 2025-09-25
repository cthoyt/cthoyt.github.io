---
layout: post
title: Suggesting new relations in ROR from Wikidata
date: 2025-09-25 17:35:00 +0200
author: Charles Tapley Hoyt
tags:
  - ROR
  - Wikidata
  - organization
  - organizations
  - bibliometrics
---

I was looking at the different NFDI consortia in the
[Research Organization Registry (ROR)](https://ror.org), and found that the only
two that have a parent relations to the
[NFDI (`ror:05qj6w324`)](https://bioregistry.io/ror:05qj6w324) are
[NFDI4DS (`ror:00bb4nn95`)](https://bioregistry.io/ror:00bb4nn95) and
[MaRDI (`ror:04ncnzm65`)](https://bioregistry.io/ror:04ncnzm65). This felt
strange to me, so I started looking around Wikidata to see if I could
automatically make a curation sheet to send along to them. I found that Wikidata
already has detailed pages for all NFDI consortia, and that they also include
relationships to the parent. This blog post is about the steps I took to write a
workflow to find relationships in Wikidata that are appropriate for submission
to ROR.

## Getting Wikidata

In Wikidata, an entity can be annotated with a ROR identifier via property
`P6782`. I wanted to write a SPARQL query for the
[Wikidata Query Service](https://query.wikidata.org/) to retrieve all triples
for which both the subject and object have and ROR identifier.

```sparql
SELECT ?subject ?subjectROR ?subjectLabel ?predicate ?object ?objectROR ?objectLabel
{
  ?subject ?predicate ?object ;
           wdt:P6782 ?subjectROR .
  ?object wdt:P6782 ?objectROR .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

While I now know this query should return about 67K rows, at the time, I ran
into the issue that it was too complicated and caused the Wikidata Query Service
to timeout. The next step in any investigation with a blasphemous
`?subject ?predicate ?object` pattern is to look into the predicates and try to
cut them down. I set to reformulating the query to count the frequency of
appearance of each predicate.

```sparql
SELECT DISTINCT ?p ?pLabel (COUNT(?p) as ?count)
{
  ?subject wdt:P6782 ?subjectROR;
           ?predicate ?object .
  ?object wdt:P6782 ?objectROR .
  ?p wikibase:directClaim ?predicate .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
GROUP BY ?p ?pLabel
ORDER BY DESC(?count)
```

This query uses the sneaky `wikibase:directClaim` to map between the `wd:`
entity namespace and `wdt:` direct property namespace so the query service could
look up the label for the link. The problem was, this query was still too heavy
and caused a timeout. Therefore, I had to simplify the query to just get the
counts without the label, then use a second query and join the data externally
(I also tried a nested query along the way, but it still timed out).

```sparql
SELECT DISTINCT ?predicate (COUNT(?predicate) as ?count)
{
  ?subject wdt:P6782 ?subjectROR ;
           ?predicate ?object .
  ?object wdt:P6782 ?objectROR .
}
GROUP BY ?predicate
ORDER BY DESC(?count)
```

With that out of the way, I tried re-writing the original query by formatting in
the 147 predicates I pulled out into the `VALUES ?predicate { ... }`
(abbreviated), like:

```sparql

SELECT ?subject ?subjectROR ?subjectLabel ?predicate ?object ?objectROR ?objectLabel
{
  VALUES ?predicate { ... }
  ?subject ?predicate ?object ;
           wdt:P6782 ?subjectROR .
  ?object wdt:P6782 ?objectROR .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

This still caused timeouts, so I resorted to a loop in Python, which also let me
simplify the query to skip the Wikidata IDs and just pull out RORs for the
subject and object (where the `{...}` gets replaced with a different property on
each):

```sparql
SELECT ?subjectROR ?objectROR
WHERE {
    ?subjectROR ^wdt:P6782/wdt:{...}/wdt:P6782 ?objectROR .
}
```

I really like this because it uses paths to reduce the need to specify the
middle entities which don't get used. I don't know if the SPARQL engine is able
to optimize on it, but it's cool. Maybe not so readable, but cool. The loop
created a super-sized TSV with the predicate and labels added back.

## Getting ROR

I've previously written a source to
[PyOBO](https://github.com/biopragmatics/pyobo) that wraps downloading and
structuring ROR's data dump into a readily usable format, so getting ROR's
triples was as easy as

```python
import pyobo

df = pyobo.get_relations_df("ror")
```

I also had to map the part of and has part relations from BFO to Wikidata
properties. I did this by hand because it was faster than doing it the
sustainable way, which would have been to pull the mappings from SSSOM-like
annotations in the BFO ontology or from Wikidata itself (since I curated those
into Wikidata years ago when we were preparing the (unpublished) relation
ontology paper).

## Putting it all together

While I'm glossing over a few steps, it was possible using the tools in PyOBO
and the Bioregistry to get data in the right shape.
