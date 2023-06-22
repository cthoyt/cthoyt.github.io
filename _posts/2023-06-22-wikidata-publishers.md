---
layout: post
title: Querying Journals and Publishers in Wikidata
date: 2023-06-22 19:00:23 +0200
author: Charles Tapley Hoyt
tags: wikidata bibliometrics
---

Today's short post is about three SPARQL queries I wrote to get bibliometric information
about journals and publishers out of Wikidata.

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

Journals might have multiple [International Standard Serial Numbes (ISSNs)](https://bioregistry.io/registry/issn)
because a different one is assigned to the print and electronic versions of the journal, among other things.

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

Could consider adding a clause to make sure there's a "scientific journal" in the publisher to remove some irrelevant
stuff

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

Rather than using the Wikidata label service for the journal label, I more explicitly wrote it out
to ensure that there is an english label, and to remove anything without an english label.
