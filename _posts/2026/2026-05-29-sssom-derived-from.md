---
layout: post
title: Linking Derived Records in SSSOM
date: 2026-05-29 15:51:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
---




https://github.com/biopragmatics/semra




Updates to SSSOM

- https://github.com/mapping-commons/sssom/issues/537
- https://github.com/mapping-commons/sssom/pull/548

Updates to SSSOM Pydantic

- https://github.com/cthoyt/sssom-pydantic/pull/108 implemented `derived_from`
- https://github.com/cthoyt/sssom-pydantic/pull/129 added mermaid visualization

# Inference

There are several mechanisms for inference:

- Inference via chaining (see [chaining rules](chaining-rules.md)), which should
  be tagged with `semapv:MappingChaining` as a justification
- Inference via mapping inversion, which should be tagged with
  `semapv:MappingInversion` as a justification
- Inference via prior knowledge, which should be tagged with
  `semapv:BackgroundKnowledgeBasedMatching` as a justification

## Background on Mapping Triples, Quadruples, and Records

This section provides a brief background on different ways of referencing a
mapping appearing in SSSOM.

A mapping triple has a subject, predicate, and object as in (`mesh:C000089`,
`skos:exactMatch`, `CHEBI:28646`). A mapping triple does not clarify the
judgment on whether a triple is true or false, nor how the mapping was created.

A mapping quadruple has a subject, predicate, object, and predicate modifier.
The addition of the predicate modifier allows a mapping quadruple to explicitly
denote the judgment on whether a triple is true or false. For example,
(`mesh:C000089`, `skos:exactMatch`, `CHEBI:28646`, True) explicitly represents
that the above subject, predicate, object triple is true, while (`CHEBI:10057`,
`skos:exactMatch`, `mesh:C002563`, False) is false because `CHEBI:10057` refers
to 9H-xanthene, a small molecule, and `mesh:C002563` refers to xanthan gum, a
polysaccharide. By convention, mapping triples are implicitly considered to
refer to the "true" mapping quadruple.

A mapping record refers to the subject, predicate, object, predicate modifier,
and all other fields in the SSSOM data model (except where otherwise stated in
["Hashing a SSSOM mapping record"](spec-support-hashing.md), such as the
`record_id`).

## Referring to Evidence

