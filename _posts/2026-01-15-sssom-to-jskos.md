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

[JSKOS (JSON for Knowledge Organization Systems)](https://gbv.github.io/jskos/)
is a JSON-based data model for representing terminologies, thesauri,
classifications, and other semantic artifacts. It implements the Simple
Knowledge Organization System (SKOS) data model and extends it with a data model
inspired by Wikidata with the following types:

![](https://gbv.github.io/jskos/types.svg)

JSKOS enables representing semantic mappings two ways:

1. using the `narrower`, `broader`, and `related` slots in the
   [Concept](https://gbv.github.io/jskos/#concept) class that correspond to SKOS
   relations `skos:narrowMatch`, `skos:broadMatch`, and `skos:relatedMatch`
2. using the `mappings` slot in the
   [Concept](https://gbv.github.io/jskos/#concept) class, which accepts a list
   of instances of the more generic
   [Mapping](https://gbv.github.io/jskos/#mapping) class

Here's how JSKOS represents an exact match from the
[Biomappings](https://github.com/biopragmatics/biomappings) community curated
mappings database between a
[Medical Subject Headings (MeSH)](https://semantic.farm/mesh) term and
[Chemical Entities of Biological Interest (ChEBI) ontology](https://semantic.farm/chebi)
term for the chemical [ammeline](https://en.wikipedia.org/wiki/Ammeline):

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
      "type": ["http://www.w3.org/2004/02/skos/core#exactMatch"],
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

Given the overlapping ability of the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
and JSKOS to represent semantic mappings, the JSKOS and SSSOM teams developed a
[crosswalk](https://github.com/gbv/jskos/issues/108) between JSKOS and SSSOM.
Along the way, the SSSOM and JSKOS data models evolved to incorporate good ideas
from the other, for example, the addition of a
[mapping identifier](https://github.com/mapping-commons/sssom/issues/359) to
SSSOM records to allow for referencing the SSSOM mapping itself.

The crosswalk is not (yet) lossless, for example, JSKOS does not yet have a
mechanism to express
[information about lexical and other automated mappings](https://github.com/gbv/jskos/issues/152).
However, lossless conversion between data models isn't always possible, nor is
it always necessary.

While they are both generally applicable

considering the different scopes in which they are developed and used - JSKOS is
developed primarily within the digital humanities and SSSOM is developed within
the life sciences, though both are generally applicable to any domain.

## Technical Implementation

The [sssom-js](https://github.com/gbv/sssom-js) Javascript package contained the
first SSSOM to JSKOS converter and has an
[open issue](https://github.com/gbv/sssom-js/issues/5) for conversion back to
SSSOM (TSV). This implementation is produced by the JSKOS team, meaning

- Added wrapper around sssom-js in
  https://github.com/cthoyt/sssom-pydantic/pull/26

## Motivation for SSSOM-JSKOS interoperability

- NFDI has the JSKOS stack, such as [Cocoda](https://coli-conc.gbv.de/cocoda/)
- https://gbv.github.io/jskos/#mapping
-

## Results / TODO

- Worked on JSKOS package in github.com/cthoyt/jskos, reuse text from there
