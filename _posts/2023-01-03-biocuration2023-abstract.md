---
layout: post
title: Promoting the longevity of curated scientific resources through open code, open data, and public infrastructure
date: 2023-01-03 11:28:00 -0500
author: Charles Tapley Hoyt
tags: biocuration philosophy
---
The [16th Annual International Biocuration Conference (Biocuration 2023)](https://biocuration2023.github.io)
is taking place in Padua, Italy from April 24-26<sup>th</sup>, 2023. While I'm serving as a co-chair of the conference,
I also think this is a great venue to communicate some of my thoughts on longevity and sustainability that have been
gestating during the development of the [Bioregistry](https://bioregistry.io) and
other [Biopragmatics](https://biopragmatics.github.io/) projects. This blog post contains the abstract I've submitted
for oral presentation.

**Note**: if you want to submit your own abstract, you have until the end of today (January 3<sup>rd</sup>, 2023,
anywhere on earth) to submit via [EasyChair](https://easychair.org/conferences/?conf=biocuration2023).

## Abstract

Many model organism databases, pathway databases, ontologies, and other curated resources that support research in the
life and natural sciences combine expert-curated data with surrounding software code and services. However, such
resources are often maintained internally by members of a single institution and are therefore susceptible to
fluctuations in funding, personnel, and institutional priorities. Too often, resources go out of date, are abandoned, or
become inaccessible, for example, when a grant runs out or a key person moves on. Therefore, we need better solutions
for creating resources that are less susceptible to such external factors and can continue to be used and maintained by
the community that they serve.

We propose a new model for the creation and maintenance of curated resources that promotes longevity through a
combination of technical and social workflows, and a progressive governance model that supports and encourages
community-driven curation. **1)** The technical aspect of our model necessitates open data, open code, and open
infrastructure. Both code and data are permissively licensed and kept together under public version control. This
enables anyone to directly suggest improvements and updates. Further, automation is used for continuous integration
(e.g., semi-automated curation, quality assurance) and continuous delivery (e.g., static website generation, export in
multiple formats). **2)** The social aspect of our model first prescribes the composition of training material, curation
guidelines, contribution guidelines, and a community code of conduct that encourage and support potential community
curators. Second, it requires the use of public tools for suggestions, questions, discussion as well as social workflows
like pull requests for the submission and review of changes. **3)** The governance aspect of our model necessitates the
division of responsibilities and authority (e.g., for reviewing/merging changes to the code/data) across multiple
institutions such that it is more robust to fluctuation in funding and personnel that can also be updated over time. It
prescribes liberal attribution and acknowledgement of the individuals and institutions (both internal and external to
the project) who contribute on a variety of levels (e.g., code, data, discussion, funding). More generally, our model
requires that a minimal governance model is codified and instituted as early as possible in a project's lifetime.

This talk will provide a perspective on how existing resources relate to our model, describe each of our model’s aspects
in more detail (illustrated through the [Bioregistry](https://bioregistry.io) resource), and provide a practical path
towards both creating new sustainable resources as well as revitalizing existing ones.

---
Later, I will update this post with a link to the slides for the related talk. Please let me know if you'll be in Padua
for the conference! I'd love to catch up.