The `derived_from` field was introduced in
[#537](https://github.com/mapping-commons/sssom/issues/537) in order to
reference the original subject-predicate-object-predicate modifier quadruple
from which new mappings are inferred/derived.

The following example demonstrates how the `derived_from` field can be leveraged
in two scenarios:

1. mapping chaining. The table contains a SKOS exact match from `mesh:C000089`
   to `CHEBI:28646` and from `CHEBI:28646` to `cas:645-92-1`. The third row of
   the table contains a SKOS exact match from `mesh:C000089` to `cas:645-92-1`
   produced through mapping chaining. The `derived_from` column in this row
   contains CURIEs referring to the
   `mesh:C000089`-`skos:exactMatch`-`CHEBI:28646`-True and
   `CHEBI:28646`-`skos:exactMatch`-`cas:645-92-1`-True mapping quadruples,
   concatenated with a pipe
2. mapping inversion. The fourth row of the table contains a SKOS exact match
   from `CHEBI:28646` to `mesh:C000089` produced through mapping inversion of
   the first row of the table. The `derived_from` column in this row contains
   the CURIE referring to the
   `mesh:C000089`-`skos:exactMatch`-`CHEBI:28646`-True quad.

```
# curie_map:
#   cas:  	https://commonchemistry.cas.org/detail?cas_rn=
#   CHEBI: http://purl.obolibrary.org/obo/CHEBI_
#   mesh: http://id.nlm.nih.gov/mesh/
#   orcid: https://orcid.org/
#   semapv: https://w3id.org/semapv/vocab/
#   skos: http://www.w3.org/2004/02/skos/core#
#   mapping: https://example.com/mapping/
# license: https://creativecommons.org/publicdomain/zero/1.0/
# mapping_set_id: https://github.com/mapping-commons/sssom/blob/master/examples/schema/derived_from.sssom.tsv
# creator_id:
#  - orcid:0000-0003-4423-4370
```

| subject_id   | subject_label | predicate_id    | object_id    | object_label | mapping_justification        | derived_from                                                                                                                                       | comment                                                                                                |
| ------------ | ------------- | --------------- | ------------ | ------------ | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| mesh:C000089 | ammeline      | skos:exactMatch | CHEBI:28646  | ammeline     | semapv:ManualMappingCuration |                                                                                                                                                    |                                                                                                        |
| CHEBI:28646  | ammeline      | skos:exactMatch | cas:645-92-1 | Ammeline     | semapv:ManualMappingCuration |                                                                                                                                                    |                                                                                                        |
| mesh:C000089 | ammeline      | skos:exactMatch | cas:645-92-1 | Ammeline     | semapv:MappingChaining       | mapping:36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a\|mapping:bb768f0b1e1643298f4df1a381001f6ed68fcc8fff49b371f0235b51dbab9e1e | this example needs to refer to the first two mappings in this table by mapping sameness identifier     |
| CHEBI:28646  | ammeline      | skos:exactMatch | mesh:C000089 | Ammeline     | semapv:MappingInversion      | mapping:36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a                                                                           | this example just needs to refer to the first mapping in this table by the mapping sameness identifier |

For the purposes of inference, the mapping quadruple should be used:

1. Mapping triples are insufficient: without the judgment of whether a mapping
   is true or false, then an algorithm could accidentally conclude from
   `A skos:exactMatch B` and `B (not) skos:exactMatch C` that
   `A skos:exactMatch C`. This is why mapping triples are insufficient
2. Full mapping records are inflexible: the SSSOM data should be flexible so if
   additional evidence (i.e., records) for a given mapping quadruple are found,
   then the confidence in the inferred/derived mapping (e.g., chained or
   inverted) can be adjusted accordingly. This is possible because most chaining
   and inversion algorithms logically operate on mapping quadruples, and not on
   records.

Note: the local unique identifiers used for mappings in this example are related
to the proposal in https://github.com/ts4nfdi/mapping-sameness-identifier (which
currently is under review). For now, the SSSOM specification isn't prescribing
how to assign identifiers to mapping quadruples.

## Chaining

The following

| subject_id   | subject_label         | predicate_id    | object_id    | object_label           | mapping_justification        | author_id                 | mapping_source      | derived_from                                                                                                                                      |
|:-------------|:----------------------|:----------------|:-------------|:-----------------------|:-----------------------------|:--------------------------|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|
| BTO:0006078  | pluripotent stem cell | skos:exactMatch | CL:0002248   | pluripotent stem cell  | semapv:ManualMappingCuration | orcid:0000-0003-4423-4370 | wikidata:Q111239110 |                                                                                                                                                |
| CL:0002248   | pluripotent stem cell | skos:exactMatch | mesh:D039904 | pluripotent stem cells | semapv:ManualMappingCuration | orcid:0000-0003-4423-4370 | wikidata:Q111239110 |                                                                                                                                                |
| BTO:0006078  | pluripotent stem cell | skos:exactMatch | mesh:D039904 | pluripotent stem cells | semapv:MappingChaining       |                        |                  | mapping:8a12a396b85642cccfc799fb24320c51a4aabf3294780cb31116d45f773a2572|mapping:988ce14e26fdbf24aeb27b4d8b5ad4bcc25b5cdb46be4e674bfa88a2abe12264 |

