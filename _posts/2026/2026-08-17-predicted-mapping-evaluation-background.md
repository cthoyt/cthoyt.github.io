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

> [!CAUTION] I don't have a working understanding of the entire history of the
> competition, and I found navigating its site and artifacts to be challenging.
> It's possible I missed something, so if you find that I did, please let me
> know with the comment box at the bottom of the post.

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

## Challenges and Opportunities

There are several opportunities for improving the way the evaluation of
predicted semantic mappings is done. Even though I'm using OAEI, its data
format, and technology stack as an example, these ideas are widely applicable to
any automated evaluation of predicted semantic mappings.

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
mappings. I wrote about this in detail in a [previous post]({%
post_url 2026/2026-08-07-sssom-to-owl %}).

### Making Benchmarks More Dynamic

The benchmark datasets in OAEI appear to be static, i.e., they are not updated
as the resources they concern are updated with new terms and new first-party
semantic mappings. Ideally, the benchmarks would be updated each year to
incorporate not only first party curations from the ontologies, but also third
party curations of predicted mappings from previous years.

Benchmark tasks could then be retired when the alignment between two or more
ontologies are complete. Further, new benchmarking tasks should be much easier
to produce based on first-party semantic mappings available in ontologies and
third-party semantic mappings from repositories like Biomappings.

---

In the [second
part]({% post_url 2026/2026-08-17-predicted-mapping-evaluation-implementation %})
of this post, I present an implementation of a new workflow for constructing and
evaluating benchmarks that builds on mature tools for handling ontologies and
SSSOM mappings

---

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
