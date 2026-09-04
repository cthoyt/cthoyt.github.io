---
layout: post
title:
  "Automating the Evaluation of Predicted Semantic Mappings Part 2: A New
  Workflow"
date: 2026-08-17 17:19:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - benchmarks
  - EDOAL
  - OAEI
  - Python
---

This is the second of a two-part blog post on the past and future of automated
evaluation of predicted semantic mappings. This part describes the
[implementation](https://github.com/cthoyt/sssom-pydantic/pull/131) of a new
automated workflow for the evaluation of predicted semantic mappings that
consumes arbitrary
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom),
stratifies mappings as manually curated or predicted, then produces an
evaluation for each source-target ontology pair present.

The [first part]({% post_url 2026/2026-08-17-mapping-evaluation-background %})
of this post described some of the opportunities for improving the automated
evaluation of predicted semantic mappings. However, this background isn't
necessary if you just want to see what I've made.

## Development History

I originally developed the idea and proof-of-concept for an evaluation workflow
that could consume arbitrary semantic mappings using the object model I
implemented in
[Semantic Mapping Reasoner and Assembler (SeMRA)](https://github.com/biopragmatics/semra) -
a software package for assembling semantic mappings at scale. These mappings
came from a variety of sources (e.g., ontologies, TSV, XML), data formats (e.g.,
SSSOM, EDOAL, OWL, OBO), justifications (e.g., manual curation, lexical
matching, ontology reasoning), and truthiness (positive or negative).

Therefore, it was key to consume and organize arbitrary sets semantic mappings
which may mix sources, formats, justifications, and truthiness. Specifically, I
wanted to make sure I could make use of:

1. existing tools for extracting semantic mappings from ontologies such as
   [PyOBO](https://github.com/biopragmatics/pyobo)
2. semantic mapping repositories that contain positive, negative, and predicted
   semantic mappings such as
   [Biomappings](https://github.com/biopragmatics/biomappings)
3. easily reusable prediction workflows like
   [SSSOM-Curator](https://github.com/cthoyt/sssom-curator)

While the initial 2023 implementation in
[biopragmatics/semra#12](https://github.com/biopragmatics/semra/pull/12) sat
untouched for a few years, I upstreamed some of the SeMRA's best ideas into the
SSSOM specification, implemented a new and more ergonomic SSSOM package in
Python ([SSSOM-Pydantic](https://github.com/cthoyt/sssom-pydantic)), then
re-implemented SeMRA to be fully SSSOM-compliant on top of SSSOM-Pydantic.

Finally, with motivation from my work in [NFDI4Chem](https://nfdi4chem.de) and
[NFDI Section Metadata Working Group on Ontology Harmonization and Mapping](https://github.com/nfdi-de/section-metadata-wg-onto)
supporting [Philip Strömert](https://github.com/StroemPhi) and
[Noura Rayya](https://github.com/NRayya) in revitalizing the
[Chemical Methods Ontology (CHMO)](https://semantic.farm/chmo) and other
chemistry ontologies, I was ready to re-implement the evaluation workflow to use
SSSOM rather than the SeMRA custom data model.

## Workflow

After assembling semantic mappings that comprise a _benchmark_, then there are
several questions to answer when evaluating predicted mappings between each pair
of resources (often ontologies), whose terms appear as subjects/objects in
mappings:

- what percentage of entities are already manually mapped?
- what percentage of entities are already known to be unmappable (i.e.,
  annotated with [sssom:NoTermFound](https://w3id.org/sssom/NoTermFound))?
- what percentage of entities that aren't already manually mapped have
  predictions that could be curated?
- what is the curation burden to check all predictions? to complete the
  alignment?
- how correct are the predictions, reported with accuracy, precision, recall,
  $F_1$, etc.?

<!-- prettier-ignore-start -->

> [!WARNING]
> There are a few caveats about the evaluation:
>
> 1. Until all predictions are curated, the accuracy, precision, recall, and
> $F_1$ are an estimation of the true metrics, since the positive and
> negative manually curated mappings likely are not complete and therefore
> have some bias in which things were curated (e.g., I always curate the
> easiest first, leading towards a skew that more of my manual curations
> result in positive calls).
> 2. SSSOM-Pydantic does not yet explicitly support `sssom:NoTermFound`, meaning
> that prior knowledge about unmappable entities isn't considered. This
> artificially increases the perceived mapping burden and deflates other
> metrics. I have been collecting ideas on how to model unmappabilities
> [here](https://github.com/cthoyt/sssom-pydantic/issues/163).

<!-- prettier-ignore-end -->

### Stratification

After concatenating semantic mappings from mixed sources, they are stratified as
predicted versus curated based on their mapping justification. Predicted
semantic mappings have one of the following justifications:

- `semapv:LexicalMatching`
- `semapv:LexicalSimilarityThresholdMatching`
- `semapv:LogicalReasoning`
- `semapv:SemanticSimilarityThresholdMatching`
- `semapv::StructuralMatching`

Manually curated semantic mappings have one of the following justifications:

- `semapv:ManualMappingCuration`
- `semapv:UnspecifiedMatching` (configurable, not universally useful)

Remaining mapping justifications in the
[Semantic Mapping Vocabulary (SEMAPV)](https://semantic.farm/registry/semapv)
can't be easily categorized. Semantic mappings are then subcategorized as
positive or negative (i.e., when the predicate modifier is set to `Not`). Note,
there are typically no negative predicted semantic mappings because software
focuses on producing positive semantic mappings.

### Statistics

A [confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix) is produced
with the following four count values, which can be calculated with simple set
operations:

- **true positives (TP)** comprise predicted positive mappings that have
  corresponding manually curated positive mappings.
- **false positives (FP)** comprise predicted positive mappings that have
  corresponding manually curated negative mappings. In practice, the false
  positive count becomes more accurate over time as predicted mappings get
  reviewed and incorporated into the manually curated set
- **true negatives (TN)** comprise predicted negative mappings that have
  corresponding manually curated negative mappings. In practice, prediction
  tools do not typically produce negative predictions.
- **false negatives (FN)** comprise predicted negative mappings that have
  corresponding manually curated positive mappings. Again, in practice,
  prediction tools do not typically produce negative predictions.

The formula for recall, precision, $F_1$, and others can be read off the linked
Wikipedia page. However, the lack of negatives makes statistics involving the
true negative and false negative counts less applicable.

If needed, negative mappings can be sampled using techniques based on the open
world assumption (OWA) or local closed world assumption (LCWA). The
[PyKEEN](https://github.com/pykeen/pykeen/) graph machine learning library has
[detailed documentation](https://pykeen.readthedocs.io/en/stable/reference/negative_sampling.html)
on these processes.

In the SSSOM-Pydantic implementation, the local closed world assumption is used,
meaning that for every manually curated positive mapping, if there is not a
corresponding positive prediction, then it's considered that a negative
prediction was made (and it's a false negative). Similarly, if there is a
manually curated negative mapping without a corresponding positive prediction,
then it's considered that the negative prediction was made (and it's a true
negative).

## Example Evaluation

The implementation of the evaluation workflow is available with a
well-documented Python API in
[ `sssom_pydantic.workflow.evaluation`](https://sssom-pydantic.readthedocs.io/en/latest/workflow/evaluation.html)
as well as via the `sssom_pydantic evaluate` command line interface.

Below, I present an end-to-end example evaluation of lexical predictions
produced by SSSOM Curator, in which three sources of mappings are produced and
combine:

1. Mappings from [Medical Action Ontology (MAXO)](https://semantic.farm/maxo)
   extracted using PyOBO, which include mappings to
   [Medical Subject Headings (MeSH)](https://semantic.farm/mesh) with no
   metadata, so they default to `oboInOwl:hasDbXref` as a predicate and
   `semapv:UnspecifiedMapping` as a justification.
2. Manually curated mappings from Biomappings, which includes previously curated
   mappings between MAXO and MeSH with high precision predicates and
   justification.
3. Mappings predicted by the
   [SSSOM Curator](https://github.com/cthoyt/sssom-curator) between MAXO and
   MeSH with lexical matching

The following commands use `uvx` for automatic installation and running of
command line interfaces for PyOBO and SSSOM-Pydantic to acquire/produce the
SSSOM files that are run in evaluation:

```console
$ uvx pyobo lookup sssom maxo -o maxo.sssom.tsv

$ uvx sssom_pydantic subset \
    -i https://w3id.org/biopragmatics/biomappings/sssom/biomappings.sssom.tsv \
    --prefix maxo \
    --target-prefix mesh \
    --no-exclude-negatives \
    --no-exclude-unsure \
    --exclude-predicted \
    -o biomappings-maxo-mesh.sssom.tsv

$ mkdir maxo-mesh-predictions
$ uvx sssom_curator init --directory maxo-mesh-predictions
$ uvx sssom_curator -p maxo-mesh-predictions predict lexical mesh maxo

$ uvx sssom_pydantic evaluate \
    -i maxo.sssom.tsv \
    -i biomappings-maxo-mesh.sssom.tsv \
    -i maxo-mesh-predictions/data/predictions.sssom.tsv \
    --accept-unspecified
```

I actually extended this workflow to evaluate the mapping between several other
[Open Biological and Biomedical Ontology Foundry (OBO) Foundry](https://obofoundry.org/)
ontologies and MeSH and present the results below.

MeSH is a highly valuable lexical resource developed to index papers in PubMed,
but it doesn't go as far as to develop itself as an ontology with more precise
definitions of relationships and axioms. Therefore, many OBO Foundry ontologies
either use MeSH as a starting point, or at least cover similar topics. Many
additionally curate mappings back to MeSH, but if they're available, they're not
always complete. In the most eggrigious case, the
[Ontology for MicroRNA Target (OMIT)](https://semantic.farm/omit) clones the
entirety of MeSH under
[OMIT:0000110 (MeSH_term)](http://purl.obolibrary.org/obo/OMIT_0000110) but
provides no cross-references back to the original terms 🤦

| Prefix 1                               | Prefix 2                           | Completion | Accuracy | Precision | Recall | $F_1$ |
| -------------------------------------- | ---------------------------------- | ---------: | -------: | --------: | -----: | ----: |
| [chebi](https://semantic.farm/chebi)   | [mesh](https://semantic.farm/mesh) |       7.9% |    98.2% |     98.9% |  99.2% | 99.1% |
| [cl](https://semantic.farm/cl)         | [mesh](https://semantic.farm/mesh) |      26.9% |    53.4% |     90.8% |  47.6% | 62.5% |
| [clo](https://semantic.farm/clo)       | [mesh](https://semantic.farm/mesh) |      50.0% |    61.9% |     66.7% |  85.7% | 75.0% |
| [fix](https://semantic.farm/fix)       | [mesh](https://semantic.farm/mesh) |      29.7% |    93.5% |     93.3% | 100.0% | 96.6% |
| [go](https://semantic.farm/go)         | [mesh](https://semantic.farm/mesh) |      32.5% |    80.3% |     82.6% |  96.1% | 88.8% |
| [hgnc](https://semantic.farm/hgnc)     | [mesh](https://semantic.farm/mesh) |       1.9% |    43.6% |     68.0% |  45.9% | 54.8% |
| [hp](https://semantic.farm/hp)         | [mesh](https://semantic.farm/mesh) |      12.2% |    96.6% |     98.8% |  97.7% | 98.3% |
| [maxo](https://semantic.farm/maxo)     | [mesh](https://semantic.farm/mesh) |      43.3% |    86.9% |    100.0% |  86.9% | 93.0% |
| [mi](https://semantic.farm/mi)         | [mesh](https://semantic.farm/mesh) |      17.6% |    95.8% |     95.8% | 100.0% | 97.9% |
| [mmo](https://semantic.farm/mmo)       | [mesh](https://semantic.farm/mesh) |      39.6% |    88.9% |    100.0% |  88.9% | 94.1% |
| [ms](https://semantic.farm/ms)         | [mesh](https://semantic.farm/mesh) |      44.8% |    81.5% |     80.8% | 100.0% | 89.4% |
| [so](https://semantic.farm/so)         | [mesh](https://semantic.farm/mesh) |      14.6% |    95.2% |     95.2% | 100.0% | 97.6% |
| [txpo](https://semantic.farm/txpo)     | [mesh](https://semantic.farm/mesh) |      25.8% |    72.6% |     98.4% |  73.5% | 84.1% |
| [uberon](https://semantic.farm/uberon) | [mesh](https://semantic.farm/mesh) |       7.1% |    12.2% |     98.7% |  12.2% | 21.7% |
| [vo](https://semantic.farm/vo)         | [mesh](https://semantic.farm/mesh) |      69.4% |    64.1% |     91.2% |  53.8% | 67.6% |
| [vto](https://semantic.farm/vto)       | [mesh](https://semantic.farm/mesh) |       0.3% |    50.0% |     50.0% | 100.0% | 66.7% |
| [xlmod](https://semantic.farm/xlmod)   | [mesh](https://semantic.farm/mesh) |      44.7% |    98.7% |     98.7% | 100.0% | 99.3% |

Note that lexical matching typically has a high precision (i.e., most
predictions are right) but lower recall (i.e., some potential predictions are
missed). However, this is also biased, because most curations are biased towards
the easiest, and therefore, most likely to be correct.

Given the problem domain that (almost all) ontologies don't have one-to-many or
many-to-one mappings, then it's also possible to identify entities for which
there is no mapping between two given resources and further increase the
accuracy of the accuracy metric, recall the use of `sssom:NoTermFound`.

In this table, I only present the completion, which corresponds to the
percentage of predictions that have been curated. There's still lots of work to
go - I could imagine doing a bit more math to estimate curation burden in terms
of hours and even cost. I've been preparing these curations with a local version
of SSSOM-Curator, but the goal in the future is to have a hosted instance that
is more accessible, e.g., for ontology curators or other NFDI stakeholders (see
[tracking issue](https://github.com/cthoyt/sssom-curator/issues/47)).

## Next Steps

Looking forward, this workflow can be arbitrarily extended with additional
curations of mappings in Biomappings (or any other manually curated SSSOM files
or ontologies) to create new benchmarks, which stay up-to-date by being
reproducibly constructed against the most recent versions of the upstream
ontologies and Biomappings.

This workflow doesn't yet stratify by mapping tool, since in practice,
Biomappings and SSSOM-Curator have mostly used the lexical matching workflow,
except for the interesting case of mapping image annotations to chemical
instrumentation in my post on [Bridging NFDI's culture and chemistry knowledge
graphs]({% post_url 2025/2025-10-07-bridging-culture-and-chemistry %}) with text
embedding-based matching. However, I'm motivated to make this extension because
of a recent submission from [Harshit Soni](https://github.com/HarshitSoni1903)
to include predictions from
[LeonMap](https://github.com/HarshitSoni1903/Weakly-Supervised-Representation-Learning-for-Cross-Ontology-Mapping)
in Biomappings in
[biopragmatics/biomappings#274](https://github.com/biopragmatics/biomappings/pull/274)
and recent discussion with the
[OntoAligner](https://github.com/sciknoworg/OntoAligner) developers to include
SSSOM export in their tool in
[sciknoworg/OntoAligner#123](https://github.com/sciknoworg/OntoAligner/issues/123).
Then, this evaluation workflow could be used to run competitions and make
comparison tools between mapping tools or hyperparameter optimization for a
single tool, and significantly simplify competitions like the
[Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org),
which I discussed in detail in my [previous
post]({% post_url 2026/2026-08-17-mapping-evaluation-background %}#brief-background-on-oeai)

However, as I mentioned in the closing remarks of my [previous
post]({% post_url 2026/2026-08-17-mapping-evaluation-background %}#conclusions),
I don't think that competition should be the point here - tools are more than
good enough, and I haven't yet seen a benefit in increasingly complex and
expensive mapping software past simple lexical prediction. Ideally, I would like
to see more improvement in integration of various components of the mapping
prediction, curation, and publication stack to support the most downstream tasks
that actually consume mappings.

---

in case you're wondering, it took about 8-10 days to do all the implementation
and write these posts. it's finally raining in Bonn, and I'm feeling good about
finishing this up.
