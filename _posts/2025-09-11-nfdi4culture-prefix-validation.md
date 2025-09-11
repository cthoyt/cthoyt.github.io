---
layout: post
title:
  Exploring an unfamiliar SPARQL endpoint with the Bioregistry - a case study
  from NFDI4Culture
date: 2025-09-11 12:26:00 +0200
author: Charles Tapley Hoyt
tags:
  - NFDI
  - SPARQL
  - Bioregistry
---

Yesterday evening at sixth NFDI4Chem consortium meeting,
[Torsten Schrade](https://www.adwmainz.de/personen/mitarbeiterinnen/profil/torsten-schrade.html)
(from NFDI4Culture) gave a lovely and whimsical talk entitled _A Data
Alchemist's Journey through NFDI_ which explored ways that we might federate and
jointly query both consortia's knowledge.

I'll follow up with a post on that, but this pos

https://github.com/biopragmatics/bioregistry/pull/1691

how did i implement this?

1. note that this doesn't work for all triple stores, just Virtuoso ones because
   of the way that it has a special page for showing the prefix map.
   Unfortunately, I couldn't figure out if there were a programmatic way to get
   this (e.g., with content negotiation), so it requires doing some HTML
   parsing.
2. Reuse the generic stuff I mentioned in last post that validates any old
   prefix map

```console
$ bioregistry validate virtuoso https://nfdi4culture.de/sparql --tablefmt github
```

| prefix    | uri_prefix                                            | issue                     | solution                                                          |
| --------- | ----------------------------------------------------- | ------------------------- | ----------------------------------------------------------------- |
| as        | https://www.w3.org/ns/activitystreams#                | unknown CURIE prefix      | Switch to CURIE prefix ac, inferred from URI prefix               |
| bif       | http://www.openlinksw.com/schemas/bif#                | unknown CURIE prefix      |                                                                   |
| dawgt     | http://www.w3.org/2001/sw/DataAccess/tests/test-dawg# | unknown CURIE prefix      |                                                                   |
| dbpprop   | http://dbpedia.org/property/                          | unknown CURIE prefix      | Switch to CURIE prefix dbpedia.property, inferred from URI prefix |
| fn        | http://www.w3.org/2005/xpath-functions/#              | unknown CURIE prefix      |                                                                   |
| formats   | http://www.w3.org/ns/formats/                         | unknown CURIE prefix      |                                                                   |
| gqi       | http://www.openlinksw.com/schemas/graphql/intro#      | unknown CURIE prefix      |                                                                   |
| gql       | http://www.openlinksw.com/schemas/graphql#            | unknown CURIE prefix      |                                                                   |
| gr        | http://purl.org/goodrelations/v1#                     | unknown CURIE prefix      |                                                                   |
| ldp       | http://www.w3.org/ns/ldp#                             | unknown CURIE prefix      |                                                                   |
| math      | http://www.w3.org/2000/10/swap/math#                  | unknown CURIE prefix      |                                                                   |
| nci       | http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#   | non-standard CURIE prefix | Switch to standard prefix: ncit                                   |
| ogc       | http://www.opengis.net/                               | unknown CURIE prefix      |                                                                   |
| ogcgml    | http://www.opengis.net/ont/gml#                       | unknown CURIE prefix      |                                                                   |
| ogcgs     | http://www.opengis.net/ont/geosparql#                 | unknown CURIE prefix      |                                                                   |
| ogcgsf    | http://www.opengis.net/def/function/geosparql/        | unknown CURIE prefix      |                                                                   |
| ogcgsr    | http://www.opengis.net/def/rule/geosparql/            | unknown CURIE prefix      |                                                                   |
| ogcsf     | http://www.opengis.net/ont/sf#                        | unknown CURIE prefix      |                                                                   |
| product   | http://www.buy.com/rss/module/productV2/              | unknown CURIE prefix      |                                                                   |
| protseq   | http://purl.org/science/protein/bysequence/           | unknown CURIE prefix      |                                                                   |
| rdfdf     | http://www.openlinksw.com/virtrdf-data-formats#       | unknown CURIE prefix      |                                                                   |
| sc        | http://purl.org/science/owl/sciencecommons/           | unknown CURIE prefix      |                                                                   |
| scovo     | http://purl.org/NET/scovo#                            | unknown CURIE prefix      |                                                                   |
| sd        | http://www.w3.org/ns/sparql-service-description#      | unknown CURIE prefix      |                                                                   |
| sioc      | http://rdfs.org/sioc/ns#                              | unknown CURIE prefix      | Switch to CURIE prefix sioc.core, inferred from URI prefix        |
| sql       | http://www.openlinksw.com/schemas/sql#                | unknown CURIE prefix      |                                                                   |
| stat      | http://www.w3.org/ns/posix/stat#                      | unknown CURIE prefix      |                                                                   |
| vcard2006 | http://www.w3.org/2006/vcard/ns#                      | unknown CURIE prefix      | Switch to CURIE prefix vcard, inferred from URI prefix            |
| virtcxml  | http://www.openlinksw.com/schemas/virtcxml#           | unknown CURIE prefix      |                                                                   |
| virtrdf   | http://www.openlinksw.com/schemas/virtrdf#            | unknown CURIE prefix      |                                                                   |
| xf        | http://www.w3.org/2004/07/xpath-functions             | unknown CURIE prefix      |                                                                   |
| xsl10     | http://www.w3.org/XSL/Transform/1.0                   | unknown CURIE prefix      |                                                                   |
| xsl1999   | http://www.w3.org/1999/XSL/Transform                  | unknown CURIE prefix      |                                                                   |
| xslwd     | http://www.w3.org/TR/WD-xsl                           | unknown CURIE prefix      |                                                                   |
| yago      | http://dbpedia.org/class/yago/                        | unknown CURIE prefix      |                                                                   |

follow-ups:

1. this gives a whole set of related prefixes from OpenGIS, which is related to
   physical location
