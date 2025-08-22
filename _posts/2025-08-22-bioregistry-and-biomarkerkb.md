---
layout: post
title: The Bioregistry and BiomarkerKB
date: 2025-08-22 10:32:00 +0200
author: Charles Tapley Hoyt
tags:
  - biomarker
  - semantic spaces
  - bioregistry
  - BiomarkerKB
---

The [Bioregistry](https://bioregistry.io) is a community-driven registry of
semantic spaces and their metadata. When I learned about
[BiomarkerKB](https://biomarkerkb.org) at the International Society for
Biocuration's
[18th Annual International Biocuration Conference](https://www.stowers.org/events/biocuration2025),
I was excited to curate new records (and prefixes) in the Bioregistry to cover
BiomarkerKB's semantic spaces on biomarkers. This post summarizes the
discussions I've had with its maintainers, Jeet and Raja, throughout the
Bioregistry curation process and also gives insight into how databases can
benefit from being represented in the Bioregistry.

## How to Contribute to the Bioregistry

The Bioregistry follows the
[open data, open code, open infrastructure (O3) guidelines](https://www.nature.com/articles/s41597-024-03406-w),
meaning that anyone can make suggestions or additions either by creating an
issue or a pull request on its
[GitHub repository](https://github.com/biopragmatics/bioregistry). Both
maintainers of ontologies, controlled vocabularies, databases, etc. and
proactive community members can request new prefixes (i.e., add new records that
represent a semantic space) by following the project's
[contribution guidelines](https://github.com/biopragmatics/bioregistry/blob/main/docs/CONTRIBUTING.md#content-contribution)
(TL;DR, [watch this tutorial](https://www.youtube.com/watch?v=e-I6rcV2_BE)).

## Contributing New Prefixes for BiomarkerKB

Most importantly, I coordinated with its maintainers Raja and Jeet to make a
[pull request](https://github.com/biopragmatics/bioregistry/pull/1527) to the
Bioregistry's [GitHub repository](https://github.com/biopragmatics/bioregistry)
and add two new prefixes. I was also able to explain the relationship between
the records in the Bioregistry and their resource. I recorded part of our
discussion that is generally useful for anyone who's making a resource, and want
to think about some of the benefits:

<iframe width="560" height="315" src="https://www.youtube.com/embed/Of1mH_uSBpc?si=mPp_3r_9fUgq22Mp" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

As a follow-up, Jeet and Raja requested a summary of this discussion that they
could incorporate into BiomarkerKB's FAQ. Below is a draft of that text, which
could be easily adapted for any resource.

## Text for BiomarkerKB's FAQ

The [Bioregistry](https://bioregistry.io) is a community-driven registry of
semantic spaces and their metadata. It contains records for three semantic
spaces created for BiomarkerKB:

1. [`obci`](https://bioregistry.io/obci) for the Ontology for Biomarkers of
   Clinical Interest
2. [`biomarkerkb`](https://bioregistry.io/biomarkerkb) for condition-specific
   biomarkers
3. [`biomarkerkb.canonical`](https://bioregistry.io/biomarkerkb.canonical) for
   condition-agnostic biomarkers

The Bioregistry enables BiomarkerKB to unambiguously communicate how its
entities should be written as URIs and compact URIs (CURIEs) for use in semantic
web and linked (open) data settings. This supports many kinds of scientists,
including:

- **biocurators**, to identify BiomarkerKB's semantic spaces as high quality
  resources for use in annotating their own data
- **data providers**, to make their data and knowledge more FAIR before and
  during publication
- **data scientists**, to validate biomarker data annotated with BiomarkerKB
  semantic spaces against an actionable
- **data stewards**, to reference the Bioregistry records as components of
  research data management plans (DMPs)
- **web developers**, to resolve identifiers from BiomarkerKB's semantic spaces
  to human-readable web pages

---

If you're a database maintainer and would like some specific attention given to
representing your resource in the Bioregistry, or explainaning how the
Bioregistry could be used for your project, please reach out! My contact
information is at the bottom of my website.