```mermaid
flowchart LR
  BTO:0006078[pluripotent stem cell
BTO:0006078]
  CL:0002248[pluripotent stem cell
CL:0002248]
  EEB83E3B60649C0E("BTO:0006078
skos:exactMatch
CL:0002248
manual curation")
  style EEB83E3B60649C0E fill:#bbf
  orcid:0000-0003-4423-4370[Charles Tapley Hoyt
orcid:0000-0003-4423-4370]
  style orcid:0000-0003-4423-4370 fill:#bef
  wikidata:Q111239110[Biomappings
wikidata:Q111239110]
  style wikidata:Q111239110 fill:#feb
  8a12a396b85642cccfc799fb24320c51a4aabf3294780cb31116d45f773a2572[["BTO:0006078
skos:exactMatch
CL:0002248"]]
  style 8a12a396b85642cccfc799fb24320c51a4aabf3294780cb31116d45f773a2572 fill:#f9f
  mesh:D039904[pluripotent stem cells
mesh:D039904]
  CD2204936C2DDC93("CL:0002248
skos:exactMatch
mesh:D039904
manual curation")
  style CD2204936C2DDC93 fill:#bbf
  988ce14e26fdbf24aeb27b4d8b5ad4bcc25b5cdb46be4e674bfa88a2abe12264[["CL:0002248
skos:exactMatch
mesh:D039904"]]
  style 988ce14e26fdbf24aeb27b4d8b5ad4bcc25b5cdb46be4e674bfa88a2abe12264 fill:#f9f
  AC5F57BF466F5641("BTO:0006078
skos:exactMatch
mesh:D039904
chaining")
  style AC5F57BF466F5641 fill:#bbf
  0d2804dff03667d435d38f61e97cd8435382ad45104c6be460f9aa318e0a4622[["BTO:0006078
skos:exactMatch
mesh:D039904"]]
  style 0d2804dff03667d435d38f61e97cd8435382ad45104c6be460f9aa318e0a4622 fill:#f9f
  EEB83E3B60649C0E-->|has author|orcid:0000-0003-4423-4370
  EEB83E3B60649C0E-->|source|wikidata:Q111239110
  BTO:0006078-->|subject of|EEB83E3B60649C0E
  CL:0002248-->|object of|EEB83E3B60649C0E
  8a12a396b85642cccfc799fb24320c51a4aabf3294780cb31116d45f773a2572-->|has evidence|EEB83E3B60649C0E
  CD2204936C2DDC93-->|has author|orcid:0000-0003-4423-4370
  CD2204936C2DDC93-->|source|wikidata:Q111239110
  CL:0002248-->|subject of|CD2204936C2DDC93
  mesh:D039904-->|object of|CD2204936C2DDC93
  988ce14e26fdbf24aeb27b4d8b5ad4bcc25b5cdb46be4e674bfa88a2abe12264-->|has evidence|CD2204936C2DDC93
  BTO:0006078-->|subject of|AC5F57BF466F5641
  mesh:D039904-->|object of|AC5F57BF466F5641
  0d2804dff03667d435d38f61e97cd8435382ad45104c6be460f9aa318e0a4622-->|has evidence|AC5F57BF466F5641
  AC5F57BF466F5641-->|derived from|8a12a396b85642cccfc799fb24320c51a4aabf3294780cb31116d45f773a2572
  AC5F57BF466F5641-->|derived from|988ce14e26fdbf24aeb27b4d8b5ad4bcc25b5cdb46be4e674bfa88a2abe12264
```

## Chaining with Negatives

| subject_id   | subject_label   | predicate_id    | predicate_modifier   | object_id    | object_label   | mapping_justification        | author_id                 | mapping_source      | derived_from                                                                                                                                       |
|:-------------|:----------------|:----------------|:---------------------|:-------------|:---------------|:-----------------------------|:--------------------------|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------|
| chebi:10057  | 9H-xanthene     | skos:exactMatch | Not                  | mesh:C002563 | xanthan gum    | semapv:ManualMappingCuration | orcid:0000-0003-4423-4370 | wikidata:Q111239110 |                                                                                                                                                 |
| cas:92-83-1  | Xanthene        | skos:exactMatch |                   | chebi:10057  | 9H-xanthene    | semapv:ManualMappingCuration | orcid:0000-0003-4423-4370 | wikidata:Q111239110 |                                                                                                                                                 |
| cas:92-83-1  | Xanthene        | skos:exactMatch | Not                  | mesh:C002563 | xanthan gum    | semapv:MappingChaining       |                        |                  | mapping:58f24ccfaf71431276da873c9e7b77ea61a2425e4e8b283b943542290deb292b~|mapping:bb1162fb2afb1c519c0aa8be98c352061720af220e2d052c571a1fecabff9800 |

