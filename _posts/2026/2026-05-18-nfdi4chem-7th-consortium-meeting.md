---
layout: post
title: NFDI4Chem 7th Consortium Meeting
date: 2026-05-18 15:51:00 +0100
author: Charles Tapley Hoyt
tags:
  - NFDI
  - NFDI4Chem
  - chemistry
---

The [7<sup>th</sup> NFDI4Chem consortium meeting](https://nfdi4chem.de/event/consortium-meeting-7-0/) took place
last week in Jena. This post is a summary of some of the interesting discussions I had there.

## Semantic Farm

The [Semantic Farm](https://semantic.farm) (previously called the Bioregistry, now adapted to be domain-agnostic)
is a registry of ontologies, controlled vocabularies, terminologies, and other resources that mint (persistent)
identifiers. While it's already been widely adopted in the biomedical domain (e.g., in the OBO Foundry, Monarch
Initiative)
since its creation in 2019, I've been working to integrate it within NFDI4Chem and other consortia via
the [NFDI Section Metadata Working Group for Ontology Harmonization and Mapping](https://github.com/nfdi-de/section-metadata-wg-onto/).
I want to highlight a few discussions I had about the Semantic Farm at the 7<sup>th</sup> NFDI4Chem consortium meeting:

### Extending Semantic Farm's Provider Data Model

I talked with Steffen Neumann () about extending the data model for providers in Semantic Farm to include information
about what media types (e.g., HTML, JSON, RDF) each provider returns and whether content negotiation is possible
(i.e., when sending an `Accept` header to tell the server what kind of media type to return).

Steffen's use case in NFDI4Chem is the Semantic Farm entry for MassBank ([https://semantic.farm/massbank](https://semantic.farm/massbank)).
Enabling Semantic Farm to resolve in different ways will support the development of computational workflows as well as make
it more useful when implementing the MassBank front-end.

### Adding Semantic Web Interoperability to Semantic Farm's Resolver

I talked with [Egon Willighagen](https://egonw.github.io) (a longtime collaborator of mine and a member of one of
the [NFDI4Chem advisory boards](https://nfdi4chem.de/the-advisory-boards/) about how to extend the "resolver"
functionality of Semantic Farm to support content negotiation. Normally, this redirects addresses constructed
with a CURIE like https://semantic.farm/GO:0032571 to the first-party (or best) web page for human reading.
Egon suggested that if a request to this endpoint contains an `Accept` header asking for `text/turtle` (or any other RDF-adjacent mimetype)
that it could return the list of related URIs. Importantly, this functionality is already available to some extent on the front-end when viewing
[https://semantic.farm/reference/GO:0032571] and via the API through [https://semantic.farm/api/reference/go:0032571].

In [biopragmatics/bioregistry#1954](https://github.com/biopragmatics/bioregistry/pull/1954), I extended the resolver so now it's possible to
use `Accept` headers like in the following:

```python
import requests

res = requests.get("https://semantic.farm/GO:0032571", headers={"Accept": "text/turtle"})
```

I also added a way of adding query parameters to get the same results when 
navigating to [https://semantic.farm/GO:0032571?format=turtle]. For both, the following is returned:

```turtle
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

<https://semantic.farm/GO:0032571> rdfs:seeAlso <http://bio2rdf.org/go:0032571>,
        <http://identifiers.org/obo.go/GO:0032571>,
        <http://purl.obolibrary.org/obo/GO_0032571>,
        <http://purl.org/obo/owl/GO#GO_0032571>,
        <http://www.geneontology.org/GO:0032571>,
        <http://www.informatics.jax.org/searches/GO.cgi?id=GO:0032571>,
        <http://www.informatics.jax.org/vocab/gene_ontology/GO:0032571>,
        <http://www.pantherdb.org/panther/category.do?categoryAcc=GO:0032571>,
        <https://bioportal.bioontology.org/ontologies/GO/?p=classes&conceptid=http://purl.obolibrary.org/obo/GO_0032571>,
        <https://identifiers.org/GO:0032571>,
        <https://n2t.net/go:0032571>,
        <https://www.ebi.ac.uk/QuickGO/GTerm?id=GO:0032571>,
        <https://www.ebi.ac.uk/QuickGO/term/GO:0032571>,
        <https://www.ebi.ac.uk/ols4/ontologies/go/terms?iri=http://purl.obolibrary.org/obo/GO_0032571>,
        <https://www.nextprot.org/term/GO:0032571> .

```

![](https://media.licdn.com/dms/image/v2/D4D22AQHqfgc54wvFUw/feedshare-shrink_1280/B4DZ4g4PxrJcAM-/0/1778668076762?e=1780531200&v=beta&t=_dakjbl7LvozLAYKTGkzGFsSQ6Wtg4wV89HLaahyUYg)

1. Discussion with Egon to improve Bioregistry / Semantic Farm lead
   to https://github.com/biopragmatics/bioregistry/pull/1954
2. Discussion with Mario WOlter in how to make a theoretical chemistry intiigy
4. Preparation of CHMO-REX-FIX-GoldBook mappings
5. discussion with Albert Engstfeld on how to incorporate ontology annotations (e.g., from CHMO) into echemdb (electro
   chemistry) LinkML to use CHMO. high relevance to pre-wor
6. Discussion of using graph machine learning with Kenichi Endo (junior prof in Stuttgart)
   and Felix
7. Discussion with Shashank Harivyasi (KIT) about plans to start sucking content out of Chemotion
8. Discussion with Nicole Jung (KIT) about converging in a data model for representing reactions in chemotion/outside
9. Discussion with Hans-Georg Weinig (h.weinig@gdch.de) on the trian home about getting some training materials from the
   German Chemical Society into DALIA.
10. Talked with Base4NFDI folks on how Semantic Farm could support existing Base services