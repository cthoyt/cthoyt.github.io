---
layout: post
title: Where do Semantic Mappings Come From?
date: 2026-01-20 11:42:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - knowledge graphs
---

The first challenge with semantic mappings is the variety of forms they can
take. This both includes different data models and serializations of those
models. This problem is effectively solved, but I think is worth reviewing for
historical purposes (please let me know if I missed something):

<img src="https://forge.extranet.logilab.fr/uploads/-/system/project/avatar/107/external-content.duckduckgo.com.jpeg" align="left" style="max-height: 3em;" alt="SKOS logo"/>
[Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference)
is a data model for RDF to represent controlled vocabularies, taxonomies,
dictionaries, thesauri, and other semantic artifacts. It defines several
semantic mapping predicates including for broad matches, narrow matches, close
matches, related matches, and exact matches.

[JSKOS (JSON for Knowledge Organization Systems)](https://gbv.github.io/jskos/#mapping),
a JSON-based extension of the SKOS data model. I recently wrote a post about
converting between [SSSOM and JSKOS]({% post_url 2026-01-15-sssom-to-jskos %}).

<img src="https://www.jean-delahousse.net/wp-content/uploads/2020/09/Owl_logo-258x300.png"  align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OWL logo">
[Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-syntax/) is primarily
used for ontologies. It has first-class language support for encoding
equivalences between classes, properties, or individuals. Other semantic
mappings can be encoded as annotation properties on classes, properties, or
individuals, e.g., using SKOS predicates.

<img src="https://obofoundry.org/images/foundrylogo.png"  align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OBO logo">
The
[OBO Flat File Format](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html)
is a simplified version of OWL with macros most useful for curating biomedical
ontologies. It has the same abilities as OWL, but also the `xref` macro which
corresponds to `oboInOwl:hasDbXref` relations, which are by nature imprecise and
therefore used in a variety of ways.

<img src="https://avatars.githubusercontent.com/u/77892844?v=4" align="left" style="max-height: 3em; margin-right: 0.5em;" alt="SSSOM logo">
The
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
is a fit-for-purpose format for semantic mappings between classes, properties,
or individuals. SSSOM guides curators towards inputting key metadata that are
typically missing from other formalisms and is gaining wider community adoption.
Importantly, SSSOM integrates into ontology curation workflows, especially for
[Ontology Development Kit (ODK)](https://incatools.github.io/ontology-development-kit)
users.

The
[Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
lives in a similar space to SSSOM, but IMO was much less approachable (c.f.
XML + Java), and has not seen a lot of traction in the biomedical space.

<img src="https://ontoportal.org/images/logo.png" align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OntoPortal logo"/>
[OntoPortal](https://ontoportal.org/) has its own data model for semantic
mappings that has low metadata precision. I recently wrote a post on converting
[OntoPortal to SSSOM]({% post_url 2025-11-23-sssom-from-bioportal %}). OntoPortal would also like
to invest more in SSSOM infrastructure if it can organize funding and human resources.

<img src="https://upload.wikimedia.org/wikipedia/commons/6/66/Wikidata-logo-en.svg" align="left" style="max-height: 3em" alt="Wikidata logo">
[Wikidata](https://www.wikidata.org) has its own data model for semantic
mappings that include higher precision metadata. I recently wrote a post on
mapping between the data models from [SSSOM and
Wikidata]({% post_url 2026-01-07-sssom-to-wikidata %}).

Finally, there's a long tail of mappings that live in poorly annotated CSV, TSV,
Excel, and other formats. Similarly, mappings can live in plain RDF files, e.g.,
encoded with SKOS predicates, but without high precision metadata.