```mermaid
flowchart LR
  chebi:10057[9H-xanthene
chebi:10057]
  mesh:C002563[xanthan gum
mesh:C002563]
  462D9D4128330C63("chebi:10057
not skos:exactMatch
mesh:C002563
manual curation")
  style 462D9D4128330C63 fill:#bbf
  orcid:0000-0003-4423-4370[Charles Tapley Hoyt
orcid:0000-0003-4423-4370]
  style orcid:0000-0003-4423-4370 fill:#bef
  wikidata:Q111239110[Biomappings
wikidata:Q111239110]
  style wikidata:Q111239110 fill:#feb
  58f24ccfaf71431276da873c9e7b77ea61a2425e4e8b283b943542290deb292bN[["chebi:10057
not skos:exactMatch
mesh:C002563"]]
  style 58f24ccfaf71431276da873c9e7b77ea61a2425e4e8b283b943542290deb292bN fill:#f9f
  cas:92-83-1[Xanthene
cas:92-83-1]
  190EA9377428B4CB("cas:92-83-1
skos:exactMatch
chebi:10057
manual curation")
  style 190EA9377428B4CB fill:#bbf
  bb1162fb2afb1c519c0aa8be98c352061720af220e2d052c571a1fecabff9800[["cas:92-83-1
skos:exactMatch
chebi:10057"]]
  style bb1162fb2afb1c519c0aa8be98c352061720af220e2d052c571a1fecabff9800 fill:#f9f
  25AC613A93F7EF14("cas:92-83-1
not skos:exactMatch
mesh:C002563
chaining")
  style 25AC613A93F7EF14 fill:#bbf
  84238c3cc875f0939ee4a8cf76bf33f216784434756833e3ba8d1b1183c372f5N[["cas:92-83-1
not skos:exactMatch
mesh:C002563"]]
  style 84238c3cc875f0939ee4a8cf76bf33f216784434756833e3ba8d1b1183c372f5N fill:#f9f
  462D9D4128330C63-->|has author|orcid:0000-0003-4423-4370
  462D9D4128330C63-->|source|wikidata:Q111239110
  chebi:10057-->|subject of|462D9D4128330C63
  mesh:C002563-->|object of|462D9D4128330C63
  58f24ccfaf71431276da873c9e7b77ea61a2425e4e8b283b943542290deb292bN-->|has evidence|462D9D4128330C63
  190EA9377428B4CB-->|has author|orcid:0000-0003-4423-4370
  190EA9377428B4CB-->|source|wikidata:Q111239110
  cas:92-83-1-->|subject of|190EA9377428B4CB
  chebi:10057-->|object of|190EA9377428B4CB
  bb1162fb2afb1c519c0aa8be98c352061720af220e2d052c571a1fecabff9800-->|has evidence|190EA9377428B4CB
  cas:92-83-1-->|subject of|25AC613A93F7EF14
  mesh:C002563-->|object of|25AC613A93F7EF14
  84238c3cc875f0939ee4a8cf76bf33f216784434756833e3ba8d1b1183c372f5N-->|has evidence|25AC613A93F7EF14
  25AC613A93F7EF14-->|derived from|58f24ccfaf71431276da873c9e7b77ea61a2425e4e8b283b943542290deb292bN
  25AC613A93F7EF14-->|derived from|bb1162fb2afb1c519c0aa8be98c352061720af220e2d052c571a1fecabff9800
```

## Inversion

| subject_id   | subject_label   | predicate_id    | object_id    | object_label   | mapping_justification        | author_id                 | mapping_source      | derived_from                                                             |
|:-------------|:----------------|:----------------|:-------------|:---------------|:-----------------------------|:--------------------------|:--------------------|:-------------------------------------------------------------------------|
| mesh:C000089 | ammeline        | skos:exactMatch | chebi:28646  | ammeline       | semapv:ManualMappingCuration | orcid:0000-0003-4423-4370 | wikidata:Q111239110 |                                                                       |
| chebi:28646  | ammeline        | skos:exactMatch | mesh:C000089 | ammeline       | semapv:MappingInversion      |                        |                  | mapping:36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a |

