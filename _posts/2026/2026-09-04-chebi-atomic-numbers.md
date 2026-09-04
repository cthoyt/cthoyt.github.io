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
that axiomatizes the atomic numbers for ChEBI terms representing atoms (i.e.,
subclasses of [CHEBI:33250](https://semantic.farm/CHEBI:33250)) using subclass
expressions with data restrictions, and the ROBOT
[template](https://robot.obolibrary.org/template.html) magic that made it
possible.

## Motivation

I am currently working in [NFDI4Chem](https://nfdi4chem.de) with
[Mario Wolter](https://github.com/MarioWolter) and
[Robin Ströhmann](https://github.com/CodoRob) at TU Braunschweig towards
developing an ontology for theoretical chemistry. Our first narrowly scoped
module covers
[basis sets](https://en.wikipedia.org/wiki/Basis_set_%28chemistry%29) - sets of
mathematical functions and their respective parametrization used to construct
wave equations in computational chemistry experiments. Our initial approach is
to extend the [Basis Set Exchange](https://www.basissetexchange.org), an
existing comprehensive database of basis sets that could be made more valuable
by ontologizing its contents.

A key aspect of each basis set is to which elements it is applicable. While any
general purpose programming language with a cheminformatics package could be
used to parse a molecule from SMILES, InChI, Molfile, SDF, or other format then
cross-check against the basis set metadata (see below), our goal is to enable an
ontology reasoner to determine which basis sets are applicable to a molecule
based on logical axioms connecting the molecule with the
[has part (BFO:0000051)](https://semantic.farm/BFO:0000051) relationship to a
subclass of [atom (CHEBI:33250)](https://semantic.farm/CHEBI:33250).

[![](/img/basis-set-to-elements.svg)](https://docs.google.com/drawings/d/1ejVJLlijiJEdzlasYgKAIf9oXjRmSVvi6v6QbVUND4c/edit?usp=sharing)

Each basis set in the Basis Set Exchange can be downloaded as JSON from their
API. For example, the _4-31G valence double-zeta basis set_ can be downloaded
[here](http://www.basissetexchange.org/api/basis/4-31g/format/json/?version=1)
and gives the following JSON (lightly edited and abridge for clarity, element
values removed):

```json
{
  "name": "4-31G",
  "family": "pople",
  "description": "4-31G valence double-zeta basis set",
  "role": "orbital",
  "elements": {
    "1": {},
    "2": {},
    "5": {},
    "6": {},
    "7": {},
    "8": {},
    "9": {},
    "10": {},
    "15": {},
    "16": {},
    "17": {}
  }
}
```

With this data, I am very close to being able to create axioms on my basis set
terms for which atoms they support. The issue with this data is that I don't
have a mapping from the atomic numbers appearing as keys in the `elements`
dictionary to the ChEBI terms for each atom.

It turns out, that this information isn't encoded in ChEBI at all! My natural
reflex was to start curating and to start coding a solution. The resulting
ontology module is available
[here](https://github.com/cthoyt/chebi-atomic-numbers-ontology/raw/refs/heads/main/chebi-atomic-numbers.owl).

## How did I make it?

I started with a cursory search of ChEBI to understand the different senses in
which atoms/elements are encoded - the atom hierarchy typically has the element
name plus "atom" at the end, except in a few cases. I curated a dictionary
mapping from atomic number to element name in Python then used
[PyOBO](https://github.com/biopragmatics/pyobo) to look up ChEBI terms based on
labels using the following (pseudo)code:

```python
import pyobo
from pystow.utils import safe_open_writer

atomic_number_to_name = {
    1: "hydrogen",
    # and everything in between, omitted for brevity
    118: "oganesson",
}
grounder = pyobo.get_grounder("chebi")
with safe_open_writer("elements.tsv") as writer:
    writer.writerow(("ID", "TYPE", "label", "atomic number"))
    writer.writerow(("ID", "TYPE", "", "SC 'ChEMROF:atomic_number' value %"))
    for atomic_number, name in atomic_number_to_name.items():
        if match := grounder.get_best_match(f"{name} atom"):
            writer.writerow((match.curie, "class", match.name, atomic_number))
        elif match := grounder.get_best_match(name):
            # all nine of these cases were post-checked to be correct, see table below
            writer.writerow(
                (match.curie, "class - check/fix", match.name, atomic_number)
            )
        else:
            # this never happens, because ChEBI is comprehensive
            raise ValueError(f"no match available for {name}")
```

Along the way, I found nine elements that fell within the atom hierarchy but
were named without the "atom" suffix. I also found that for aluminum and cesium
that ChEBI only encoded the British spelling and not the American spelling, so
these had to be post-curated by hand. I opened up an issue on the ChEBI
repository summarizing the situation at
[ebi-chebi/ChEBI#4958](https://github.com/ebi-chebi/ChEBI/issues/4958):

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

The primary manually curated artifact in this repository
([cthoyt/chebi-atomic-numbers-ontology](https://github.com/cthoyt/chebi-atomic-numbers-ontology))
is
[elements.tsv](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/src/elements.tsv),
a tab-separated values (TSV) file that contains templating information in its
header that directs [ROBOT](https://robot.obolibrary.org) how to convert it into
an ontology file.

The contents of the file look like this:

| ID                                                 | TYPE  | label           |                                                                     atomic number |
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
3. `label` having a label column is important to make this file human-readable,
   but it's better to keep the output ontology module lean, so I didn't add a
   ROBOT command.  
   If I had wanted to serialize these values, I could have used the ROBOT
   command `AT rdfs:label^^xsd:string`.
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

In addition to keeping the ontology lean, omitting the labels also avoids the
issue where the labels in my curated resource might get out of sync with the
upstream ChEBI ontology. This is especially true because this work prompted me
to petition ChEBI to update some of these labels! A typical ontology workflow is
to have both a _lean_ and a _full_ export. In the full export, I can use the
`robot extract` command with the
[MIREOT algorithm](https://robot.obolibrary.org/extract.html#mireot) to pull in
all descendants of the ChEBI atom class and merge them in the build. This also
has the benefit of making the _full_ export easier for humans to navigate, e.g.,
from Protégé.

## How to make the ontology export

The usage of [`robot template`](https://robot.obolibrary.org/template.html) is
encoded in the repository's
[ `justfile`](<[justfile](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/justfile)>).
This does the following:

1. Qualifies all prefixes used (CHEBI and ChEMROF)
2. Merges a dedicate metadata ontology module
   [`metadata.ofn`](<[src/metadata.ofn](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/src/metadata.ofn)>)
3. Adds declaration information for the data property that doesn't appear in
   `entities.tsv` that is in a different ROBOT template
   [`properties.tsv`](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/src/properties.tsv)

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

---

While I put everything in a GitHub repository and archived it on Zenodo
[![DOI](https://zenodo.org/badge/1357107774.svg)](https://doi.org/10.5281/zenodo.22306043),
I would love to see this get upstreamed to ChEBI itself. Now, I can get back to
the original goal of encoding the basis set information 🚀
