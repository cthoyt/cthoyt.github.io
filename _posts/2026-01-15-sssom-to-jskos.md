---
layout: post
title: Mapping from SSSOM to JSKOS
date: 2026-01-15 11:42:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - SKOS
  - semantic mappings
  - mappings
  - interoperability
  - JSKOS
---

## Background on JSKOS

[JSKOS (JSON for Knowledge Organization Systems)](https://gbv.github.io/jskos/) is a JSON-based data model for
representing
terminologies, thesauri, classifications, and other semantic artifacts. It implements the
Simple Knowledge Organization System (SKOS) data model and extends it with a data model
inspired by Wikidata with the following types:

![](https://gbv.github.io/jskos/types.svg)

JSKOS enables representing semantic mappings two ways:

1. using the `narrower`, `broader`, and `related` slots in the [Concept](https://gbv.github.io/jskos/#concept) class
   that correspond to SKOS relations `skos:narrowMatch`, `skos:broadMatch`, and `skos:relatedMatch`
2. using the `mappings` slot in the [Concept](https://gbv.github.io/jskos/#concept) class, which accepts a list of more
   generic [`Mapping`](https://gbv.github.io/jskos/#mapping) objects

Here's how JSKOS represents an exact match from the [Biomappings](https://github.com/biopragmatics/biomappings)
community curated mappings database between a [Medical Subject Headings (MeSH)](https://semantic.farm/mesh) term and
[Chemical Entities of Biological Interest (ChEBI) ontology](https://semantic.farm/chebi) term for the chemical [ammeline](https://en.wikipedia.org/wiki/Ammeline):

```json
{
  "license": [
    {
      "uri": "https://spdx.org/licenses/CC0-1.0"
    }
  ],
  "uri": "https://w3id.org/biopragmatics/biomappings/sssom/biomappings.sssom.tsv",
  "mappings": [
    {
      "type": [
        "http://www.w3.org/2004/02/skos/core#exactMatch"
      ],
      "subject_bundle": {
        "member_set": [
          {
            "uri": "http://id.nlm.nih.gov/mesh/C000089"
          }
        ]
      },
      "object_bundle": {
        "member_set": [
          {
            "uri": "http://purl.obolibrary.org/obo/CHEBI_28646"
          }
        ]
      },
      "justification": "https://w3id.org/semapv/vocab/ManualMappingCuration"
    }
  ]
}
```

## Interoperability between SSSOM and JSKOS


- Added wrapper around sssom-js in https://github.com/cthoyt/sssom-pydantic/pull/26

## Motivation for SSSOM-JSKOS interoperability

- NFDI has the JSKOS stack, such as [Cocoda](https://coli-conc.gbv.de/cocoda/)
- https://gbv.github.io/jskos/#mapping
-

## Results / TODO

- Worked on JSKOS package in github.com/cthoyt/jskos, reuse text from there