```mermaid
flowchart LR
  mesh:C000089[ammeline
mesh:C000089]
  chebi:28646[ammeline
chebi:28646]
  1181E81AD58C1B94("mesh:C000089
skos:exactMatch
chebi:28646
manual curation")
  style 1181E81AD58C1B94 fill:#bbf
  orcid:0000-0003-4423-4370[Charles Tapley Hoyt
orcid:0000-0003-4423-4370]
  style orcid:0000-0003-4423-4370 fill:#bef
  wikidata:Q111239110[Biomappings
wikidata:Q111239110]
  style wikidata:Q111239110 fill:#feb
  36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a[["mesh:C000089
skos:exactMatch
chebi:28646"]]
  style 36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a fill:#f9f
  54D1553627DC5514("chebi:28646
skos:exactMatch
mesh:C000089
inversion")
  style 54D1553627DC5514 fill:#bbf
  faeefc6d1dd08238a9732de5a3c9dcf99388e62fa8b1caaf9ba28c7eaf6d483a[["chebi:28646
skos:exactMatch
mesh:C000089"]]
  style faeefc6d1dd08238a9732de5a3c9dcf99388e62fa8b1caaf9ba28c7eaf6d483a fill:#f9f
  1181E81AD58C1B94-->|has author|orcid:0000-0003-4423-4370
  1181E81AD58C1B94-->|source|wikidata:Q111239110
  mesh:C000089-->|subject of|1181E81AD58C1B94
  chebi:28646-->|object of|1181E81AD58C1B94
  36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a-->|has evidence|1181E81AD58C1B94
  chebi:28646-->|subject of|54D1553627DC5514
  mesh:C000089-->|object of|54D1553627DC5514
  faeefc6d1dd08238a9732de5a3c9dcf99388e62fa8b1caaf9ba28c7eaf6d483a-->|has evidence|54D1553627DC5514
  54D1553627DC5514-->|derived from|36a1f9244ea7641a90987c82f33c25c0c13712ee8f48207b2a0825f8a4e4e26a
```

## Background Knowledge

| subject_id   | subject_label   | predicate_id       | predicate_label              | object_id   | object_label   | mapping_justification                   | mapping_source   | derived_from                                                             |
|:-------------|:----------------|:-------------------|:-----------------------------|:------------|:---------------|:----------------------------------------|:-----------------|:-------------------------------------------------------------------------|
| chebi:10057  | 9H-xanthene     | oboInOwl:hasDbXref | has database cross-reference | cas:92-83-1 | Xanthene       | semapv:UnspecifiedMatching              | obo:chebi        |                                                                       |
| chebi:10057  | 9H-xanthene     | skos:exactMatch    |                           | cas:92-83-1 | Xanthene       | semapv:BackgroundKnowledgeBasedMatching |               | mapping:887c2cc0c006b49df5fa0bc281e23bd3722880d5096e27218082bd6edf96f59e |

```mermaid
flowchart LR
  chebi:10057[9H-xanthene
chebi:10057]
  cas:92-83-1[Xanthene
cas:92-83-1]
  964DD2FDA95501A2("chebi:10057
oboInOwl:hasDbXref
cas:92-83-1
unspecified")
  style 964DD2FDA95501A2 fill:#bbf
  obo:chebi[ChEBI Ontology
obo:chebi]
  style obo:chebi fill:#feb
  887c2cc0c006b49df5fa0bc281e23bd3722880d5096e27218082bd6edf96f59e[["chebi:10057
oboInOwl:hasDbXref
cas:92-83-1"]]
  style 887c2cc0c006b49df5fa0bc281e23bd3722880d5096e27218082bd6edf96f59e fill:#f9f
  B5CF0F3AB755AC6D("chebi:10057
skos:exactMatch
cas:92-83-1
background know.")
  style B5CF0F3AB755AC6D fill:#bbf
  e61f33dbb925f2282823afdad56c24feee9875953ea2de9124a50e47bd63418a[["chebi:10057
skos:exactMatch
cas:92-83-1"]]
  style e61f33dbb925f2282823afdad56c24feee9875953ea2de9124a50e47bd63418a fill:#f9f
  964DD2FDA95501A2-->|source|obo:chebi
  chebi:10057-->|subject of|964DD2FDA95501A2
  cas:92-83-1-->|object of|964DD2FDA95501A2
  887c2cc0c006b49df5fa0bc281e23bd3722880d5096e27218082bd6edf96f59e-->|has evidence|964DD2FDA95501A2
  chebi:10057-->|subject of|B5CF0F3AB755AC6D
  cas:92-83-1-->|object of|B5CF0F3AB755AC6D
  e61f33dbb925f2282823afdad56c24feee9875953ea2de9124a50e47bd63418a-->|has evidence|B5CF0F3AB755AC6D
  B5CF0F3AB755AC6D-->|derived from|887c2cc0c006b49df5fa0bc281e23bd3722880d5096e27218082bd6edf96f59e
```

