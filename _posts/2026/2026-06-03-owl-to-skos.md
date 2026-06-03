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

The data model in [PyOBO](https://github.com/biopragmatics/pyobo) closely
resembles the Web Ontology Language (OWL) and macros in the
[OBO Flat File format](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html).
However, some communities prefer the simplified nature of the SKOS data model
compared to the highly precise (and sometimes burdensome) nature of OWL
semantics. This post describes the workflow I implemented to
[downscale OWL to SKOS](https://github.com/biopragmatics/pyobo/pull/509).

Before diving into this, I searched for previous work in mapping OWL to SKOS and
was surprised to find only a few things (and they're all old):

- [Exploring the Relationships between OWL and SKOS](https://www.cs.man.ac.uk/~stevensr/papers/iswc2009DC.pdf)
  by Nor Azlinayati Abdul Manaf (2009)
- [Using OWL and SKOS](https://www.w3.org/2006/07/SWD/SKOS/skos-and-owl/master.html)
  by Sean Bechhofer and Alstair Miles (2008)
- [SKOS2OWL](https://www.heppnetz.de/projects/skos2owl/) by Hepp _et al._ (2007)

## Predicate Mappings

However, I didn't find these resources very helpful, so I just jumped right into
an implementation. First, I mapped several predicates used in OWL to predicates
used in SKOS:

- `rdfs:label` maps to `skos:prefLabel`
- synonym predicates from OBO-flavored OWL (`oboInOwl:hasExactSynonym`,
  `oboInOwl:hasNarrowSynonym`, `oboInOwl:hasBroadSynonym`) are squashed to
  `skos:altLabel`, and synonym type information is thrown away
- `dcterms:description` maps to `skos:scopeNote`
- `rdf:subClassOf` and `rdf:type` are squashed to `skos:broadMatch`
- similarly, individuals (`owl:NamedIndividual`) and classes (`owl:Class`) are
  both squashed to `skos:Concept`
- predicates and relationships are omitted
- root terms annotated on the ontology with `IAO:0000700` (ontology has root
  term) get annotated on the SKOS concept scheme with `skos:hasTopConcept`

## Hierarchical Reasoning

I introduced
[`OMO:0003014` (has ontology hierarchical property)](https://semantic.farm/OMO:0003014)
in
[information-artifact-ontology/ontology-metadata#193](https://github.com/information-artifact-ontology/ontology-metadata/pull/193)
to enable ontologies to explicitly annotate which predicates should be used
during hierarchical browsing (in addition to `rdf:subClassOf`). For example, the
[Uber Anatomy Ontology (UBERON)](https://semantic.farm/uberon) contains a
partonomy of anatomical features, and should therefore be browsable based on the
[`BFO:0000050` (part of)](https://semantic.farm/BFO:0000050) relationship. This
annotation was originally inspired by the custom configuration for adding new
ontologies to the EBI's
[Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/) - now, the
configuration for the OLS can be upstreamed into the ontologies themselves and
be made more reusable.

Accordingly, I used hierarchical properties annotated on to the ontology with
`OMO:0003014` to translate object property constraints into broad matches.
Inside PyOBO, I updated the source for the
[Research Organization Registry (ROR)](https://ror.org/) to explicitly annotate
[`org:subOrganizationOf`](https://semantic.farm/org:subOrganizationOf) as a
hierarchical property. Below, the entry for the French
[Techniques of Informatics and Microelectronics for Integrated Systems Architecture](https://ror.org/000063q30)
shows the translation into broad matches for both the subclass relation to the
_ad hoc_ term for a facility and the sub-organization relations to its four
parent organizations:

```ttl
ror:000063q30 a skos:Concept ;
    skos:altLabel "TIMA",
        "TIMA Laboratory",
        "Techniques de l'Informatique et de la Microélectronique pour l'Architecture des Systèmes Intégrés"@fr ;
    skos:broadMatch <http://purl.obolibrary.org/obo/ror#facility>,
        ror:02feahw73,
        ror:02rx3b187,
        ror:04z22qz54,
        ror:05sbt2524 ;
    skos:prefLabel "Techniques of Informatics and Microelectronics for Integrated Systems Architecture" ;
    skos:scopeNote "a facility in Grenoble established in 2003" .
```

## Inverse Hierarchical Reasoning

I extended this notion further to leverage inverse predicate information for the
hierarchical property annotations. If the inverse of a hierarchical property is
used in an object property constraint (or annotation property), then it is
translated into a narrow match.

For example, in FamPlex, complexes are annotated with the
[`RO:0002351` (has member)](https://semantic.farm/RO:0002351) relationship to
genes. This algorithm looks up the inverse relationship
[ `RO:0002350` (is member of)](https://semantic.farm/RO:0002350) and annotates
that as a complex has narrow match to gene triple, and simultaneously, gene has
broad match to complex triple.

```ttl
fplx:Sarcoglycan_complex a skos:Concept ;
    skos:broadMatch fplx:DGC ;
    skos:inScheme <https://w3id.org/biopragmatics/resources/fplx/fplx.ttl> ;
    skos:narrowMatch hgnc:10805,
        hgnc:10806,
        hgnc:10807,
        hgnc:10808,
        hgnc:14075 ;
    skos:prefLabel "Sarcoglycan_complex" ;
    skos:scopeNote "A family of transmembrane dystrophin-associated proteins that play a role in the membrane association of the DYSTROPHIN-ASSOCIATED PROTEIN COMPLEX." .
```

## Encoding Institutional Knowledge in Code while Translating Databases into Ontologies

We have the goal in NFDI4Chem to map from ontology terms in the Chemical Methods
Ontology (CHMO) to the [IUPAC GoldBook](https://goldbook.iupac.org), a
compendium of chemical terminology which also covers instrumentation and
experimental techniques.

While GoldBook's data is now available in both JSON and XML, neither ascribe
semantics to their fields, i.e., the XML doesn't use namespaces and the JSON
doesn't have a _linked data_ component. This meant that as I implemented a PyOBO
source for GoldBook in
[biopragmatics/pyobo#436](https://github.com/biopragmatics/pyobo/pull/436), I
had to interpret what each field means, and ascribe semantics to them by
assigning existing, well-known predicates to each.

However, based on
[discussions](https://github.com/NFDI4Chem/Ontologies4Chem2026/discussions/7) in
preparation for the 6<sup>th</sup> Ontologies4Chem workshop later this year, it
appears IUPAC does not want to make ontological commitments for its entities,
and would instead prefer to produce a SKOS vocabulary.

My work on ontologizing GoldBook was done without discussion with IUPAC, similar
to most PyOBO sources. Personally, I think it's much more valuable to ascribe
precise semantics. I am less dogmatic about ontological commitments and have
usually focused on what makes a data resource useful for me. In this case, it
was being able to access GoldBook through an ontology-like interface such that
it could be loaded in SSSOM Curator to
[lexically predict then manually curate CHMO-GoldBook mappings](https://github.com/biopragmatics/biomappings/pull/240).

However, now with the SKOS exporter described earlier in this post, I can have
it both ways: first starting with a more precise OWL artifact, then downscaling
to a simpler SKOS artifact with entries that look like:

```ttl
goldbook:08003 a skos:Concept ;
    skos:inScheme <https://w3id.org/biopragmatics/resources/goldbook/goldbook.ttl> ;
    skos:prefLabel "analytical chemistry" ;
    skos:scopeNote "Scientific discipline that develops and applies strategies, instruments, and procedures to obtain information on the composition and nature of matter in space and time." .
```

---

There are still a few parts of SKOS that I'm not familiar with, so I expect that
this translation will evolve over time. For example, because SKOS is so tightly
tied to RDF as a serialization, it has better support for language tags. OWL can
be serialized in RDF, but the OBO Flat File Format is inherently limited in its
ability to express language. I'm interested to overcome these limits in the
PyOBO implementation.
