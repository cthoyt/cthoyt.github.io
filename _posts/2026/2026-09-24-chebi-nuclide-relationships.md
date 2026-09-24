---
layout: post
title: Axiomatizing Nuclides and their Relationships in ChEBI
date: 2026-09-04 16:35:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEBI
  - chemistry
  - ontology
  - biocuration
---

In my [previous post]({% post_url 2026/2026-09-04-chebi-atomic-numbers %}),
I created axioms for atomic numbers for atoms represented in ChEBI.

In this post, I take a similar approach to axiomizing the neutron number and
nucleon number (i.e., atomic number + neutron number) for fully qualified atoms
appearing as children of partially qualified atoms in ChEBI.

Then, I materialize relationships between fully qualified atoms: isotope (same
atomic number), isotone (same neutron number), and isobar (same nucleon number)
materialization.

This post covers
[cthoyt/chebi-atomic-numbers-ontology@2](https://github.com/cthoyt/chebi-atomic-numbers-ontology/pull/2)
and
[cthoyt/chebi-atomic-numbers-ontology#3](https://github.com/cthoyt/chebi-atomic-numbers-ontology/pull/3).

## Making a ROBOT template

While ChEBI has full coverage through element 117 in the atoms branch, it only
has light coverage of isotopes. While some of them have been operationalized
with the `isotopes.tsv` file, the following script can be used to generate
additional rows.

With the exception of the three isotopes of hydrogen, which each have their own
labels, all isotopes have the nomenclature scheme `<element>-<nucleon number>`.

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
isotopes_df.to_csv("isotopes-extended.tsv", sep="\t", index=False)
```

| curie       | type  | label          |                      nucleon number |                      neutron number |
|-------------|-------|----------------|------------------------------------:|------------------------------------:|
| ID          | TYPE  |                | SC 'ChEMROF:nucleon_number' value % | SC 'ChEMROF:neutron_number' value % |
| CHEBI:29236 | class | protium atom   |                                   1 |                                   0 |
| CHEBI:29237 | class | deuterium atom |                                   2 |                                   1 |
| CHEBI:29238 | class | tritium atom   |                                   3 |                                   2 |
| CHEBI:30218 | class | helium-3       |                                   3 |                                   1 |
| CHEBI:37004 | class | helium-8       |                                   8 |                                   6 |
| CHEBI:30219 | class | helium-4       |                                   4 |                                   2 |
| CHEBI:37003 | class | helium-6       |                                   6 |                                   4 |

## Materializing relationships

OWL is really against encoding logical relationship rules about classes. I wish
SWRL supported this, but the ivory tower says "don't do that" once again. If you
want to get around this, you have to invoke the arcane arts of punning, and I
don't think that it's worth it. So instead, I used SPARQL to create new
relationships between classes.

### Isotopes

[Isotopes](https://en.wikipedia.org/wiki/Isotope)
are atoms of the same element with different number of neutrons. They can be
produced, e.g., through the process of
[neutron capture](https://en.wikipedia.org/wiki/Neutron_capture). For example,
[thallium-199 (CHEBI:37805)](https://semantic.farm/CHEBI:37805),
[thallium-201 (CHEBI:37804)](https://semantic.farm/CHEBI:37804),
[thallium-203 (CHEBI:37802)](https://semantic.farm/CHEBI:37802), and
[thallium-205 (CHEBI:37803)](https://semantic.farm/CHEBI:37803) are isotopes
of thallium.

The following SPARQL materializes isotope relationships between atoms
using the [ChEMROF:isotope_of](https://semantic.farm/ChEMROF:isotope_of)
relationship.

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

[Isotones](https://en.wikipedia.org/wiki/Isotone)
are atoms of different elements with the same number of neutrons. They can be
produced, e.g., through the process of
[proton capture](https://en.wikipedia.org/wiki/Proton_capture). For example,
[nitrogen-17 (CHEBI:36937)](https://semantic.farm/)
[oxygen-18 (CHEBI:33815)](https://semantic.farm/CHEBI:33815), and
[fluorine-19 (CHEBI:36940)](https://semantic.farm/CHEBI:36940) each have 10
neutrons.

The following SPARQL materializes isotone relationships between atoms
using the [ChEMROF:isotone_of](https://semantic.farm/ChEMROF:isotone_of)
relationship.

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

[Isobars](https://en.wikipedia.org/wiki/Isobar_(nuclide)) are atoms of different
elements with the same number of nucleons. They can be produced, e.g., through
the process of [beta decay](https://en.wikipedia.org/wiki/Beta_decay). For
example,
[nitrogen-15 (CHEBI:36934)](https://semantic.farm/CHEBI:36934)
and [oxygen-15 (CHEBI:36932)](https://semantic.farm/CHEBI:36932) are isobars
with the same nucleon number of 15.

The following SPARQL materializes isobar relationships between atoms
using the [ChEMROF:nucleon_number](https://semantic.farm/ChEMROF:nucleon_number)
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

### Additional relationships

[Isodiaphers](https://en.wikipedia.org/wiki/Nuclide#Types_of_nuclides)
are atoms with equal neutron excess (i.e., neutron number minus atomic number).
They can be produced, e.g., through the process of
[alpha decay](https://en.wikipedia.org/wiki/Alpha_decay). For example,
[carbon-13 (CHEBI:36928)](https://semantic.farm/CHEBI:36928),
[nitrogen-15 (CHEBI:36934)](https://semantic.farm/CHEBI:36934), and
[oxygen-17 (CHEBI:33819)](https://semantic.farm/CHEBI:33819) are isodiaphers
with a neutron excess of 1.

[Mirror nuclei](https://en.wikipedia.org/wiki/Mirror_nuclei) are atoms whose
neutron numbers and atomic numbers are swapped. They can be produced, e.g.,
through the process of
[positron emission](https://en.wikipedia.org/wiki/Positron_emission). For
example, [tritium (CHEBI:29238)](https://semantic.farm/CHEBI:29238) and
[helium-3 (CHEBI:30218)](https://semantic.farm/CHEBI:30218) are mirror nuclei.
