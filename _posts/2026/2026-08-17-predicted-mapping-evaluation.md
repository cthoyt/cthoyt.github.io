---
layout: post
title:
  "Automating the Evaluation of Predicted Semantic Mappings: Opportunities for
  OAEI"
date: 2026-08-17 11:41:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - benchmarks
  - EDOAL
  - OAEI
---

This is the first of a two part blog post on the past and future of automated
evaluation of predicted semantic mappings.



What is this post: Why does it exist: What should people look at:

This idea was originally from 2023 and was developed inside SeMRA, but with the
re-implementation of SSSOM software in SSSOM-Pydantic in the last year, I was
able to make it fully generic.

This post is an adaptation of the docs at XXX

## Part 1 - A Brief History of the OAEI

While there have been many manual, automated, and semi-automated efforts towards
ontology alignment, this post will focus on the
[Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org)
as a well-established, yearly competition occurring since 2004. It has produced
and evaluated benchmarks for ontology mapping software across biology, medicine,
ecology, digital humanities, archaeology, and other disciplines.

In order to submit their ontology mapping software to the OAEI for evaluation,
developers must ensure their software consumes ontologies in the
[Web Ontology Language (OWL)](https://www.w3.org/OWL/) format and outputs
predicted semantic mappings in the
[Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
format. Then, the software can be automatically evaluated by the OAEI's
[Alignment API and Alignment Server](https://moex.gitlabpages.inria.fr/alignapi),
and more recently, a larger set of frameworks and tools including
[HOBBIT](https://project-hobbit.eu/outcomes/hobbit-platform/),
[MELT](https://github.com/dwslab/melt/), and SEALS[^1], orchestrated through
Docker.

[^1]:
    The most recent report from OAEI in 2024 points to
    `https://seals-project.eu`, which appears to have been hijacked by a
    cryptocurrency scam.

During its two-decade runtime, the OAEI consistently reuses the same benchmarks.
For example, the [largebio](https://www.cs.ox.ac.uk/isg/projects/SEALS/oaei/)
task for mapping between the
[Foundational Model of Anatomy (FMA)](https://semantic.farm/registry/fma>)
ontology,
[Systematized Nomenclature of Medicine - Clinical Terms (SNOMED-CT)](https://semantic.farm/registry/snomedct),
and United States
[National Cancer Institute Thesaurus (NCIT)](https://semantic.farm/registry/ncit)
ran between 2011 and 2022 before being incorporated into the
[Bio-ML](https://krr-oxford.github.io/OAEI-Bio-ML/) task, which still runs as of
writing in 2026.

There are several opportunities for improving the way the evaluation of
predicted semantic mappings is done.

### Improved Standards and Software

The EDOAL format is relatively challenging to understand and work with and the
number and complexity of frameworks involved in the OAEI evaluation (e.g.,
SEALS, HOBBIT, MELTS) has increased dramatically.

The
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
presents an alternative for the automated evaluation of predicted semantic
mappings whose:

- specification is defined with modern tooling (i.e.,
  [LinkML](https://linkml.io))
- primary exchange format is simpler (TSV instead of XML)
- documentation is more approachable and complete
- software ecosystem
  ([sssom-pydantic](https://github.com/cthoyt/sssom-pydantic/),
  [sssom-py](https://github.com/mapping-commons/sssom-py), and
  [sssom-java](https://incenp.org/dvlpt/sssom-java/)) is still under active
  development (the Alignment API project has been inactive since 2021) and
  available in Python

Ideally, evaluation would just be the comparison of semantic mappings in the
SSSOM format from two sources: **manual curation from experts** and
**predictions from software**. This could significantly reduce the complexity
and proliferation of evaluation software.

As an aside, `sssom-py` implements a preliminary
[EDOAL importer](https://mapping-commons.github.io/sssom-py/api/parsers/?h=xml#sssom.parsers.parse_alignment_xml),
however, this would need revisiting and re-reimplementing in SSSOM-Pydantic with
unit tests, examples, and better documentation. Establishing interoperability
between data formats makes transitioning much easier, and allows for more
abstract thinking about the problem space rather than worrying about the
politics and history of the formats themselves.

### Improved Transparency and Longevity

The OAEI does not have an obvious mechanism through which it stores and shares
predicted semantic mappings and their metadata. In some cases, I was able to
find links from the published results to files that contained the results from
the challenges, but not consistently.

This is an openness and transparency issue that poses challenges in the reuse of
previously results, such as for reproduction. It also hinders historical
analyses such as the elucidation trends in software performance over time.

Community repositories for semantic mappings like
[Biomappings](https://github.com/biopragmatics/biomappings) demonstrated how an
[open data, open code, and open infrastructure (O3)](https://doi.org/10.1038/s41597-024-03406-w)
approach democratizes the storage and curation of semantic mappings. O3
resources achieve transparency and longevity by making their static results
available through long-term archival systems like [Zenodo](https://zenodo.org)
and manually curated results available through version control systems like
[Git](https://git-scm.com/) via a forge like [GitHub](https://github.com).

Biomappings spun out its code into the stand-alone
[SSSOM Curator](https://github.com/cthoyt/sssom-curator) software to enable the
creation and management of new semantic mapping repositories beyond Biomappings
that exist for various tasks, projects, or domains.

### Making the Results Actionable

If the predicted semantic mappings were stored and shared, then expert curators
could review them and submit them to the upstream resources that they concern.
This would be an opportunity for OAEI to have a meaningful impact on the
downstream scientific tasks that consume mappings.

Again, the Biomappings repository pioneered combining the prediction, storage,
and curation workflows into a single software stack. Such a workflow could be
adopted by OAEI (and similar mapping challenges) to increase its downstream
impact. This would be supported by ontology curation environments like the
[Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit),
which are implementing SSSOM support to enable the external curation of semantic
mappings. I wrote about this in detail in a [previous
post]({% post_url 2026/2026-08-07-sssom-to-owl %}).

### Making Benchmarks More Dynamic

The benchmark datasets in OAEI appear to be static, i.e., they are not updated
as the resources they concern are updated with new terms and new first-party
semantic mappings.
Ideally, the benchmarks would be updated each year to incorporate not only
first party curations from the ontologies, but also third party curations
of predicted mappings from previous years.

Benchmark tasks could then be retired when the alignment between two or
more ontologies are complete. Further, new benchmarking tasks should be much easier to produce
based on first-party semantic mappings available in ontologies and third-party semantic mappings
from repositories like Biomappings.

---

In the second part of this post, I present an implementation of a new workflow for
constructing and evaluating benchmarks that builds on mature tools for handling
ontologies and SSSOM mappings






## Part 2 - A New Implementation

### Maintenance of Benchmarks

1. adopt a better semantic mapping format and software ecosystem
2. store and manually curate the results of mapping prediction
3. maintain old benchmarks and create new ones
4. retire benchmarks for which ontology alignment has been completed

The goal of the SSSOM-Pydantic evaluation pipeline is to build on existing tools
for extracting mappings from ontologies (e.g.,
[PyOBO](https://github.com/biopragmatics/pyobo)), curated resources like
Biomappings, and easily reusable prediction workflows like SSSOM-Curator to
automatically construct new benchmarks based on existing SSSOM documents then
automatically calculate statistics about alignment completion (i.e., how many
more curations are needed to check all predicted mappings, and how many more
curations are needed to complete the alignment?) and the correctness of the
prediction software (e.g., accuracy, precision, recall, $F_1$).

Until all predictions are curated, the accuracy, precision, recall, and $F_1$
are an estimation of the true metrics, since the positive and negative manually
curated mappings likely are not complete and therefore have some bias in which
things were curated (e.g., I always curate the easiest first, leading towards a
skew that more of my manual curations result in positive calls).



1. Explain the implementation
2. Show the results

## Evaluating Lexical Predictions produced by SSSOM Curator

In the following example, three sources of mappings are combine for the
evaluation:

1. Mappings from [Medical Action Ontology (MAXO)](https://semantic.farm/maxo)
   extracted using PyOBO, which include mappings to
   [Medical Subject Headings (MeSH)](https://semantic.farm/mesh) with no
   metadata, so they default to `oboInOwl:hasDbXref` as a predicate and
   `semapv:UnspecifiedMapping` as a justification.
2. Manually curated mappings from Biomappings, which includes previously curated
   mappings between MAXO and MeSH with high precision predicates and
   justification.
3. Mappings predicted by the SSSOM Curator between MAXO and MeSH with lexical
   matching

```console
$ pyobo lookup sssom maxo -o maxo.sssom.tsv

$ sssom_pydantic subset \
    -i https://w3id.org/biopragmatics/biomappings/sssom/biomappings.sssom.tsv \
    --prefix maxo \
    --target-prefix mesh \
    --no-exclude-negatives \
    --no-exclude-unsure \
    --exclude-predicted \
    -o biomappings-maxo-mesh.sssom.tsv

$ mkdir maxo-mesh-predictions
$ sssom_curator init --directory maxo-mesh-predictions
$ sssom_curator -p maxo-mesh-predictions predict lexical mesh maxo

$ sssom_pydantic evaluate \
    -i maxo.sssom.tsv \
    -i biomappings-maxo-mesh.sssom.tsv \
    -i maxo-mesh-predictions/data/predictions.sssom.tsv \
    --accept-unspecified
```

This workflow pools arbitrary SSSOM files then stratifies them into positive,
negative, predicted (positive), and predicted negative mappings using the
`stratify()` function. When extending this workflow to several other OBO Foundry
ontologies mapping to MeSH, a table like this is produced:

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

Why am I looking at mesh? Many ontologies use MeSH as a starting point. MeSH is
a highly valuable lexical resource developed to index papers in PubMed, but it
doesn't go as far as to develop itself as an ontology with more precise
definitions of relationships and axioms. Therefore, many OBO Foundry ontologies
can be mapped back to mesh. OMIT even shamelessly imports the entirety of MeSH
under http://purl.obolibrary.org/obo/OMIT_0000110 (shameless because it assigns
new identifiers but doens't cross-reference back to the original MeSH terms)

Note that lexical matching typically has a high precision (i.e., most
predictions are right) but lower recall (i.e., some potential predictions are
missed). Given the problem domain that (almost all) ontologies don't have
one-to-many or many-to-one mappings, then it's also possible to identify
entities for which there is no mapping between two given resources and further
increase the accuracy of the accuracy metric.

## Next Steps

Looking forward, this workflow can be arbitrarily extended with additional
curations of mappings in Biomappings (or any other manually curated SSSOM files
or ontologies) to be applied. It currently doesn't automatically stratify based
on mapping tool, but if there are additional ones put into use (such as LeonMap,
implemented by Harshit Soni and suggested
[here](https://github.com/biopragmatics/biomappings/pull/274), then this is an
important step towards building an automated, rerunnable evaluation workflow.

## Appendix

For reference, here are the OAEI Calls and Publications between 2004-2026:

| Year | Call                                   | Publication                                                            |
| ---: | -------------------------------------- | ---------------------------------------------------------------------- |
| 2026 | https://oaei.ontologymatching.org/2026 |                                                                        |
| 2025 | https://oaei.ontologymatching.org/2025 |                                                                        |
| 2024 | https://oaei.ontologymatching.org/2024 | https://inria.hal.science/hal-04892635/                                |
| 2023 | https://oaei.ontologymatching.org/2023 | https://ora.ox.ac.uk/objects/uuid:e167c7dc-72cd-476a-ba23-d4bcc86e0b60 |
| 2022 | https://oaei.ontologymatching.org/2022 | https://hal.science/hal-04351729/                                      |
| 2021 | https://oaei.ontologymatching.org/2021 | https://openaccess.city.ac.uk/id/eprint/27602/                         |
| 2020 | https://oaei.ontologymatching.org/2020 | https://hal.science/hal-04312966/                                      |
| 2019 | https://oaei.ontologymatching.org/2019 | https://openaccess.city.ac.uk/id/eprint/23708/                         |
| 2018 | https://oaei.ontologymatching.org/2018 | https://hal.science/hal-02089249/                                      |
| 2017 | https://oaei.ontologymatching.org/2017 | https://air.unimi.it/handle/2434/550707                                |
| 2016 | https://oaei.ontologymatching.org/2016 | https://inria.hal.science/hal-01421833/                                |
| 2015 | https://oaei.ontologymatching.org/2015 | https://hal.science/hal-01254907/                                      |
| 2014 | https://oaei.ontologymatching.org/2014 | https://hal.science/hal-01180915/                                      |
| 2013 | https://oaei.ontologymatching.org/2013 | https://inria.hal.science/hal-01140027/                                |
| 2012 | https://oaei.ontologymatching.org/2012 | https://inria.hal.science/hal-00768409/                                |
| 2011 | https://oaei.ontologymatching.org/2011 | https://inria.hal.science/hal-00781022/                                |
| 2010 | https://oaei.ontologymatching.org/2010 | https://inria.hal.science/hal-00793276/                                |
| 2009 | https://oaei.ontologymatching.org/2009 | https://inria.hal.science/hal-00794918/                                |
| 2008 | https://oaei.ontologymatching.org/2008 | https://inria.hal.science/hal-00793535/                                |
| 2007 | https://oaei.ontologymatching.org/2007 | https://inria.hal.science/hal-00822893/                                |
| 2006 | https://oaei.ontologymatching.org/2006 | https://ceur-ws.org/Vol-225/paper7.pdf                                 |
| 2005 | https://oaei.ontologymatching.org/2005 | https://inria.hal.science/hal-00922283/                                |
| 2004 | https://oaei.ontologymatching.org/2002 | https://inria.hal.science/hal-04892635/                                |
