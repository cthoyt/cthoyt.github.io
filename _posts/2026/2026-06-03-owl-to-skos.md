---
layout: post
title: A practical approach to translate OWL to SKOS
date: 2026-06-03 12:11:00 +0200
author: Charles Tapley Hoyt
tags:
  - OWL
  - SKOS
  - PyOBO
---

PyOBO's data model closely resembles the highly expressive data model of Web Ontology
Language (OWL). In contrast, the SKOS data model is much simpler than OWL, shedding the
ability relationships between entities besides a loose hierarchy of broader and narrower
relations.

Some communities prefer SKOS because of its simplicity and lack of need for more
explicit and/or precise semantics.

While I found some `notes
<https://www.w3.org/2006/07/SWD/SKOS/skos-and-owl/master.html>`_ from W3 on the
relationship between SKOS and OWL, I surprisingly wasn't easily able to find something
official-looking on how to downscale OWL to SKOS.

Therefore, I implemented my own mapping in PyOBO:

- ``rdfs:label`` becomes ``skos:prefLabel``
- all synonym predicates (``oboInOwl:hasExactSynonym``, ``oboInOwl:hasNarrowSynonym``,
  ``oboInOwl:hasBroadSynonym``) squashed to ``skos:altLabel`` and synonym type
  information is thrown away
- ``dcterms:description`` becomes ``skos:scopeNote``
- ``rdf:subClassOf`` and ``rdf:type`` are squashed to ``skos:broadMatch``
- similarly, individuals and classes are both squashed to ``skos:Concept``
- predicates aren't translated into SKOS
- root terms annotated on the ontology with ``IAO:0000700`` get annotated on the SKOS concept scheme with ``skos:hasTopConcept``

I also did some non-trivial transformations based on the ``OMO:0003014``
"has ontology hierarchical property" that I introduced in
https://github.com/information-artifact-ontology/ontology-metadata/pull/193, which
allows ontologies to explicitly specify what are the hierarchical properties used
(in addition to ``rdf:subClassOf``). This annotation was originally inspired by the
need for the EBI's Ontology Lookup Service (OLS) to annotate this information in its
custom configuration - now it can be made explicit in the ontology itself. For example,
Uberon is a partonomy, meaning that the _part of_ relationship is used for hierarchical
browsing. In my SKOS conversion, the relations annotated this way are also translated into
broad matches.

2. show ROR as an example which uses the subOrganizationOf relationship


I extended this notion one step further to reason over the inverse of the hierarchical
relations, and annotate any object or annotation properties using that inverse predicate
with a narrow match. For example, in FamPlex, complexes are annotated with the _has member_
relationship to genes. This algorithm looks up the inverse relationship _is member of_ and
annotates that as a complex has narrow match to gene triple, and simultaneously,
gene has broad match to complex triple. 



Interestingly, SKOS has better support for language tags because it is so closely
defined based on RDF as a serialization (whereas OWL can be serialized in RDF, but OBO
does not have many of the language support ideas that are inherent to RDF things)