## End-to-End Inference

| subject_id   | subject_label      | predicate_id       | predicate_label              | object_id      | object_label       | mapping_justification                   | mapping_source      | derived_from                                                                                                                                      | author_id                 |
|:-------------|:-------------------|:-------------------|:-----------------------------|:---------------|:-------------------|:----------------------------------------|:--------------------|:--------------------------------------------------------------------------------------------------------------------------------------------------|:--------------------------|
| chebi:133530 | tyramine sulfate   | oboInOwl:hasDbXref | has database cross-reference | cas:30223-92-8 | Tyramine sulfate   | semapv:UnspecifiedMatching              | obo:chebi           |                                                                                                                                                |                        |
| chebi:133530 | tyramine sulfate   | skos:exactMatch    |                           | cas:30223-92-8 | Tyramine sulfate   | semapv:BackgroundKnowledgeBasedMatching |                  | mapping:0b8eb968c306d65e1715a7b0961f6a4d99b5b19081edb67cee701fd887af1290                                                                          |                        |
| chebi:133530 | tyramine sulfate   | skos:exactMatch    |                           | mesh:C027957   | tyramine O-sulfate | semapv:ManualMappingCuration            | wikidata:Q111239110 |                                                                                                                                                | orcid:0000-0003-4423-4370 |
| mesh:C027957 | tyramine O-sulfate | skos:exactMatch    |                           | chebi:133530   | tyramine sulfate   | semapv:MappingInversion                 |                  | mapping:b8d737b89a421bd6ca058314564c9ed507cbfe3ec4a2e82979fefdfe708019ea                                                                          |                        |
| mesh:C027957 | tyramine O-sulfate | skos:exactMatch    |                           | cas:30223-92-8 | Tyramine sulfate   | semapv:MappingChaining                  |                  | mapping:a0022401f47964288ecc1ab706d79b4d4abc10edf33d0a71953834a0b0b3c24c|mapping:1036c55358639c5db78ada181ac38d8eda337e83efe1db901716d101777f8474 |                        |

