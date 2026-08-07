---
layout: post
title: Mapping from SSSOM to OWL
date: 2026-08-07 13:59:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - ontologies
  - OWL
  - semantic mappings
  - OFN
  - functional OWL
---

The [Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
specifies a transformation from its data model to the to [Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-overview/)
its [documentation](https://mapping-commons.github.io/sssom/dev/spec-formats-owl/). This post is
about implementing and extending that transformation in the
[sssom-pydantic](https://github.com/cthoyt/sssom-pydantic/pull/159) Python package.

The transformation from SSSOM to OWL enables ontology curators to externalize curation of semantic mappings into
SSSOM TSV files, which better support curators in capturing precise mapping
predicates and provenance metadata. After, SSSOM can be transformed into OWL and
merged with their ontology edit file during release, for example, using the
[ROBOT](https://robot.obolibrary.org/) tool.

SSSOM-Pydantic implements the
transformation into the [OWL Functional-Style Syntax](https://www.w3.org/TR/owl2-syntax/)
object model with the [`functional-owl`](https://github.com/cthoyt/functional-owl) package,
which enables serialization to OWL Functional Notation (OFN), OWL/RDF, and
OWL/XML.

## Usage

A semantic mapping can be transformed with the [`get_axiom()`](https://sssom-pydantic.readthedocs.io/en/latest/api/sssom_pydantic.contrib.owl.get_axiom.html) function:

```python
from curies import Converter
from sssom_pydantic import SemanticMapping
from sssom_pydantic.contrib.owl import get_axiom
converter = Converter.from_prefix_map({
    "mesh": "http://id.nlm.nih.gov/mesh/",
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
})
mapping = SemanticMapping.exact("mesh:C000089", "CHEBI:28646")
get_axiom(mapping, converter).to_funowl()
# AnnotationAssertion(skos:exactMatch mesh:C000089 CHEBI:28646)
```

A collection of semantic mappings and optional mapping set metadata can be
written to an OWL file with [`write_owl`](https://sssom-pydantic.readthedocs.io/en/latest/api/sssom_pydantic.contrib.owl.write_owl.html).

```python
from curies import Converter, Reference
from sssom_pydantic import SemanticMapping, MappingSet
from sssom_pydantic.examples import TEST_CONVERTER
from sssom_pydantic.contrib.owl import write_owl

converter = Converter.from_prefix_map({
    "CHEBI": "http://purl.obolibrary.org/obo/CHEBI_",
    "dcterms": "http://purl.org/dc/terms/",
    "mesh": "http://id.nlm.nih.gov/mesh/",
    "orcid": "https://orcid.org/",
})
metadata = MappingSet(
    id="https://example.org/test.sssom.tsv",
    creators=[Reference(prefix="orcid", identifier="0000-0003-4423-4370")],
)
mappings = [SemanticMapping.exact("mesh:C000089", "CHEBI:28646")]
write_owl(
    mappings,
    "test.ofn",
    metadata=metadata,
    converter=converter,
    generation_date_comment=False,
)
```

which outputs the following OWL functional notation (OFN):

```
Prefix(CHEBI:=<http://purl.obolibrary.org/obo/CHEBI_>)
Prefix(dcterms:=<http://purl.org/dc/terms/>)
Prefix(mesh:=<http://id.nlm.nih.gov/mesh/>)
Prefix(orcid:=<https://orcid.org/>)

Ontology(
    Annotation(dcterms:creator orcid:0000-0003-4423-4370)
    AnnotationAssertion(skos:exactMatch mesh:C000089 CHEBI:28646)
)
```

Throughout this post, I'm going to omit the annotations on the annotation
assertions that come from other SSSOM metadata such as the confidence and author.
These can be added with the `mapping_annotations=True` in `write_owl()`.
This workflow can also be called from the command line with:

```console
$ uv tool install sssom_pydantic
$ sssom_pydantic owl -i test.sssom.tsv -o test.ofn
```

## Transformation Rules

This section describes the SSSOM to OWL transformation rules, which are
dependent on the semantic mapping predicate, the subject type, and object type.
By default, semantic mappings are transformed into annotation properties in OWL,
with a small number of special cases that are transformed into logical axioms.

Finally, this section describes two custom workflows for producing OWL bridge
files (see
[the Uberon documentation](https://github.com/obophenotype/uberon/blob/master/docs/bridges.md))
and for upgrading negated semantic mappings to logical axioms.

### Annotation Properties

Semantic mappings whose predicates are annotation properties, such as those
originating from SKOS, are transformed using the `AnnotationAssertion()` axioms
as follows:

| Semantic Mapping                     | Functional OWL Expression                                 |
|--------------------------------------|-----------------------------------------------------------|
| `S skos:exactMatch O`                | `AnnotationAssertion(skos:exactMatch S O)`                |
| `S skos:broadMatch O`                | `AnnotationAssertion(skos:broadMatch S O)`                |
| `S skos:narrowMatch O`               | `AnnotationAssertion(skos:narrowMatch S O)`               |
| `S skos:closeMatch O`                | `AnnotationAssertion(skos:closeMatch S O)`                |      
| `S skos:relatedMatch O`              | `AnnotationAssertion(skos:relatedMatch S O)`              |
| `S rdfs:seeAlso O`                   | `AnnotationAssertion(skos:seeAlso S O)`                   |
| `S oboInOwl:hasDbXref O`             | `AnnotationAssertion(oboInOwl:hasDbXref S O)`             |
| `S IAO:0000118 O` (alternate term)   | `AnnotationAssertion(IAO:0000118 S O)`                    |
| `S IAO:0100001 O` (term replaced by) | `AnnotationAssertion(IAO:0100001 S O)`                    |
| `S semapv:crossSpeciesExactMatch O`  | `AnnotationAssertion(semapv:crossSpeciesExactMatch S O)`  |               
| `S semapv:crossSpeciesNarrowMatch O` | `AnnotationAssertion(semapv:crossSpeciesNarrowMatch S O)` |                
| `S semapv:crossSpeciesBroadMatch O`  | `AnnotationAssertion(semapv:crossSpeciesBroadMatch S O)`  |               

In practice, any semantic mapping predicate that doesn't have another
transformation rule associated with it in the following sections
[Logical Axioms for Classes](#logical-axioms-for-classes),
[Logical Axioms for Named Individuals](#logical-axioms-for-named-individuals),
and [Logical Axioms for Properties](#logical-axioms-for-properties) will get
serialized as a `AnnotationAssertion()`.

OWL does not have a generic notion of negations, inversions, or complements.
Therefore, the first-class predicate modifier field in SSSOM that represents
false information is annotated onto the annotation assertion using
`Annotation(sssom:predicate_modifier "Not")` as in:

| Semantic Mapping            | Functional Expression                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------|
| `S not skos:exactMatch O`   | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:exactMatch S O)`   |
| `S not skos:broadMatch O`   | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:broadMatch S O)`   |
| `S not skos:narrowMatch O`  | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:narrowMatch S O)`  |
| `S not skos:closeMatch O`   | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:closeMatch S O)`   |
| `S not skos:relatedMatch O` | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:relatedMatch S O)` |
| `S not rdfs:seeAlso O`      | `AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:seeAlso S O)`      |

Here's an example SSSOM table containing both a positive and negative semantic
mapping and its transformation into OWL, serialized in OWL functional notation
(OFN). The prefix map and metadata are omitted from both the SSSOM and OWL
output for clarity.

| subject_id   | subject_label | predicate_id     | predicate_modifier | object_id     | object_label           | mapping_justification         |
|--------------|--------------|------------------|--------------------|---------------|------------------------|-------------------------------|
| CHEBI:28646  | ammeline     | skos:exactMatch  |                    |  mesh:C000089 | ammeline               | semapv:ManualMappingCuration  |
| CHEBI:10057  | 9H-xanthene  | skos:exactMatch  | Not                | mesh:C002563  | xanthan gum            | semapv:ManualMappingCuration  |

```
Ontology(
    Declaration(Class(CHEBI:28646))
    Declaration(Class(CHEBI:10057))
    Declaration(Class(mesh:C000089))
    Declaration(Class(mesh:C002563))

    AnnotationAssertion(skos:exactMatch CHEBI:28646 mesh:C000089)
    AnnotationAssertion(Annotation(sssom:predicate_modifier "Not") skos:exactMatch CHEBI:10057 mesh:C002563)
)
```

## Logical Axioms for Classes

The following semantic mapping predicates are expanded into OWL logical axioms
describing classes. Any semantic mapping using these predicates have their
subject and object types interpreted as classes.

| Semantic Mapping          | Functional OWL Expression                    |
|---------------------------|----------------------------------------------|
| `S owl:equivalentClass O` | `EquivalentClasses(S O)`                     |
| `S rdfs:subClassOf O`     | `SubClassOf(S O)`                            |
| `S owl:complementOf O`    | `EquivalentClasses(S ObjectComplementOf(O))` |
| `S owl:disjointWith O`    | `DisjointClasses(S O)`                       |

## Logical Axioms for Named Individuals

The following semantic mapping predicates are expanded into OWL logical axioms
describing named individuals. Any semantic mapping using these predicates have
their subject and object types interpreted as named indiduals, with the
exception being `rdfs:type`, which infers the object is a class.

| Semantic Mapping        | Functional OWL Expression   |
|-------------------------|-----------------------------|
| `S rdfs:type O`         | `ClassAssertion(O S)`       |
| `S owl:sameAs O`        | `SameIndividual(S O)`       |
| `S owl:differentFrom O` | `DifferentIndividuals(S O)` |

Here's an example SSSOM table and accompanying OWL output containing examples
for each semantic mapping predicate.

| subject_id    | subject_label          | predicate_id      | object_id     | object_label | mapping_justification        |
|---------------|------------------------|-------------------|---------------|--------------|------------------------------|
| ror:04xfq0f34 | RWTH Aachen University | rdf:type          | OBI:0000245   | organization | semapv:ManualMappingCuration |
| ror:04fbd2g40 | BioNTech (Germany)     | owl:sameAs        | VO:0004946    | BioNTech     | semapv:ManualMappingCuration |
| ror:04fbd2g40 | BioNTech (Germany)     | owl:differentFrom | ror:054q96n74 | AstraZeneca  | semapv:ManualMappingCuration |

```
Ontology(
    Declaration(Class(OBI:0000245))
    Declaration(NamedIndividual(ror:04xfq0f34))
    Declaration(NamedIndividual(VO:0004946))
    Declaration(NamedIndividual(ror:054q96n74))

    ClassAssertion(OBI:0000245 ror:04xfq0f34)
    SameIndividual(ror:04xfq0f34 VO:0004946)
    DifferentIndividuals(ror:04fbd2g40 ror:054q96n74)
)
```

:::: note ::: title Note :::

The semantics of `owl:sameAs` and `owl:differentFrom` are exactly negated,
meaning that this could be extended to incorporate negated semantic mappings.
See the section below on [Negations](#negations) for more information. ::::

## Logical Axioms for Properties

The following semantic mapping predicates are expanded into OWL logical axioms
describing properties. The OWL data model differentiates between object
properties, data properties, and annotation properties. Object and data
properties are part of the logical definition of an entity, whereas annotation
properties are only informative.

This means that the `subject_type` is important in determining the correct
functional OWL expression. When `subject_type` is unavailable, this
implementation assumes that the property is an object property.

| Semantic Mapping Functional    | OWL Expression                    | Subject Type        |
|--------------------------------|-----------------------------------|---------------------|
| `S owl:equivalentProperty O`   | `EquivalentObjectProperties(S O)` | object property     |
| `S owl:equivalentProperty O`   | `EquivalentDataProperties(S O)`   | data property       |
| `S owl:equivalentProperty O`   | does not exist[^1]                | annotation property |
| `S owl:propertyDisjointWith O` | `DisjointObjectProperties(S O)`   | object property     |
| `S owl:propertyDisjointWith O` | `DisjointDataProperties(S O)`     | data property       |
| `S owl:propertyDisjointWith O` | doesn't make sense[^2]            | annotation property |
| `S rdfs:subPropertyOf O`       | `SubObjectPropertyOf(S O)`        | object property     |
| `S rdfs:subPropertyOf O`       | `SubDataPropertyOf(S O)`          | data property       |
| `S rdfs:subPropertyOf O`       | `SubAnnotationPropertyOf(S O)`    | annotation property |
| `S owl:inverseOf O`            | `InverseObjectProperties(S O)`    | object property     |
| `S owl:inverseOf O`            | doesn't make sense[^3]            | data property       |
| `S owl:inverseOf O`            | does not exist[^4]                | annotation property |

Here's an example SSSOM table and accompanying OWL output containing examples
for some semantic mapping predicates.

| subject_id               | subject_label           | subject_type            | predicate_id           | object_id                      | object_label               | mapping_justification        |
|--------------------------|-------------------------|-------------------------|------------------------|--------------------------------|----------------------------|------------------------------|
| RO:0018033               | is deprotonated form of | owl object property     | owl:equivalentProperty | obo:chebi#is_conjugate_base_of | is conjugate base of       | semapv:ManualMappingCuration | 
| RO:0018002               | myristoylates           | owl object property     | rdfs:subPropertyOf     | RO:0002436                     | molecularly interacts with | semapv:ManualMappingCuration |
| oboInOwl:hasBroadSynonym | has broad synonym       | owl annotation property | rdfs:subPropertyOf     | IAO:0000118                    | alternative label          | semapv:ManualMappingCuration |

```
Ontology(
    Declaration(ObjectProperty(RO:0018033))
    Declaration(ObjectProperty(RO:0018002))
    Declaration(ObjectProperty(RO:0002436))
    Declaration(ObjectProperty(obo:chebi#is_conjugate_base_of))
    Declaration(ObjectProperty(oboInOwl:hasBroadSynonym))
    Declaration(ObjectProperty(IAO:0000118 ))

    EquivalentObjectProperties(RO:0018033 obo:chebi#is_conjugate_base_of)
    SubObjectPropertyOf(RO:0018002 RO:0002436)
    SubAnnotationPropertyOf(oboInOwl:hasBroadSynonym IAO:0000118)
)
```

## Bridging

A bridge ontology is an ontology with logical axioms for merging two or more
other ontologies and enabling joint inference and reasoning. This fits neatly
with the notion of transforming SSSOM to OWL, however, bridge ontologies do not
make use of annotation assertions. Therefore, when constructing a bridge
ontology, it is sometimes advantageous to ascribe stronger logical axioms to
weaker semantic mapping predicates like `skos:exactMatch`, `skos:narrowMatch`,
and `skos:broadMatch` that would normally produce annotation assertions.

This behavior is not part of the SSSOM specification, but was pioneered by
[Damien Goutte-Gattat](https://github.com/gouttegd/) in the incorporation of
SSSOM with Ontology Development Kit (ODK) release workflows and briefly
described
[here](https://github.com/INCATools/ontology-development-kit/issues/626#issuecomment-3285032670).
SSSOM Pydantic extends Damien's original idea with additional rules described in
the following table, which are implemented in
`get_upgraded_annotation_property`{.interpreted-text role="func"}.

:::: note ::: title Note :::

In the following table, `class` is shorthand for `rdfs:Class`, `rdfs:Resource`,
`owl:Class`, or `skos:Concept`. ::::

| Semantic Mapping       | Functional OWL Expression         | Subject Type                      |
|------------------------|-----------------------------------|-----------------------------------|
| `S skos:exactMatch O`  | `EquivalentClasses(S O)`          | class or undefined                |
| `S skos:exactMatch O`  | `SameIndividual(S O)`             | `owl:NamedIndividual`             |
| `S skos:exactMatch O`  | `EquivalentObjectProperties(S O)` | `owl:ObjectProperty` or undefined |
| `S skos:exactMatch O`  | `EquivalentDataProperties(S O)`   | `owl:DataProperty`                |
| `S skos:exactMatch O`  | does not exist                    | `owl:AnnotationProperty`          |
| `S skos:broadMatch O`  | `SubClassOf(S O)`                 | class or undefined                |
| `S skos:broadMatch O`  | `ClassAssertion(O, S)`            | `owl:NamedIndividual`             |
| `S skos:broadMatch O`  | `SubObjectPropertyOf(S O)`        | `owl:ObjectProperty` or undefined |
| `S skos:broadMatch O`  | `SubDataPropertyOf(S O)`          | `owl:DataProperty`                |
| `S skos:broadMatch O`  | `SubAnnotationPropertyOf(S O)`    | `owl:AnnotationProperty`          |
| `O skos:narrowMatch S` | `SubClassOf(S O)`                 | class or undefined                |
| `O skos:narrowMatch S` | `ClassAssertion(O, S)`            | `owl:NamedIndividual`             |
| `O skos:narrowMatch S` | `SubObjectPropertyOf(S O)`        | `owl:ObjectProperty` or undefined |
| `O skos:broadMatch S`  | `SubDataPropertyOf(S O)`          | `owl:DataProperty`                |
| `O skos:broadMatch S`  | `SubAnnotationPropertyOf(S O)`    | `owl:AnnotationProperty`          |

:::: warning ::: title Warning :::

The rules between `skos:broadMatch` and `skos:narrowMatch` are complementary,
which is why the `S` and `O` are flipped. In practice, the implementation
requires applying
`sssom_pydantic.process.invert_narrow_matches`{.interpreted-text role="func"} to
flip all narrow matches into broad matches before transforming to OWL. ::::

Adding the `mode="bridge"` parameter to `write_owl()` opts into this upgrading behavior to transform the following SSSOM
into OWL.

| subject_id  | subject_label | predicate_id    | object_id    | object_label | mapping_justification        |
|-------------|---------------|-----------------|--------------|--------------|------------------------------|
| CHEBI:28646 | ammeline      | skos:exactMatch | mesh:C000089 | ammeline     | semapv:ManualMappingCuration |

```
Ontology(
    Declaration(Class(CHEBI:28646))
    Declaration(Class(mesh:C000089))

    EquivalentClasses(CHEBI:28646 mesh:C000089)
)
```

Similarly, the `--mode bridge` option can be passed to the CLI to enable
bridging upgrades.

```console
sssom_pydantic owl --mode bridge -i test.sssom.tsv -o test.ofn
```

## Negations

When constructing a bridge ontology, it is sometimes advantageous to ascribe
stronger logical axioms to weaker semantic mapping mappings that include a
negative predicate modifier in conjunction with predicates such as
`skos:exactMatch`, `skos:narrowMatch`, and `skos:broadMatch` that would normally
produce annotation assertions. For example, `A not exact match B` could be used
to assert `A disjointFrom B`.

However, there are a few major caveats to such ascription.

1.  If another positive mapping such as `A subclass of B` exists, then
    `A not exact match B` is a trivial negative mapping, and should be
    discarded. Otherwise, the production of `A disjointFrom B` would cause an
    unsatisfiability. The
    `sssom_pydantic.process.remove_trivial_negative`{.interpreted-text
    role="func"} identifies and removes trivial negative mappings.
2.  Even the lack of existence of another explicit positive mapping such as
    `A subclass of B` doesn't mean that the positive mapping is true.
    Constructing a logical axiom from a negative mapping can only work if based
    on your curation workflow, you are sure that the existence of a negative
    mapping between `A` and `B` implies that no positive mapping exists.

While these caveats apply to class and property mappings, negative modifiers on
mappings between individuals can be more confidently handled. The negatition of
the `owl:differentFrom` relation always means that they are the same, and the
negation of `owl:sameAs` always means they are different.

The following table describes rules for doing this which are implemented in
`get_implied_negation_axiom`{.interpreted-text role="func"}.


| Semantic Mapping                   | Functional OWL Expression                  | Subject Type                      |
|------------------------------------|--------------------------------------------|-----------------------------------|
| `S not skos:exactMatch O`          | `DisjointClasses(S O)`                     | class or undefined                |
| `S not skos:exactMatch O`          | `DifferentIndividuals(S O)`                | `owl:NamedIndividual`             |
| `S not skos:exactMatch O`          | `DisjointObjectProperties(S O)`            | `owl:ObjectProperty`              |
| `S not skos:exactMatch O`          | `DisjointDataProperties(S O)`              | `owl:DataProperty`                |
| `S not skos:exactMatch O`          | does not exist                             | `owl:AnnotationProperty`          |
| `S not owl:equivalentClass O`      | `DisjointClasses(S O)`                     |                                   |
| `S not owl:disjointWith O`         | `EquivalentClasses(S O)`                   |                                   |
| `S not owl:differentFrom O`        | `SameIndividual(S O)`                      |                                   |
| `S not owl:sameAs O`               | `DifferentIndividuals(S O)`                |                                   |
| `S not owl:equivalentProperty O`   | `DisjointObjectProperties(S O)`            | `owl:ObjectProperty` or undefined |
| `S not owl:equivalentProperty O`   | `DisjointDataProperties(S O)`              | `owl:DataProperty`                |
| `S not owl:equivalentProperty O`   | does not exist                             | `owl:AnnotationProperty`          |
| `S not owl:propertyDisjointWith O` | `EquivalentObjectProperties(S O)`          | `owl:ObjectProperty` or undefined |
| `S not owl:propertyDisjointWith O` | `EquivalentDataProperties(S O)`            | `owl:DataProperty`                |
| `S not owl:propertyDisjointWith O` | does not exist                             | `owl:AnnotationProperty`          |

The following example shows how the negative semantic mapping from the section
[Annotation Properties](#annotation-properties) now produces a
`DisjointClasses()` logical axiom instead of an `AnnotationAssertion()` axiom.
It also reuses the examples from
[Logical Axioms for Named Individuals](#logical-axioms-for-named-individuals)
but flips inverts their predicates.

| subject_id    | subject_label      | predicate_id      | predicate_modifier | object_id     | object_label | mapping_justification            |
|---------------|--------------------|-------------------|--------------------|---------------|--------------|----------------------------------|
| CHEBI:10057   | 9H-xanthene        | skos:exactMatch   | Not                | mesh:C002563  | xanthan      | gum semapv:ManualMappingCuration |
| ror:04fbd2g40 | BioNTech (Germany) | owl:differentFrom | Not                | VO:0004946    | BioNTech     | semapv:ManualMappingCuration     |
| ror:04fbd2g40 | BioNTech (Germany) | owl:sameAs        | Not                | ror:054q96n74 | AstraZeneca  | semapv:ManualMappingCuration     |

```
Ontology(
    Declaration(Class(CHEBI:10057))
    Declaration(Class(mesh:C002563))
    Declaration(NamedIndividual(ror:04fbd2g40))
    Declaration(NamedIndividual(ror:054q96n74))
    Declaration(NamedIndividual(VO:0004946))

    DisjointClasses(CHEBI:10057 mesh:C002563)
    SameIndividual(ror:04xfq0f34 VO:0004946)
    DifferentIndividuals(ror:04fbd2g40 ror:054q96n74)
)
```

The `--negation-workflow` option can be passed to the CLI to enable this
workflow when in bridge mode.

```console
sssom_pydantic owl --mode bridge --negation-workflow -i test.sssom.tsv -o test.ofn
```

[^1]:
    This seems like an oversight, because stating that two annotation properties
    are interchangable (e.g., `dce:creator` and `dcterms:creator`) is important

[^2]:
    Because the `owl:propertyDisjointWith` is interpreted in a logical way, it
    doesn't make sense for OWL to have a corresponding functional OWL expression
    for annotation properties.

[^3]:
    Literals don't appear as subjects in triples in OWL, so having an inverse
    for a data property doesn't make sense

[^4]:
    Annotation properties can meaningfully be inverted if their range isn't a
    literal, so this seems like an oversight. OWL probably didn't include this
    since it's only informative and not part of a logical definition of an
    entity.
