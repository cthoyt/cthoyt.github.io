---
layout: post
title: ChEBI Atomic Numbers
date: 2026-09-04 16:35:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEBI
  - chemistry
  - ontology
  - biocuration
---

NFDI4Chem

[![DOI](https://zenodo.org/badge/1357107774.svg)](https://doi.org/10.5281/zenodo.22306043)

This repository contains an ontology component that injects axioms for the
atomic numbers for the atoms in ChEBI's
[atom (CHEBI:33250)](https://www.ebi.ac.uk/chebi/CHEBI:33250) hierarchy.

The resulting ontology artifact is available from
[https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl](https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl)
(PURL coming soon).

## How did I make it?

I started with a dictionary of element to name, then used PyOBO

```bibtex
import pyobo

element_to_name = {1: "hydrogen", ...}

grounder = pyobo.get_grounder("chebi")
for element, name in element_to_name.items():
match = grounder.get_best_match(name)
```

Issues along the way I had to contribute back to ChEBI in
https://github.com/ebi-chebi/ChEBI/issues/4958

| atomic number | ChEBI label  | CURIE                                            | Problem                                                                                                       |
| ------------: | ------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
|            13 | Aluminum     | [CHEBI:28984](https://semantic.farm/CHEBI:28984) | missing american spelling variant, see [ebi-chebi/ChEBI#4956](https://github.com/ebi-chebi/ChEBI/issues/4956) |
|            46 | Palladium    | [CHEBI:33363](https://semantic.farm/CHEBI:33363) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            55 | Cesium       | [CHEBI:30514](https://semantic.farm/CHEBI:30514) | missing american spelling variant [ebi-chebi/ChEBI#4957](https://github.com/ebi-chebi/ChEBI/issues/4957)      |
|            58 | Cerium       | [CHEBI:33369](https://semantic.farm/CHEBI:33369) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            68 | Erbium       | [CHEBI:33379](https://semantic.farm/CHEBI:33379) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            70 | Ytterbium    | [CHEBI:33381](https://semantic.farm/CHEBI:33381) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            78 | Platinum     | [CHEBI:33364](https://semantic.farm/CHEBI:33364) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            90 | Thorium      | [CHEBI:33385](https://semantic.farm/CHEBI:33385) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|           100 | Fermium      | [CHEBI:33394](https://semantic.farm/CHEBI:33394) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|           102 | Nobelium     | [CHEBI:33396](https://semantic.farm/CHEBI:33396) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|           110 | Darmstadtium | [CHEBI:33367](https://semantic.farm/CHEBI:33367) | is in atom hierarchy, but name is missing suffix "atom"                                                       |

## How does this work?

The primary manually curated artifact in this repository is
[src/elements.tsv](src/elements.tsv), a tab-separated values (TSV) file that
contains templating information in its header that directs
[ROBOT](https://robot.obolibrary.org) how to convert it into an ontology file.

The file looks like this:

| ID                                                 | type  | label           |                                                                     atomic number |
| -------------------------------------------------- | ----- | --------------- | --------------------------------------------------------------------------------: |
| ID                                                 | TYPE  |                 | SC '[ChEMROF:atomic_number](https://semantic.farm/ChEMROF:atomic_number)' value % |
| [CHEBI:49637](https://semantic.farm/CHEBI:49637)   | class | hydrogen atom   |                                                                                 1 |
| [CHEBI:30217](https://semantic.farm/CHEBI:30217)   | class | helium atom     |                                                                                 2 |
| ...                                                | ...   | ...             |                                                                               ... |
| [CHEBI:194539](https://semantic.farm/CHEBI:194539) | class | tennessine atom |                                                                               117 |
| [CHEBI:194541](https://semantic.farm/CHEBI:194541) | class | oganesson atom  |                                                                               118 |

Note that there are two header rows: the first contains labels and the second
contains ROBOT commands. Here's what each means:

1. The `ID` command says that this column contains the CURIE for the entity
   we're annotating. We write `ID` in both the human label and the ROBOT command
   here to reduce confusion.
2. `TYPE` says what kind of entity it is and how it should get declared. Either
   an informal abbreviation `class` or fully qualified CURIE `owl:Class` can be
   used in this column
3. `label` having a label column is important to make this file readable, but I
   actually didn't want to add label axioms this way. The issue is this TSV
   could get out of sync with the upstream, especially because I suggested
   several of the relevant classes get their names improved in
   https://github.com/ebi-chebi/ChEBI/issues/4958 while I was working on this.
   As an alternative, these can be slurped from the current OWL file and merged
   (future work). If I wanted to include this, I would add
   `AT rdfs:label^^xsd:string`.
4. `atomic number` this is the coolest part of what's going on in this file.
   `SC 'ChEMROF:atomic_number' value %` has four parts:
   1. `SC` means that this is going to be a subclass expression
   2. [`ChEMROF:atomic_number`](https://chemkg.github.io/chemrof/atomic_number/)
      is the data property from the
      [Chemical Entity Materials and Reactions Ontological Framework (CHEMROF)](https://semantic.farm/registry/chemrof)
      used in the expression. Quotes around the CURIE are required!
   3. `value` signals it's going to be a literal
   4. `%` is the placeholder for the value in each row

Because of the flexibility of the ROBOT templating language, this TSV can
effectively be used as a normal TSV, e.g., to programmatically get the mapping
from ChEBI identifiers to atomic numbers without going through OWL software.

## How to make the ontology export

The usage of [`robot template`](https://robot.obolibrary.org/template.html) is
encoded in this repository's [ `justfile`](justfile). This does the following:

1. Qualifies all prefixes used (CHEBI and ChEMROF)
2. Merges in metadata from a different ontology file
   [`src/metadata.ofn`](src/metadata.ofn)
3. Adds declaration information for the data property from
   [`src/properties.tsv`](src/properties.tsv) that doesn't appear in
   `entities.tsv`

These can all be re-run with:

```console
$ just convert
```

The results are OWL that look like this (shown in OFN for brevity):

```
SubClassOf(CHEBI:49637 DataHasValue(ChEMROF:atomic_number "1"^^xsd:integer))
SubClassOf(CHEBI:30217 DataHasValue(ChEMROF:atomic_number "2"^^xsd:integer))
...
SubClassOf(CHEBI:194539 DataHasValue(ChEMROF:atomic_number "117"^^xsd:integer))
SubClassOf(CHEBI:194541 DataHasValue(ChEMROF:atomic_number "118"^^xsd:integer))
```
