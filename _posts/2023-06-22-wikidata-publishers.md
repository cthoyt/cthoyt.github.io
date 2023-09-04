---
layout: post
title: Querying Journals and Publishers in Wikidata
date: 2023-06-22 19:00:23 +0200
author: Charles Tapley Hoyt
tags: wikidata bibliometrics
---

Today's short post is about three SPARQL queries I wrote to get bibliometric information
about journals and publishers out of Wikidata.

Each of the following queries can be readily copy-pasted into the
[Wikidata Query Service](https://query.wikidata.org/) and run in the browser.

## Journals

The following SPARQL query gets information about journals:

```sparql
SELECT ?journal ?journalLabel (GROUP_CONCAT(?issn) as ?issns)
WHERE 
{
  ?journal wdt:P31 wd:Q5633421 ;
           wdt:P236 ?issn .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}
GROUP BY ?journal ?journalLabel
```

Follow [this link](https://w.wiki/6ryy) to populate the Wikidata Query Service with this query. 
Note that this query takes a while to run and may time out since there are on the scale of 100K
journals.

Journals might have multiple [International Standard Serial Numbers (ISSNs)](https://bioregistry.io/registry/issn)
because a different one is assigned to the print and electronic versions of the journal, among other things.

Get the ISSN-L (the normalized/preferred) ISSN for each:

```sparql
SELECT ?journal ?journalLabel ?issn
WHERE 
{
  ?journal wdt:P31 wd:Q5633421 .
  OPTIONAL { ?journal wdt:P7363 ?issnl }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}
```

Get a forward mapping from all ISSNs to ISSN-L. Note that these have been filtered to scientific journals (wd:Q5633421)


```sparql
SELECT ?issn ?issnl
WHERE 
{
  ?journal wdt:P31 wd:Q5633421 ;
           wdt:P7363 ?issnl ;
           wdt:P236 ?issn .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}
```

## Publishers

The following SPARQL query gets information about publishers:

```sparql
SELECT DISTINCT ?publisher ?publisherLabel ?ror ?grid ?isni
WHERE 
{
  ?publisher wdt:P31/wdt:P279+ wd:Q2085381 ;
             rdfs:label ?publisherLabel .
  FILTER ( LANG(?publisherLabel) = "en" )
  OPTIONAL { ?publisher wdt:P6782 ?ror }
  OPTIONAL { ?publisher wdt:P2427 ?grid }
  OPTIONAL { ?publisher wdt:P213 ?isni }
}
```

Follow [this link](https://w.wiki/6ry$) to populate the Wikidata Query Service with this query. 
This query returns the [Research Organization Registry (ROR)](https://bioregistry.io/registry/ror)
identifier when available. This registry effectively subsumes the
[Global Research Identifier Database (GRID)](https://bioregistry.io/registry/grid), which has since
been shut down, but this might be helpful for integrating data that hasn't been updated.
The [International Standard Name Identifier (ISNI)](https://bioregistry.io/registry/isni) is also
included when available. Wikidata has several other nomenclature authorities such as
[GND](https://bioregistry.io/registry/gnd), [VIAF](https://bioregistry.io/registry/viaf), RingGold,
and others that are omitted for brevity (each has their own corresponding Wikidata property.).

Later, I could consider adding a clause to make sure there's a "scientific journal"
in the publisher to remove some irrelevant records.

## Connections between Journals and Publishers

Finally, the [publisher (P123)](https://bioregistry.io/wikidata:P123) relation can be used to
identify the relationships between journals and their respective publishers.

```sparql
SELECT DISTINCT ?journal ?journalLabel ?publisher ?publisherLabel
WHERE 
{
  ?journal wdt:P31 wd:Q5633421 ;
           rdfs:label ?journalLabel ;
           wdt:P123 ?publisher .
  FILTER ( LANG(?journalLabel) = "en" ) 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". } # Helps get the label in your language, if not, then en language
}
ORDER BY ?journalLabel
```

Follow [this link](https://w.wiki/6rz5) to populate the Wikidata Query Service with this query. 

Rather than using the Wikidata label service for the journal label, I more explicitly wrote it out
to ensure that there is an english label, and to remove anything without an english label.
