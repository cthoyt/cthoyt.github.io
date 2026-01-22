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

#### What I Bring With Me

I maintain a comprehensive set of
[free/libre and open-source software (FLOSS)](https://www.gnu.org/philosophy/floss-and-foss.en.html)
packages for the standardization, integration, and analysis of data and
knowledge. These are typically licensed using business-friendly
[Open Source Initiative (OSI)](https://opensource.org/licenses)-approved
licenses such as the MIT and Apache 2.0 license. Until now, I have avoided using
[copyleft licenses](https://www.gnu.org/licenses/copyleft.en.html) to reduce
issues with private/internal/proprietary forks.

For example, the [Biopragmatics Stack](https://github.com/biopragmatics)
packages these components for use in the generation and application of
biomedical knowledge graphs, e.g., in early stage drug discovery. Have a look at
my [blog](..) for insight into various components of the Biopragmatics Stack and
related, domain-agnostic tooling that I develop and maintain.

#### Open Source vs. Internal

I expect that during projects, whether public or private, I will maintain and
make (generic) extensions to components as open source contributions to the
appropriate public repositories. For example, if a project requires the addition
of a new public database to [PyOBO](https://github.com/biopragmatics/pyobo),
then I would directly incorporate it into the public PyOBO repository.

Conversely, if a project requires the addition of an internal, proprietary, or
otherwise private database to PyOBO, then I would incorporate it into PyOBO via
PyOBO's plugin interface. The resulting code that implements the plugin would
remain internal and proprietary to the project partner.

In general, the various components of my software stack are pluggable in this
manner such that they can be extended without modifying the underlying public
codebase.

I find that the value I can bring to project partners is the experience and
knowledge of how to use existing software, the ability to extend it, and most
importantly, the ability to create custom workflows that fit the business needs
of project partners. As such, code that works with internal data, integrates
with internal systems, or accomplishes business-driven objectives is
interal/proprietary by default.

#### Technology Transfer

When bringing my technology to a project partner, a typical first step is to
rely on public hosting infrastructure such as GitHub for source code, the Python
Package Index (PyPI) for hosting releases, and DockerHub for hosting containers
along with appropriate usage of lock files, SBOMs, and other
reproducibility/auditing tools.

Depending on project partners' needs, a second step is to enable the project
partner's team to maintain internal forks of relevant components, use an
internal package index (e.g., Warehouse, Artifactory), and an internal container
host (e.g., GitHub, Amazon ECR). In general, I strive to keep my code elegant
and well documented, and am happy to produce additional training materials, give
trainings, etc. to support technology transfer. Alternatively, some partners opt
for medium- or long-term service contracts.

Code that I write for working code that works with internal data, integrates
with internal systems, or accomplishes business-driven objectives is
internal/proprietary by default. Project partners take responsibility for this
code at the end of projects, but similarly, I strive to make this code elegant,
well-documented, and easy to hand over.
