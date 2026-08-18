---
layout: post
title:
  "Automating the Evaluation of Predicted Semantic Mappings Part 1:
  Opportunities for OAEI"
date: 2026-08-17 11:41:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - benchmarks
  - EDOAL
  - OAEI
---

This is the first of a two-part blog post on the past and future of automated
evaluation of predicted semantic mappings. I describe some of the challenges and
opportunities for challenges like the
[Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org)
and how they could be addressed with
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom),
and its ecosystem. In the [second
part]({% post_url 2026/2026-08-17-predicted-mapping-evaluation-implementation %}),
I present a concrete implementation of a new automated evaluation system that
address some of those challenges.

## Brief Background on OAEI

While there have been many manual, automated, and semi-automated efforts towards
ontology alignment, this post will focus on the
[Ontology Alignment Evaluation Initiative (OAEI)](https://oaei.ontologymatching.org)
as a well-established, yearly competition occurring since 2004. It has produced
and evaluated benchmarks for ontology mapping software across biology, medicine,
ecology, digital humanities, archaeology, and other disciplines.

<!-- prettier-ignore-start -->

> [!CAUTION]
> I found navigating the OAEI site difficult and its artifacts hard to find,
> so it's possible I missed something. If you find that I did, please let me
> know with the comment box at the bottom of the post and I will update the
> post accordingly.

<!-- prettier-ignore-end -->

The OAEI documents on their website that ontology mapping software should
consume ontologies in the [Web Ontology Language (OWL)](https://www.w3.org/OWL/)
format and outputs predicted semantic mappings the XML-based
[Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
format.

Originally, the results were to be submitted to the OAEI's
[Alignment API and Alignment Server](https://moex.gitlabpages.inria.fr/alignapi),
but there are now three additional frameworks for preparing code for submission
including the [HOBBIT](https://project-hobbit.eu/outcomes/hobbit-platform/),
[MELT](https://github.com/dwslab/melt/), and SEALS[^1]. I even found in the
[OAEI's 2024 results paper](https://inria.hal.science/hal-04892635/) that the
MELT framework can now accept mappings in the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom).

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

## Challenges and Opportunities

There are several opportunities for improving the way the evaluation of
predicted semantic mappings is done. Even though I'm using OAEI as an example
along with its format and technology stack, these ideas are widely applicable to
any automated evaluation of predicted semantic mappings.

### Improved Standards and Software

The revelation that the OAEI can now accept semantic mappings in SSSOM came late
into the process of writing this post, so the main point to make on the software
is that the proliferation and complexity of four frameworks for submitting to
OAEI (and their need to support the legacy EDOAL format) is overwhelming and not
obviously documented from their website.

<details style="margin-bottom: 1em">
<summary>expand to show why SSSOM is great anyway</summary>
<p>
SSSOM presents an alternative for the automated evaluation of predicted semantic
mappings whose:
</p>
<ul>
<li>specification is defined with modern tooling (i.e.,
  <a href="https://linkml.io">LinkML</a>)</li>
<li>primary exchange format is simpler (TSV instead of XML)</li>
<li>documentation is more approachable and complete</li>
<li>software ecosystem (
  <a href="https://github.com/cthoyt/sssom-pydantic">sssom-pydantic</a>,
  <a href="https://github.com/mapping-commons/sssom-py">sssom-py</a>, and
  <a href="https://incenp.org/dvlpt/sssom-java/">sssom-java</a>) is still under active
  development (the Alignment API project has been inactive since 2021) and
  available in Python and does not require containerization
</li>
</ul>
</details>

Further, the concept of evaluation could be greatly simplified. Ideally,
evaluation would just be the comparison of semantic mappings from two sources:
**manual curation from experts** and **predictions from software**. SSSOM has
the benefit of storing a mapping justification that tracks exactly this,
enabling the ingestion of arbitrary number of self-documenting SSSOM files,
rather than relying on external configuration, file identify, file naming
conventions, or other fragile mechanisms to differentiate between mapping types.

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
[SSSOM Curator](https://github.com/cthoyt/sssom-curator) software package to
enable the creation and management of new semantic mapping repositories beyond
Biomappings, which might be created for various tasks, projects, or domains.

### Making the Results Actionable

If the predicted semantic mappings were stored and shared, then expert curators
could review them and submit them to the upstream resources that they concern.
This would be an opportunity for OAEI to have a meaningful impact on the
downstream scientific tasks that consume mappings, as the goal of predicting
mappings is to complete alignments between pairs of ontologies (and other
semantic spaces).

Again, the Biomappings repository pioneered combining the semantic mapping
prediction, storage, and curation workflows into a single software stack. Such a
workflow could be adopted by OAEI (and similar mapping challenges) to increase
its downstream impact. The use of SSSOM also feeds into ontology curation
environments like the
[Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit),
which have implemented SSSOM support in order to enable the external curation of
semantic mappings. I wrote about this in detail in a [previous
post]({% post_url 2026/2026-08-07-sssom-to-owl %}).

The OAEI could achieve more meaningful impact by storing the predictions in the
SSSOM a git repository where they could be more easily reviewed, either with
SSSOM Curator or any other similar workflow that maintains full provenance from
prediction to review/curation.

### Making Benchmarks More Dynamic

The benchmark datasets in OAEI appear to be static, i.e., they do not appear to
be updated as the resources they concern are updated with new terms and new
first-party semantic mappings. Ideally, the benchmarks would be updated each
year to incorporate not only first party curations from the ontologies, but also
third party reviews/curations of predicted mappings from previous years'
competitions. Benchmark tasks could then be retired when the alignment between
two or more ontologies are completed.

Further, a workflow that can (semi-)automatically maintain a benchmark should
also be able to easier produce new benchmarking tasks based on first-party
semantic mappings available in ontologies and third-party semantic mappings from
repositories like Biomappings.

## Conclusions

Competitions like the
[Critical Assessment of Structure Prediction (CASP)](https://predictioncenter.org/index.cgi)
work because they ask for predictions to be made before performing an expensive,
specialized experiment in the laboratory. Conversely, the prediction of semantic
mappings exists in a very different space, where predictions can be easily
reviewed and validated. Therefore, I think that the automated evaluation of
predicted semantic mappings is long overdue for a perspective change, where the
goal shouldn't be to focus on the development of new tools, but rather to focus
on the prediction and curation of novel mappings that serve downstream
scientific applications.

In short: make your predictions, curate them, contribute them to Biomappings or
directly upstream, then everyone benefits, and we don't have to keep playing
this game.

In the [second
part]({% post_url 2026/2026-08-17-predicted-mapping-evaluation-implementation %})
of this post, I present an implementation of a new workflow for constructing and
evaluating benchmarks that closes this loop and addresses many of the challenges
and opportunities described above.

## Appendix

For reference, here are the OAEI Calls and Publications between 2004-2026:

| Year | Call                                           | Publication                                                            |
| ---: | ---------------------------------------------- | ---------------------------------------------------------------------- |
| 2026 | [Call](https://oaei.ontologymatching.org/2026) |                                                                        |
| 2025 | [Call](https://oaei.ontologymatching.org/2025) |                                                                        |
| 2024 | [Call](https://oaei.ontologymatching.org/2024) | https://inria.hal.science/hal-04892635/                                |
| 2023 | [Call](https://oaei.ontologymatching.org/2023) | https://ora.ox.ac.uk/objects/uuid:e167c7dc-72cd-476a-ba23-d4bcc86e0b60 |
| 2022 | [Call](https://oaei.ontologymatching.org/2022) | https://hal.science/hal-04351729/                                      |
| 2021 | [Call](https://oaei.ontologymatching.org/2021) | https://openaccess.city.ac.uk/id/eprint/27602/                         |
| 2020 | [Call](https://oaei.ontologymatching.org/2020) | https://hal.science/hal-04312966/                                      |
| 2019 | [Call](https://oaei.ontologymatching.org/2019) | https://openaccess.city.ac.uk/id/eprint/23708/                         |
| 2018 | [Call](https://oaei.ontologymatching.org/2018) | https://hal.science/hal-02089249/                                      |
| 2017 | [Call](https://oaei.ontologymatching.org/2017) | https://air.unimi.it/handle/2434/550707                                |
| 2016 | [Call](https://oaei.ontologymatching.org/2016) | https://inria.hal.science/hal-01421833/                                |
| 2015 | [Call](https://oaei.ontologymatching.org/2015) | https://hal.science/hal-01254907/                                      |
| 2014 | [Call](https://oaei.ontologymatching.org/2014) | https://hal.science/hal-01180915/                                      |
| 2013 | [Call](https://oaei.ontologymatching.org/2013) | https://inria.hal.science/hal-01140027/                                |
| 2012 | [Call](https://oaei.ontologymatching.org/2012) | https://inria.hal.science/hal-00768409/                                |
| 2011 | [Call](https://oaei.ontologymatching.org/2011) | https://inria.hal.science/hal-00781022/                                |
| 2010 | [Call](https://oaei.ontologymatching.org/2010) | https://inria.hal.science/hal-00793276/                                |
| 2009 | [Call](https://oaei.ontologymatching.org/2009) | https://inria.hal.science/hal-00794918/                                |
| 2008 | [Call](https://oaei.ontologymatching.org/2008) | https://inria.hal.science/hal-00793535/                                |
| 2007 | [Call](https://oaei.ontologymatching.org/2007) | https://inria.hal.science/hal-00822893/                                |
| 2006 | [Call](https://oaei.ontologymatching.org/2006) | https://ceur-ws.org/Vol-225/paper7.pdf                                 |
| 2005 | [Call](https://oaei.ontologymatching.org/2005) | https://inria.hal.science/hal-00922283/                                |
| 2004 | [Call](https://oaei.ontologymatching.org/2004) | https://inria.hal.science/hal-04892635/                                |
