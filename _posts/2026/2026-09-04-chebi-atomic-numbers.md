---
layout: post
title: Axiomatizing Atomic Numbers in ChEBI
date: 2026-09-04 16:35:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEBI
  - chemistry
  - ontology
  - biocuration
---

This post describes how I produced a
[novel ontology module](https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl)
that axiomatizes the relationships between terms representing elements in ChEBI
(i.e., subclasses of [CHEBI:33250](https://semantic.farm/CHEBI:33250)) and their
atomic numbers as subclass expressions with data restrictions, and the ROBOT
[template](https://robot.obolibrary.org/template.html) magic that made it
possible.

## Motivation

I am currently developing a suite of ontologies for theoretical chemistry with
[Mario Wolter](https://github.com/MarioWolter) and
[Robin Ströhmann](https://github.com/CodoRob) as part of
[NFDI4Chem](https://nfdi4chem.de).

In our first module, we are ontologizing
[basis sets](https://en.wikipedia.org/wiki/Basis_set_%28chemistry%29), sets of
mathematical functions and their respective parametrization used to construct
wave equations in computational chemistry experiments. We are building on the
[Basis Set Exchange](https://www.basissetexchange.org), a comprehensive database
of basis sets that itself is missing the organization of an ontology.

[![](/img/basis-set-to-elements.svg)](https://docs.google.com/drawings/d/1ejVJLlijiJEdzlasYgKAIf9oXjRmSVvi6v6QbVUND4c/edit?usp=sharing)

A key aspect of a basis set is definition of how each orbital is modeled for
each element. Not all basis sets can be used to model all elements.

The definition of each basis set in Basis Set Exchange is transformed into
axioms about which atoms it supports, where the atoms are encoded with ChEBI
terms under the CHEBI:33250 (atom) hierarchy Molecules that are encoded in ChEBI
have axioms saying which atoms are in them A logical rule can be encoded in BSEO
so reasoners can infer whether a given basis set is applicable to a molecule if
all atoms that are parts of the molecule are also supported by the basis set.
We're currently in the process of determining how to best formalize this Of
course, this can also be trivially implemented using any modern cheminformatics
software package, but the implications are that this logic can be formalized

https://github.com/NFDI4Chem/basis-set-exchange-ontology

Why? im currently working on making an ontology for theoretical chemistry with
Mario and Robin. we're looking at basis sets, and need to ontologize the fact
that some basis sets are only applicable for certain atoms. I wanted a mapping
from atomic number to an ontology identifier - ChEBI would be the first guess,
but they don't have this mapping. Therefore, I wanted to make this mapping
explicit so I could reuse it in Python code and also to axiomatize it in OWL.

https://github.com/cthoyt/chebi-atomic-numbers-ontology

This repository contains an ontology component that injects axioms for the
atomic numbers for the atoms in ChEBI's
[atom (CHEBI:33250)](https://www.ebi.ac.uk/chebi/CHEBI:33250) hierarchy.

The resulting ontology artifact is available from
[https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl](https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl)
(PURL coming soon).

## How did I make it?

I started with a dictionary of element to name, then used PyOBO

```python
import pyobo

element_to_name = {
    1: "hydrogen",
    # everything in between
    118: "oganesson",
}

grounder = pyobo.get_grounder("chebi")
for element, name in element_to_name.items():
    match = grounder.get_best_match(name)
```

Issues along the way I had to contribute back to ChEBI in
https://github.com/ebi-chebi/ChEBI/issues/4958

| atomic number | ChEBI label  | CURIE                                            | Problem                                                                                                       |
| ------------: | ------------ | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
|            13 | Aluminium    | [CHEBI:28984](https://semantic.farm/CHEBI:28984) | missing american spelling variant, see [ebi-chebi/ChEBI#4956](https://github.com/ebi-chebi/ChEBI/issues/4956) |
|            46 | Palladium    | [CHEBI:33363](https://semantic.farm/CHEBI:33363) | is in atom hierarchy, but name is missing suffix "atom"                                                       |
|            55 | Caesium      | [CHEBI:30514](https://semantic.farm/CHEBI:30514) | missing american spelling variant [ebi-chebi/ChEBI#4957](https://github.com/ebi-chebi/ChEBI/issues/4957)      |
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

## Next Steps

I want to make a "full" version of this which also uses the MIREOT algorithm to
get all atoms and pull in the upstream annotations from the upstream ChEBI
ontology file. That's happening in
https://github.com/cthoyt/chebi-atomic-numbers-ontology, with the goal to make
an easier to explore OWL file.

---

While I put everything in a GitHub repository and archived it on Zenodo
[![DOI](https://zenodo.org/badge/1357107774.svg)](https://doi.org/10.5281/zenodo.22306043),
I would love to see this get upstreamed to ChEBI itself.
