---
layout: post
title: "Semantic Mapping Review Workflows"
date: 2026-08-27 11:00:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - review
---

A flowchart.

```mermaid
flowchart TD
    Start[[Generation of Mappings]]
    Manual[Manual Curation]
    Automated[Automated Production]
    Final[Confidence Assessment]
    Start -->|via manual curation| Manual
    Start -->|via automated methods| Automated
    Manual --> M1[M1: Add reviewer] --> Final
    Manual --> M2[M2: Replace with manual curation] --> Final
    Manual --> M3[M3: Curator Consensus] --> Final
    M2 -.-> M1
    M3 -.-> M1
    Automated --> A1[A1: Add reviewer] --> Final
    Automated --> A2[A2: Replace with manual curation] --> Final
    A2 -.-> M1
```

[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/).

The following SSSOM omits the metadata - standard
[Semantic Farm](https://semantic.farm/) prefixes should be assumed (previously
called Bioregistry).

The following SSSOM contains two mappings between the
[Monarch Disease Ontology (MONDO)](https://semantic.farm/mondo) - one that was
produced through [SSSOM Curator's](https://github.com/cthoyt/sssom-curator)
lexical matching workflow, and one that was manually curated.

The way the mappings were captured is reflected in the `mapping_justification`
field via [Semantic Mapping Vocabulary (SEMAPV)](https://semantic.farm/semapv)
terms - the lexical matching gets
[semapv:LexicalMatching](https://semantic.farm/semapv:LexicalMatching) and the
manual curation gets
[semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration).

The kind of mapping also strongly suggests what metadata gets added to the
mapping. The lexical mapping has information about the mapping tool (and could
additionally include fields like
[subject_match_field](https://w3id.org/sssom/subject_match_field),
[object_match_field](https://w3id.org/sssom/object_match_field), and
[match_string](https://w3id.org/sssom/match_string)). Importantly, the manual
curation contains an `author_id` for the individual who did the curation. Both
kinds of mappings include a [confidence](https://w3id.org/sssom/confidence),
which allows either the mapping tool or the curator to self-report the
confidence in the mapping's correctness.

| record_id | subject_id                                           | subject_label         | predicate_id                                             | object_id                                    | object_label          | mapping_justification                                                       | author_id                                                                    | mapping_tool  | mapping_tool_id                                                  | mapping_tool_version | confidence |
| --------- | ---------------------------------------------------- | --------------------- | -------------------------------------------------------- | -------------------------------------------- | --------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------- | -------------------- | ---------- |
| ex:1      | [MONDO:0005641](https://semantic.farm/MONDO:0005641) | aleutian mink disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:2934](https://semantic.farm/DOID:2934) | aleutian mink disease | [semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration) | [orcid:0000-0003-4423-4370](https://semantic.farm/orcid:0000-0003-4423-4370) |               |                                                                  |                      | 0.99       |
| ex:2      | [MONDO:0005676](https://semantic.farm/MONDO:0005676) | borna disease         | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:5154](https://semantic.farm/DOID:5154) | borna disease         | [semapv:LexicalMatching](https://semantic.farm/semapv:LexicalMatching)      |                                                                              | SSSOM Curator | [wikidata:Q138902949](https://semantic.farm/wikidata:Q138902949) | 0.6.3                | 0.778      |

## M1: Reviewing a Manually Curated Mapping

The most obvious review workflow for manually curated semantic mappings is for a
second curator (the reviewer) to decide if they agree, disagree, or are unsure
about the correctness of the manually curated semantic mapping. The reviewer
then adds their ORCiD into the `reviewer_id` column and their level of agreement
in the [reviewer_agreement](https://w3id.org/sssom/reviewer_agreement) column,
in which $+1.0$ means full agreement, $0.0$ means ambivalence, and $-1.0$ means
full disagreement. The reviewer can optionally add the date of review in the
[ `review_date`](https://w3id.org/sssom/review_date) column to support
historical analyses, e.g., that help understand the lifecycles of mappings.

The following example illustrates what it would look like if Nicole Vasilevsky
(one of the primary maintainers of MONDO) positively reviewed the manually
curated mapping between the MONDO and DOID terms for _aleutian mink disease_
from `ex:1`. Scroll to the right to see the `reviewer_id` and
`reviewer_agreement` columns, which appear in the order prescribed by the
[TSV serialization](https://mapping-commons.github.io/sssom/dev/spec-formats-tsv/)
section of the SSSOM Specification.

| record_id | subject_id                                           | subject_label         | predicate_id                                             | object_id                                    | object_label          | mapping_justification                                                       | author_id                                                                    | confidence | reviewer_id                                                                  | reviewer_agreement |
| --------- | ---------------------------------------------------- | --------------------- | -------------------------------------------------------- | -------------------------------------------- | --------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------- | ------------------ |
| ex:3      | [MONDO:0005641](https://semantic.farm/MONDO:0005641) | aleutian mink disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:2934](https://semantic.farm/DOID:2934) | aleutian mink disease | [semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration) | [orcid:0000-0003-4423-4370](https://semantic.farm/orcid:0000-0003-4423-4370) | 0.99       | [orcid:0000-0001-5208-3432](https://semantic.farm/orcid:0000-0001-5208-3432) | 1.0                |

> [!WARNING]
>
> Note that this review workflow is _destructive_ - it alters the identity of
> the semantic mapping record (i.e., a row in the SSSOM file). Importantly, this
> means that the semantic mapping record's
> [hash](https://mapping-commons.github.io/sssom/dev/spec-support-hashing/)
> changes. This is an important implementation detail depending on how you or
> your semantic mapping review software persists its semantic mappings.

## M2: Replacing a Manually Curated Mapping

This M1 review workflow has the disadvantage that when the reviewer disagrees,
it does not materialize a new semantic mapping with the correct `predicate_id`
and `predicate_modifier`.

For example, if the originally curated mapping had `skos:exactMatch` and no
predicate modifier, but the reviewer decided it was incorrect because they are
not an exact match, then they might either want to materialize a new mapping
with the predicate `skos:exactMatch` and the `Not` predicate modifier, or they
might be able to choose a different SKOS mapping predicate that is more correct
(e.g., broad, narrow, close, or related).

## M3: Achieving Curator Consensus

the second semantic mapping review workflow is to have a second (or more)
curators manually curate the same mapping in isolation, then to compare the
results.

the curator consensus workflow can also feed into the review workflow, as each
mapping can be reviewed separately.

| subject_id                                           | subject_label         | predicate_id                                             | object_id                                    | object_label          | mapping_justification                                                       | author_id                                                                    | confidence |
| ---------------------------------------------------- | --------------------- | -------------------------------------------------------- | -------------------------------------------- | --------------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| [MONDO:0005641](https://semantic.farm/MONDO:0005641) | aleutian mink disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:2934](https://semantic.farm/DOID:2934) | aleutian mink disease | [semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration) | [orcid:0000-0003-4423-4370](https://semantic.farm/orcid:0000-0003-4423-4370) | 0.99       |
| [MONDO:0005641](https://semantic.farm/MONDO:0005641) | aleutian mink disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:2934](https://semantic.farm/DOID:2934) | aleutian mink disease | [semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration) | [orcid:0000-0003-1307-2508](https://semantic.farm/orcid:0000-0003-1307-2508) | 0.98       |

Warning: this workflow is _idempotent_, meaning that the identity of the
original record does _not_ change.

## A1: Reviewing a Predicted Mapping

this workflow is effectively equivalent to M1, in which a reviewer of a
predicted mapping adds their review into the `reviewer_id` slot. The
disadvantage of this workflow in the situation that the reviewer is highly
confident in the correctness of the manual curation, that it doesn't explicitly
capture this in the mapping justification. This motivates the next workflow

| subject_id                                           | subject_label | predicate_id                                             | object_id                                    | object_label  | mapping_justification                                                  | mapping_tool  | mapping_tool_id                                                  | mapping_tool_version | confidence | reviewer_id                                                                  | reviewer_agreement |
| ---------------------------------------------------- | ------------- | -------------------------------------------------------- | -------------------------------------------- | ------------- | ---------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------- | -------------------- | ---------- | ---------------------------------------------------------------------------- | ------------------ |
| [MONDO:0005676](https://semantic.farm/MONDO:0005676) | borna disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:5154](https://semantic.farm/DOID:5154) | borna disease | [semapv:LexicalMatching](https://semantic.farm/semapv:LexicalMatching) | SSSOM Curator | [wikidata:Q138902949](https://semantic.farm/wikidata:Q138902949) | 0.6.3                | 0.778      | [orcid:0000-0001-5208-3432](https://semantic.farm/orcid:0000-0001-5208-3432) | 1.0                |

## A2.1: Replacing a Predicted Mapping with a Manual Curation

In the case where the author is sure about their review, then the mapping can be
overwritten with a manual curation. Then, the mapping tool and lexical
prediction metadata are dropped, the `author_id` is filled out, and the
`confidence` is overwritten with the curator's confidence.

| subject_id                                           | subject_label | predicate_id                                             | object_id                                    | object_label  | mapping_justification                                                  | author_id                                                                    | confidence |
| ---------------------------------------------------- | ------------- | -------------------------------------------------------- | -------------------------------------------- | ------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------- |
| [MONDO:0005676](https://semantic.farm/MONDO:0005676) | borna disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:5154](https://semantic.farm/DOID:5154) | borna disease | [semapv:LexicalMatching](https://semantic.farm/semapv:LexicalMatching) | [orcid:0000-0001-5208-3432](https://semantic.farm/orcid:0000-0001-5208-3432) | 1.0        |

TODO: give example of disagreement and of ambivalence

## A2.2 Replacing a Predicted Mapping with a Manual Curation (with full provenance)

If full provenance is desired, then the original mapping can be retained, and
the curated mapping can use the
[derived_from](https://w3id.org/sssom/derived_from) field to point back to
original predicted mapping record via the
[SSSOM record hash](https://mapping-commons.github.io/sssom/spec-support-hashing/).
This is implemented in SSSOM Pydantic (note, the example hash is made up).

| subject_id                                           | subject_label | predicate_id                                             | object_id                                    | object_label  | mapping_justification                                                       | author_id                                                                    | mapping_tool  | mapping_tool_id                                                  | mapping_tool_version | confidence | derived_from        |
| ---------------------------------------------------- | ------------- | -------------------------------------------------------- | -------------------------------------------- | ------------- | --------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------- | ---------------------------------------------------------------- | -------------------- | ---------- | ------------------- |
| [MONDO:0005676](https://semantic.farm/MONDO:0005676) | borna disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:5154](https://semantic.farm/DOID:5154) | borna disease | [semapv:ManualMappingCuration](https://semantic.farm/ManualMappingCuration) | [orcid:0000-0003-4423-4370](https://semantic.farm/orcid:0000-0003-4423-4370) |               |                                                                  |                      | 0.99       | `mapping:CED101AFD` |
| [MONDO:0005676](https://semantic.farm/MONDO:0005676) | borna disease | [skos:exactMatch](https://semantic.farm/skos:exactMatch) | [DOID:5154](https://semantic.farm/DOID:5154) | borna disease | [semapv:LexicalMatching](https://semantic.farm/semapv:LexicalMatching)      |                                                                              | SSSOM Curator | [wikidata:Q138902949](https://semantic.farm/wikidata:Q138902949) | 0.6.3                | 0.778      |                     |

## on LLMs

I don't consider machine-assisted review to be review, but rather a different
form of prediction.

[MapperGPT: large language models for linking and mapping entities](https://arxiv.org/abs/2310.03666)
from Nico Matentzoglu, _et al._ (2023)

The usage of a machine for review is simply not accomplishing the goal, which is
to increase the confidence
