---
layout: post
title: Axiomatizing Nuclides in ChEBI
date: 2026-09-24 12:00:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEBI
  - chemistry
  - ontology
  - biocuration
---

This post describes how I extended the work in my [previous
post]({% post_url 2026/2026-09-04-chebi-atomic-numbers %}) that axiomatizes
neutron numbers and nucleon numbers for isotopes that appear in ChEBI as
children of atom terms, then materializes isotope (same atomic number), isotone
(same neutron number), and isobar (same nucleon number) relationships between
them.

While the previous post was directly motivated by needs for the upcoming basis
set ontology for NFDI4Chem, extending the axiomizations from partially qualified
atoms (with just atomic number) to fully qualified atoms (with both atomic and
neutron number) was an obvious next step once I was already familiar with the
ChEBI atom hierarchy.

The code and data presented in this post were added in
[cthoyt/chebi-atomic-numbers-ontology@2](https://github.com/cthoyt/chebi-atomic-numbers-ontology/pull/2)
and
[cthoyt/chebi-atomic-numbers-ontology#3](https://github.com/cthoyt/chebi-atomic-numbers-ontology/pull/3).

## Making the ROBOT template

While ChEBI has full coverage through element 117 in the atoms branch, it only
has partial coverage of isotopes. I used the following script to produce an
initial ROBOT template:

```python
import pandas as pd
import pyobo

elements_df = pd.read_csv("elements.tsv", sep="\t", skiprows=2, header=None)
rows = []
for curie, _, label, number in elements_df.values:
    for child in pyobo.get_descendants(curie) or []:
        full_name = pyobo.get_name(child, strict=True)
        name = full_name.removesuffix("atom").strip()
        _, _, total = name.partition("-")
        if total:
            total = int(total)
            rows.append((child.curie, "class", name, total, total - number))
        else:
            print(f"failed on {child.curie} - {full_name}")

isotopes_df = pd.DataFrame(rows)
isotopes_df.to_csv("isotopes.tsv", sep="\t", index=False)
```

Except the three isotopes of hydrogen, which each have their own labels, all
isotopes' labels have the following form: `<element>-<nucleon number>`. Here are
few example rows from the
[full ROBOT template](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/src/isotopes.tsv):

| curie                                            | type  | label          |                                                                      nucleon number |                                                                      neutron number |
| ------------------------------------------------ | ----- | -------------- | ----------------------------------------------------------------------------------: | ----------------------------------------------------------------------------------: |
| ID                                               | TYPE  |                | SC '[ChEMROF:nucleon_number](https://semantic.farm/ChEMROF:nucleon_number)' value % | SC '[ChEMROF:neutron_number](https://semantic.farm/ChEMROF:neutron_number)' value % |
| [CHEBI:29236](https://semantic.farm/CHEBI:29236) | class | protium atom   |                                                                                   1 |                                                                                   0 |
| [CHEBI:29237](https://semantic.farm/CHEBI:29237) | class | deuterium atom |                                                                                   2 |                                                                                   1 |
| [CHEBI:29238](https://semantic.farm/CHEBI:29238) | class | tritium atom   |                                                                                   3 |                                                                                   2 |
| [CHEBI:30218](https://semantic.farm/CHEBI:30218) | class | helium-3       |                                                                                   3 |                                                                                   1 |
| [CHEBI:37004](https://semantic.farm/CHEBI:37004) | class | helium-8       |                                                                                   8 |                                                                                   6 |
| [CHEBI:30219](https://semantic.farm/CHEBI:30219) | class | helium-4       |                                                                                   4 |                                                                                   2 |
| [CHEBI:37003](https://semantic.farm/CHEBI:37003) | class | helium-6       |                                                                                   6 |                                                                                   4 |

This template works the same way I described in the [previous post]({% post_url
2026/2026-09-04-chebi-atomic-numbers %}), now using two columns for data value
constraints instead of just a single column. Note, the links are added here for
convenience, and don't/shouldn't actually appear in ROBOT templates.

Interestingly, a related
[discussion](https://github.com/NFDI4Chem/Ontologies4Chem2026/discussions/8)
will be taking place at the
[Ontologies4Chem Workshop 2026](https://nfdi4chem.de/event/5th-ontologies4chem-workshop/).
I would like to add the missing isotopes to ChEBI, but this will probably take a
while!

## Materializing Relationships

I had high hopes that formalizing the atomic number, nucleon number, and neutron
number would allow for me to encode inference rules to cover what it means for
two fully qualified atoms to be isotopes, isobars, or isotones of each other,
for example, using
[Semantic Web Rule Language (SWRL)](https://www.w3.org/2003/11/swrl#). However,
I had a pretty typical experience that the OWL and semantic web technologies
don't directly support this (IMO) rather obvious use case.

Instead, I opted to write several SPARQL queries that can be used with
[`robot query`](https://robot.obolibrary.org/query.html) to manipulate OWL as
RDF and add in new object property constraints directly with a command like:

```console
$ robot query \
    --update src/isobar-construct.ru \
    --update src/isotone-construct.ru \
    --update src/isotope-construct.ru
```

See the full incorporation into the build in the repository's
[justfile](https://github.com/cthoyt/chebi-atomic-numbers-ontology/blob/main/justfile).

### Isotopes

[Isotopes](https://en.wikipedia.org/wiki/Isotope) are atoms of the same element
with different number of neutrons. They can be produced, e.g., through the
process of [neutron capture](https://en.wikipedia.org/wiki/Neutron_capture). For
example, [thallium-199 (CHEBI:37805)](https://semantic.farm/CHEBI:37805),
[thallium-201 (CHEBI:37804)](https://semantic.farm/CHEBI:37804),
[thallium-203 (CHEBI:37802)](https://semantic.farm/CHEBI:37802), and
[thallium-205 (CHEBI:37803)](https://semantic.farm/CHEBI:37803) are isotopes of
thallium.

The following SPARQL materializes isotope relationships between atoms using the
[ChEMROF:isotope_of](https://semantic.farm/ChEMROF:isotope_of) relationship.

```sparql
INSERT {
    ?x rdfs:subClassOf [
        owl:onProperty ChEMROF:isotope_of;
        owl:someValuesFrom ?y
    ] .
}
WHERE {
    ?atom rdfs:subClassOf [
        owl:onProperty ChEMROF:atomic_number;
        owl:hasValue ?atomic_number
    ] ;
    ?x rdfs:subClassOf ?atom .
    ?y rdfs:subClassOf ?atom .
    FILTER(?x != ?y)
}
```

### Isotone

[Isotones](https://en.wikipedia.org/wiki/Isotone) are atoms of different
elements with the same number of neutrons. They can be produced, e.g., through
the process of [proton capture](https://en.wikipedia.org/wiki/Proton_capture).
For example, [nitrogen-17 (CHEBI:36937)](https://semantic.farm/)
[oxygen-18 (CHEBI:33815)](https://semantic.farm/CHEBI:33815), and
[fluorine-19 (CHEBI:36940)](https://semantic.farm/CHEBI:36940) each have 10
neutrons.

The following SPARQL materializes isotone relationships between atoms using the
[ChEMROF:isotone_of](https://semantic.farm/ChEMROF:isotone_of) relationship.

```sparql
INSERT {
    ?x rdfs:subClassOf [
        owl:onProperty ChEMROF:isotone_of;
        owl:someValuesFrom ?y
    ] .
}
WHERE {
    ?x rdfs:subClassOf [
        owl:onProperty ChEMROF:neutron_number;
        owl:hasValue ?value
    ] .
    ?y rdfs:subClassOf [
        owl:onProperty ChEMROF:neutron_number;
        owl:hasValue ?value
    ] .
    FILTER(?x != ?y)
}
```

### Isobar

[Isobars](<https://en.wikipedia.org/wiki/Isobar_(nuclide)>) are atoms of
different elements with the same number of nucleons. They can be produced, e.g.,
through the process of [beta decay](https://en.wikipedia.org/wiki/Beta_decay).
For example, [nitrogen-15 (CHEBI:36934)](https://semantic.farm/CHEBI:36934) and
[oxygen-15 (CHEBI:36932)](https://semantic.farm/CHEBI:36932) are isobars with
the same nucleon number of 15.

The following SPARQL materializes isobar relationships between atoms using the
[ChEMROF:nucleon_number](https://semantic.farm/ChEMROF:nucleon_number)
relationship.

```sparql
INSERT {
    ?x rdfs:subClassOf [
        owl:onProperty ChEMROF:isobar_of;
        owl:someValuesFrom ?y
    ] .
}
WHERE {
    ?x rdfs:subClassOf [
        owl:onProperty ChEMROF:nucleon_number;
        owl:hasValue ?value
    ] .
    ?y rdfs:subClassOf [
        owl:onProperty ChEMROF:nucleon_number;
        owl:hasValue ?value
    ] .
    FILTER(?x != ?y)
}
```

## Additional Relationships

While I exhausted the current ChEMROF predicates, there still remain a few that
I found while reading up on Wikipedia:

[Isodiaphers](https://en.wikipedia.org/wiki/Nuclide#Types_of_nuclides) are atoms
with equal neutron excess (i.e., neutron number minus atomic number). They can
be produced, e.g., through the process of
[alpha decay](https://en.wikipedia.org/wiki/Alpha_decay). For example,
[carbon-13 (CHEBI:36928)](https://semantic.farm/CHEBI:36928),
[nitrogen-15 (CHEBI:36934)](https://semantic.farm/CHEBI:36934), and
[oxygen-17 (CHEBI:33819)](https://semantic.farm/CHEBI:33819) are isodiaphers
with a neutron excess of 1. I made a
[pull request to ChEMROF](https://github.com/chemkg/chemrof/pull/95) to add this
relationship - after some discussion, I might also include an additional SPARQL
query.

[Mirror nuclei](https://en.wikipedia.org/wiki/Mirror_nuclei) are atoms whose
neutron numbers and atomic numbers are swapped. They can be produced, e.g.,
through the process of
[positron emission](https://en.wikipedia.org/wiki/Positron_emission). For
example, [tritium (CHEBI:29238)](https://semantic.farm/CHEBI:29238) and
[helium-3 (CHEBI:30218)](https://semantic.farm/CHEBI:30218) are mirror nuclei.
