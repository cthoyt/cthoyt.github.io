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
`P6782`. I wanted to write a SPARQL query for the to retrieve all triples for
which both the subject and object have and ROR identifier.

```sparql
SELECT ?subject ?subjectROR ?subjectLabel ?predicate ?object ?objectROR ?objectLabel
{
  ?subject ?predicate ?object ;
           wdt:P6782 ?subjectROR .
  ?object wdt:P6782 ?objectROR .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

In the first version of this post, I ran the SPARQL queries against first-party
[Wikidata Query Service (WQS)](https://query.wikidata.org/) (permalink to this
query at [https://w.wiki/FUVA](https://w.wiki/FUVA)) and ran into timeout
issues. This motivated the following section of this post on the exploration of
the underlying triples and alternate query formulations below.

However, both Egon ([here](https://mastodon.social/@egonw/115281836981009390))
and Tiago
([here](https://github.com/cthoyt/cthoyt.github.io/issues/78#issuecomment-3345745218))
suggested I also try the University of Freiburg's QLever mirror of Wikidata
available at
[https://qlever.cs.uni-freiburg.de/wikidata](https://qlever.cs.uni-freiburg.de/wikidata)
(permalink to this query at
[https://qlever.cs.uni-freiburg.de/wikidata/Vz75fY](https://qlever.cs.uni-freiburg.de/wikidata/Vz75fY?exec=true)).

QLever is blazingly fast and returns about 67K rows in only a few seconds. That
all being said, I retained my exploration below for posterity.

## Working around timeouts on the WQS

The next step in any investigation with a blasphemous
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

The workflow I implemented for this lives in
[https://github.com/cthoyt/ror-wikidata-enrichment](https://github.com/cthoyt/ror-wikidata-enrichment).
The data from Wikidata is in
[this file](https://github.com/cthoyt/ror-wikidata-enrichment/blob/main/data/3-wikidata-ror-relations.tsv),
licensed under CC0.

Do you want this workflow to better reflect your organization? Check out my
other blog post on [how to curate data about your research organization]({% post_url 2021-01-17-organization-organization %})

## Getting ROR

I've previously implemented a source in
[PyOBO](https://github.com/biopragmatics/pyobo) that wraps downloading and
structuring ROR's data dump into a readily usable format, so getting ROR's
triples was as easy as:

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

I made an intermediate output of all of thet triples
[here](https://github.com/cthoyt/ror-wikidata-enrichment/raw/refs/heads/main/data/4-ror-relations.tsv),
licensed under CC0.

## Putting it all together

While I'm glossing over a few steps that you can grok by reading
[my python script](https://github.com/cthoyt/ror-wikidata-enrichment/blob/main/main.py),
it was possible to finish getting the data in the right shape to compare with
tools in PyOBO and
[the Bioregistry](https://github.com/biopragmatics/bioregistry.)

The final step was to take the difference between the Wikidata triples and the
ROR triples, filter for triples that make sense within the ROR schema (which for
now is just part of and has part relationships), and then dump the results out.
There were around 67K records before filtering around 2.8K after filtering. Here
are a few examples:

| subjectROR | subjectLabel                                           | predicate | predicateLabel | objectROR | objectLabel                 |
| ---------- | ------------------------------------------------------ | --------- | -------------- | --------- | --------------------------- |
| 00k4nrj32  | Essex County Hospital                                  | P361      | part of        | 02wnqcb97 | National Health Service     |
| 022efad20  | University of Gabès                                    | P527      | has part(s)    | 01hwc7828 | Institut des Régions Arides |
| 04p4gjp18  | Center of Excellence on Hazardous Substance Management | P361      | part of        | 028wp3y58 | Chulalongkorn University    |
| 04tnv7w23  | École Supérieure Polytechnique d'Antsiranana           | P361      | part of        | 00pd4qq98 | Université d’Antsiranana    |
| 02f4ya153  | Barro Colorado Island                                  | P361      | part of        | 01pp8nd67 | Smithsonian Institution     |

## Coda

The point of all of this was to automate adding the missing NFDI consortia
relationships to the parent NFDI organization in ROR, because I'm interested in
creating queries over the organization landscape related to NFDI to support an
upcoming section on Internationalization. And like most things in my work life,
I ended up cleaning some data and making upstream contributions along the way.
Let's see how receptive ROR is to this! The triples are all
[here](https://github.com/cthoyt/ror-wikidata-enrichment/blob/main/data/6-diff-suggestions.tsv)
and I can easily make them a different format for submission.

---

Caveat: if you look into the data, you might notice that some of the entities
don't have labels. I realized this is happening because I haven't updated my
PyOBO importer to get the 2.0 data dump from ROR, and I'm stuck on old version
1.36. This can be fixed independently of this workflow. Here's the rows related
to the NFDI consortia that need new relations, which are all missing labels
until I fix this.

| subjectROR | subjectLabel | predicate | predicateLabel | objectROR | objectLabel                            |
| ---------- | ------------ | --------- | -------------- | --------- | -------------------------------------- |
| 00enhv193  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 02cxb1m07  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 03xrvbe74  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 020tty630  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 04ncnzm65  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01f5dqg10  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 001jhv750  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 0310v3480  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01d2qgg03  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01k9z4a50  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 03a4sp974  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 05wwzbv21  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 0305k8y39  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 0238fds33  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 03f6sdf65  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 0033j3009  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01vnkaz16  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01v7r4v08  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 04dy2xw62  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 01xptp363  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 034pbpe12  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 05nfk7108  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 00r0qs524  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 00bb4nn95  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
| 03fqpzb44  |              | P361      | part of        | 05qj6w324 | Nationale Forschungsdateninfrastruktur |
