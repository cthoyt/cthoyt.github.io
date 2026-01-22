---
layout: page
title: Hire Me
permalink: /hiring/
---

### Public Projects

My employer, RWTH Aachen University, charges at cost for human resources, plus
around a 50% overhead for administration and facilities.

Costs are standardized for German public employees by the
[Tarifvertrag für den öffentlichen Dienst (TVöD)](https://de.wikipedia.org/wiki/Tarifvertrag_f%C3%BCr_den_%C3%B6ffentlichen_Dienst)
pay scale, which incorporates qualifications and experience.

For projects that I lead, I book (at maximum) at the
[E14 Stufe 3](https://www.jobs-beim-staat.de/tarif/tvoed-bund_e14) rate, which
is 5,928 €/month as of January 2026. This means that a contract, with overhead,
can be roughly estimated at 9,000€/month, or 52€/hour.

While it would be more lucrative to run projects privately, I currently prefer
to run projects through the university as funding is tied to career progression
towards the rank of professor.

### Privacy and Non-disclosure Agreements

I am able to participate in (mutual) non-disclosure agreements (NDAs) for
university-scoped projects through the Institute of Inorganic Chemistry at RWTH
Aachen University.

I am also able to privately sign NDAs, but not in parallel with nor before a
university NDA, i.e., it's not possible to sign a personal NDA for development
of a project that would be run through the university.

### Technology Transfer

#### Prior Art

I bring to projects a mature ecosystem of
[free/libre and open-source software (FLOSS)](https://www.gnu.org/philosophy/floss-and-foss.en.html)
packages for the standardization, integration, and analysis of data and
knowledge. These components are typically licensed under business-friendly,
permissive,
[Open Source Initiative (OSI)](https://opensource.org/licenses)-approved
licenses such as MIT or Apache 2.0.

I intentionally avoid using
[copyleft licenses](https://www.gnu.org/licenses/copyleft.en.html) in this
ecosystem in order to reduce friction for organizations that require internal,
proprietary, or private extensions.

For example, the [Biopragmatics Stack](https://github.com/biopragmatics) exposes
high-level components for use in the generation and application of biomedical
knowledge graphs, e.g., in early-stage drug discovery. My [blog](..) provides
more context on various components of the Biopragmatics Stack and related,
domain-agnostic tooling that I develop and maintain.

#### Open Source vs. Internal

**My guiding principle:** generic improvements are open; partner-specific work
remain private.

I expect that during projects, whether public or private, I will maintain and
make (generic) extensions to components as open source contributions to the
appropriate public repositories. I maintain ownership over all such open source
contributions, which are in turn made available under their respective
open-source licenses.

For example, if a project requires the addition of a new public database to
[PyOBO](https://github.com/biopragmatics/pyobo), then I would directly
incorporate it into the public PyOBO repository.

Conversely, if a project requires the addition of an internal, proprietary, or
otherwise private database to PyOBO, then I would write an extension to PyOBO
via its plugin interface that remains private and proprietary to the project
partner. Many components of my software ecosystem support extensions through a
plugin interface such that they can be extended without modifying the underlying
functionality.

By default, workflows that implement the partner-specific business needs that
directly interface with their data, systems, and other infrastructure remain
private and proprietary to the project partner.

#### Technology Transfer

Some or all of the following steps might apply for technology transfer:

1. **Initial Delivery** When bringing my technology to a project partner, a
   typical first step is to rely on public hosting infrastructure such as GitHub
   for source code, the Python Package Index (PyPI) for hosting releases, and
   DockerHub for hosting containers along with appropriate usage of lock files,
   SBOMs, and other reproducibility/auditing tools.
2. **Internalization** Depending on project partners' needs, a second step is to
   enable the project partner's team to maintain internal forks of relevant
   components, use an internal package index (e.g., Warehouse, Artifactory), and
   an internal container host (e.g., GitHub, Amazon ECR).
3. **Handoff** In general, I strive to keep my code elegant and well documented,
   and am happy to produce additional training materials, give trainings, etc.
   to support technology transfer.
4. **Support** Alternatively, some partners opt for medium- or long-term service
   contracts.

#### Summary

In practice, this model allows project partners to benefit from a continuously
improving open-source foundation while retaining full control over proprietary
data, integrations, and business logic. Licensing, contribution boundaries, and
handoff expectations are discussed explicitly at project outset and can be
adapted to partner requirements.
