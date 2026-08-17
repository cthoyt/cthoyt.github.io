---
layout: post
title: Automating the Evaluation of Predicted Semantic Mappings
date: 2026-08-17 11:41:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - benchmarks
  - EDOAL
---

The
[Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org)
has produced and evaluated benchmarks for ontology mapping software across
biology, medicine, ecology, digital humanities, archaeology, and other
disciplines since 2004. In order to submit, developers must ensure their
ontology mapping software consumes ontologies in the
[Web Ontology Language (OWL)](https://www.w3.org/OWL/) format and outputs
mappings in the
[Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
format, which can then be automatically evaluated by the OAEI's
[Alignment API and Alignment Server](https://moex.gitlabpages.inria.fr/alignapi).
A table of past OAEI calls and results are available below.

During its two-decade runtime, the OAEI consistently reuses the same benchmarks.
For example, the [largebio](https://www.cs.ox.ac.uk/isg/projects/SEALS/oaei/)
task for mapping between the
[Foundational Model of Anatomy (FMA)](https://semantic.farm/registry/fma>)
ontology, [Systematized Nomenclature of Medicine

- Clinical Terms (SNOMED-CT)](https://semantic.farm/registry/snomedct), and
  United States
  [National Cancer Institute Thesaurus (NCIT)](https://semantic.farm/registry/ncit)
  ran between 2011 and 2022 before being incorporated into the
  [Bio-ML](https://krr-oxford.github.io/OAEI-Bio-ML/) task, which still runs as
  of 2026.

This presents several opportunities to go beyond OAEI, in order to:

1. adopt a better semantic mapping format and software ecosystem
2. store and manually curate the results of mapping prediction
3. maintain old benchmarks and create new ones
4. retire benchmarks for which ontology alignment has been completed

The
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
and its associated software ecosystem are still under active maintenance
(whereas the alignment API project has not been updated since 2021), are already
considerably better documented than the alignment API and EDOAL, and adopt much
more straightforward languages (Python instead of Java) and formats (TSV instead
of XML).

Community repositories for semantic mappings like
[Biomappings](https://github.com/biopragmatics/biomappings) demonstrated how an
[open data, open code, and open infrastructure (O3)](https://doi.org/10.1038/s41597-024-03406-w)
approach democratizes the storage and curation of semantic mappings. The
Biomappings project itself led to the development of the
[SSSOM Curator](https://github.com/cthoyt/sssom-curator) software to wrap
prediction pipelines and provide an interactive curation interface for end
users.

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

Note that lexical matching typically has a high precision (i.e., most
predictions are right) but lower recall (i.e., some potential predictions are
missed). Given the problem domain that (almost all) ontologies don't have
one-to-many or many-to-one mappings, then it's also possible to identify
entities for which there is no mapping between two given resources and further
increase the accuracy of the accuracy metric.

Looking forward, this workflow can be arbitrarily extended with additional
curations of mappings in Biomappings (or any other manually curated SSSOM files
or ontologies) to be applied. It currently doesn't automatically stratify based
on mapping tool, but if there are additional ones put into use (such as LeonMap,
implemented by Harshit Soni and suggested
[here](https://github.com/biopragmatics/biomappings/pull/274), then this is an
important step towards building an automated, rerunnable evaluation workflow.

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
