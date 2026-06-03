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
was surprised to find only a few things:

- [Exploring the Relationships between OWL and SKOS](https://www.cs.man.ac.uk/~stevensr/papers/iswc2009DC.pdf)
  by Nor Azlinayati Abdul Manaf (2009)
- [Using OWL and SKOS](https://www.w3.org/2006/07/SWD/SKOS/skos-and-owl/master.html)
  by Sean Bechhofer and Alstair Miles (2008)
- [SKOS2OWL](https://www.heppnetz.de/projects/skos2owl/)

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
Uber Anatomy Ontology (UBERON) contains a partonomy of anatomical features, and
should therefore be browsable based on the
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

The effort to encode databases into ontologies has two main parts:

1. Automate downloading and parsing the source data, whether from TSV, Excel,
   relational databases, JSON, or any other format
2. Interpret what each field is supposed to be, and ascribe well-defined
   semantics
3. Enable access through a common data model

We have the goal in NFDI4Chem to map from ontology terms in the Chemical Methods
Ontology (CHMO) to the [IUPAC GoldBook](https://goldbook.iupac.org), a
compendium of chemical terminology which also covers instrumentation and
experimental techniques. However, IUPAC has a custom (and poorly-described) data
model.

<details>
<summary>See Example IUPAC GoldBook JSON</summary>

This is the JSON for [`goldbook:08003`](https://semantic.farm/08003).

```json
{
  "term": {
    "id": "08003",
    "title": "analytical chemistry",
    "longtitle": "IUPAC Gold Book - analytical chemistry",
    "doi": "10.1351\/goldbook.08003",
    "code": "08003",
    "status": "current",
    "definitions": [
      {
        "id": 1,
        "text": "Scientific discipline that develops and applies strategies, instruments, and procedures to obtain information on the composition and nature of matter in space and time.",
        "notes": {
          "1": "The definition was coined by the Working Party on Analytical Chemistry (WPAC) of the Federation of European Chemical Societies (FECS) and is known as the \"Edinburgh Definition\".",
          "2": "The term \"analytical science\" was coined in 1998 to emphasize the impact of informatics on analytical chemistry."
        },
        "links": [
          {
            "term": "chemical analysis",
            "url": "https:\/\/goldbook.iupac.org\/\/terms\/view\/08004"
          }
        ],
        "sources": [
          "PAC, 2021, 93, 997. 'Metrological and quality concepts in analytical chemistry (IUPAC Recommendations 2021)' on page 999 (https:\/\/doi.org\/10.1515\/pac-2019-0819)"
        ]
      }
    ],
    "altoutputs": {
      "html": "https:\/\/goldbook.iupac.org\/terms\/view\/08003\/html",
      "xml": "https:\/\/goldbook.iupac.org\/terms\/view\/08003\/xml",
      "plain": "https:\/\/goldbook.iupac.org\/terms\/view\/08003\/plain"
    },
    "citation": "Citation: 'analytical chemistry' in IUPAC Compendium of Chemical Terminology, 5th ed. International Union of Pure and Applied Chemistry; 2025. Online version 5.0.0, 2025. 10.1351\/goldbook.08003",
    "license": "The IUPAC Gold Book is licensed under Creative Commons Attribution-ShareAlike CC BY-SA 4.0 International (https:\/\/creativecommons.org\/licenses\/by-sa\/4.0\/) for individual terms.",
    "collection": "If you are interested in licensing the Gold Book for commercial use, please contact the IUPAC Executive Director at executivedirector@iupac.org .",
    "disclaimer": "The International Union of Pure and Applied Chemistry (IUPAC) is continuously reviewing and, where needed, updating terms in the Compendium of Chemical Terminology (the IUPAC Gold Book). Users of these terms are encouraged to include the version of a term with its use and to check regularly for updates to term definitions that you are using.",
    "accessed": "2025-09-11T08:12:32+00:00"
  }
}
```

</details>

https://github.com/biopragmatics/pyobo/pull/436

It is not about turning the Goldbook into an ontology, since this would entail
making ontological commitments IUPAC doesn't want to make. So a SKOS vocabulary
is the intended goal.

---

There are still a few parts of SKOS that I'm not familiar with, so I expect that
this translation

Interestingly, SKOS has better support for language tags because it is so
closely defined based on RDF as a serialization (whereas OWL can be serialized
in RDF, but OBO does not have many of the language support ideas that are
inherent to RDF things)