```mermaid
flowchart LR
  chebi:133530[tyramine sulfate
chebi:133530]
  cas:30223-92-8[Tyramine sulfate
cas:30223-92-8]
  983062C7B8D6517E("chebi:133530
oboInOwl:hasDbXref
cas:30223-92-8
unspecified")
  style 983062C7B8D6517E fill:#bbf
  obo:chebi[ChEBI Ontology
obo:chebi]
  style obo:chebi fill:#feb
  0b8eb968c306d65e1715a7b0961f6a4d99b5b19081edb67cee701fd887af1290[["chebi:133530
oboInOwl:hasDbXref
cas:30223-92-8"]]
  style 0b8eb968c306d65e1715a7b0961f6a4d99b5b19081edb67cee701fd887af1290 fill:#f9f
  21056C0956788E11("chebi:133530
skos:exactMatch
cas:30223-92-8
background know.")
  style 21056C0956788E11 fill:#bbf
  a0022401f47964288ecc1ab706d79b4d4abc10edf33d0a71953834a0b0b3c24c[["chebi:133530
skos:exactMatch
cas:30223-92-8"]]
  style a0022401f47964288ecc1ab706d79b4d4abc10edf33d0a71953834a0b0b3c24c fill:#f9f
  mesh:C027957[tyramine O-sulfate
mesh:C027957]
  244808D78AFCBDC1("chebi:133530
skos:exactMatch
mesh:C027957
manual curation")
  style 244808D78AFCBDC1 fill:#bbf
  orcid:0000-0003-4423-4370[Charles Tapley Hoyt
orcid:0000-0003-4423-4370]
  style orcid:0000-0003-4423-4370 fill:#bef
  wikidata:Q111239110[Biomappings
wikidata:Q111239110]
  style wikidata:Q111239110 fill:#feb
  b8d737b89a421bd6ca058314564c9ed507cbfe3ec4a2e82979fefdfe708019ea[["chebi:133530
skos:exactMatch
mesh:C027957"]]
  style b8d737b89a421bd6ca058314564c9ed507cbfe3ec4a2e82979fefdfe708019ea fill:#f9f
  474146D6A6AFF3C7("mesh:C027957
skos:exactMatch
chebi:133530
inversion")
  style 474146D6A6AFF3C7 fill:#bbf
  1036c55358639c5db78ada181ac38d8eda337e83efe1db901716d101777f8474[["mesh:C027957
skos:exactMatch
chebi:133530"]]
  style 1036c55358639c5db78ada181ac38d8eda337e83efe1db901716d101777f8474 fill:#f9f
  AED810A43159DA66("mesh:C027957
skos:exactMatch
cas:30223-92-8
chaining")
  style AED810A43159DA66 fill:#bbf
  b5cd9f2dfa98540a3485a473bed0870720d7de23b87847ba508b8c85961e3b7d[["mesh:C027957
skos:exactMatch
cas:30223-92-8"]]
  style b5cd9f2dfa98540a3485a473bed0870720d7de23b87847ba508b8c85961e3b7d fill:#f9f
  983062C7B8D6517E-->|source|obo:chebi
  chebi:133530-->|subject of|983062C7B8D6517E
  cas:30223-92-8-->|object of|983062C7B8D6517E
  0b8eb968c306d65e1715a7b0961f6a4d99b5b19081edb67cee701fd887af1290-->|has evidence|983062C7B8D6517E
  chebi:133530-->|subject of|21056C0956788E11
  cas:30223-92-8-->|object of|21056C0956788E11
  a0022401f47964288ecc1ab706d79b4d4abc10edf33d0a71953834a0b0b3c24c-->|has evidence|21056C0956788E11
  244808D78AFCBDC1-->|has author|orcid:0000-0003-4423-4370
  244808D78AFCBDC1-->|source|wikidata:Q111239110
  chebi:133530-->|subject of|244808D78AFCBDC1
  mesh:C027957-->|object of|244808D78AFCBDC1
  b8d737b89a421bd6ca058314564c9ed507cbfe3ec4a2e82979fefdfe708019ea-->|has evidence|244808D78AFCBDC1
  mesh:C027957-->|subject of|474146D6A6AFF3C7
  chebi:133530-->|object of|474146D6A6AFF3C7
  1036c55358639c5db78ada181ac38d8eda337e83efe1db901716d101777f8474-->|has evidence|474146D6A6AFF3C7
  mesh:C027957-->|subject of|AED810A43159DA66
  cas:30223-92-8-->|object of|AED810A43159DA66
  b5cd9f2dfa98540a3485a473bed0870720d7de23b87847ba508b8c85961e3b7d-->|has evidence|AED810A43159DA66
  21056C0956788E11-->|derived from|0b8eb968c306d65e1715a7b0961f6a4d99b5b19081edb67cee701fd887af1290
  474146D6A6AFF3C7-->|derived from|b8d737b89a421bd6ca058314564c9ed507cbfe3ec4a2e82979fefdfe708019ea
  AED810A43159DA66-->|derived from|a0022401f47964288ecc1ab706d79b4d4abc10edf33d0a71953834a0b0b3c24c
  AED810A43159DA66-->|derived from|1036c55358639c5db78ada181ac38d8eda337e83efe1db901716d101777f8474
```
