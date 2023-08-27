---
layout: post
title: Reproducibility Pilot in the Journal of Cheminformatics
date: 2023-08-27 00:00:00 -0800
author: Charles Tapley Hoyt
tags: cheminformatics reproducibility
---

I've been working on improving reproducibility in the field of cheminformatics for some time now.
For example, I've written posts about making data from
[DrugBank]({% post_url 2020-12-14-taming-drugbank %}) and
[ChEMBL]({% post_url 2021-08-05-taming-chembl-sql %}) more actionable. Over the last year, I've been preparing a concept
with the editors of the [Journal of Cheminformatics](https://jcheminf.biomedcentral.com) on how to
include an assessment of reproducibility to reviews of manuscripts submitted to the journal. This
has resulted in an
editorial [Improving reproducibility and reusability in the Journal of Cheminformatics](https://doi.org/10.1186/s13321-023-00730-y)
as well as a [call for papers](https://www.biomedcentral.com/collections/irrijc). In this post, I want to
summarize the first generation review criteria we developed, give an example of it applied in practice

## The Seven (First Generation) Criteria

There are many potential directions for reproducibility. Given the fact that typical computational scientists
are not trained as software engineers, we decided on seven very simple criteria that can be easily reviewed
and easily addressed:

1. Does the repository contain a LICENSE file in its root?
2. Does the repository contain a README file in its root?
3. Does the repository contain an associated public issue tracker?
4. Has the repository been externally archived on [Zenodo](https://zenodo.org/), [FigShare](https://figshare.com/), or
   equivalent that is referenced in the README?
5. Does the README contain installation documentation?
6. Is the code from the repository installable in a straight-forward manner?
7. Does the code conform to an external linter (e.g., [`black`](https://github.com/psf/black) for Python)?

These correspond to important details that are complementary to other considerations of reproducibility, but often
overlooked. Throughout the pilot, the editors and reviewers will try to support authors in addressing each of these
points during revision. I imagine that there will be future iterations of these criteria as the community begins
to expect these as standard practice. For example, we can narrow criteria 1 to specifically say that the software
should be licensed with an OSI-approved license and not accept science made with non-open licenses. We could
further narrow point 7 to have additional community style requirements (e.g., passes parts of `flake8`, as you know I
love from my post [on flake8 hell]({% post_url 2020-04-25-how-to-code-with-me-flake8 %})). We could also include
additional guidelines that e.g. say that the results presented in the paper should be reproducible with a single
command from the command line, e.g., a shell script. The rabbit hole could go very deep, so again, it's worth
saying that these are very non-controversial criteria for the first generation.

That being said, many repositories don't follow these! Since these criteria are so simple, I'm interested in automating
their assessment and further applying it to the entire Journal of Cheminformatics backlog. I'll describe this more in
a future post.

Without further ado, the text below is what I sent verbatim in the review
for [Drug-Protein Interaction Prediction via Multi-View Variational Autoencoder and Cascade Deep Forests](https://doi.org/10.21203/rs.3.rs-3242419/v1),
which is pre-printed on Research Square and has associated code [here](https://github.com/Macau-LYXia/MVAE-DFDTnet). I
have tried my best to include actionable links and information with each piece. I would like to also automate sending
separate GitHub issues for each of these points as a more concrete to-do list for authors, then also send an "epic"
issue that lists all of them together. With the magic of the GitHub API, this is possible.

## My First Reproducibility Review for the Reproducibility Pilot

Below, I apply the seven point reproducibility review prescribed by
[Improving reproducibility and reusability in the Journal of Cheminformatics](https://doi.org/10.1186/s13321-023-00730-y)
to the default branch of repository https://github.com/Macau-LYXia/MVAE-DFDTnet
(commit [c0858c8](https://github.com/Macau-LYXia/MVAE-DFDTnet/commit/c0858c8cdf61d62f945fbd74d0d60f2531394287)),
accessed on August 27<sup>th</sup>, 2023.

1. **Does the repository contain a LICENSE file in its root?**<br/>
   No. The GitHub license picker can be used to facilitate adding one by following this
   link: https://github.com/Macau-LYXia/MVAE-DFDTnet/community/license/new?branch=main. Ideal software licenses for open
   source software include the MIT License, BSD family of licenses, and other licenses approved by
   the [Open Source Initiative](https://opensource.org/licenses). A simple, informative guide for picking a license can
   be found at https://choosealicense.com.
2. Does the repository contain a README file in its root?<br/>
   No. A minimal viable README file contains:
    - A short, one line description of the project
    - Information on how to download, install, and run the code locally
    - Brief documentation describing the single most important use case for the repository. For scientific code, this is
      ideally a one-liner in Python code, a shell script, or a command line interface (CLI) that can be used to
      reproduce the results of the analysis presented in a corresponding manuscript, use the tool presented in the
      manuscript, etc.
    - Link to an archive on an external system like Zenodo, FigShare, or an equivalent.
    - Citation information, e.g., for a pre-print then later for a peer reviewed manuscript

   GitHub can be used to create a README file
   with https://github.com/Macau-LYXia/MVAE-DFDTnet/new/main?filename=README.md. Repositories typically use the
   Markdown format, which is
   explained [here](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).
3. Does the repository contain an associated public issue tracker?<br/>
   Yes. It is available at https://github.com/Macau-LYXia/MVAE-DFDTnet/issues.
4. Has the repository been externally archived on Zenodo, FigShare, or an equivalent that is referenced in the
   README?<br/>
   No, there is no README. This is also not mentioned in the manuscript.
   See https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content for a
   tutorial on how to do this.
5. Does the README contain installation documentation?<br/>
   No, there is no README. This is also not mentioned in the manuscript.
6. Is the code in the repository installable in a straight-forward manner?<br/>
   No, the code is not laid out in a typical structure, e.g., as described
   in https://blog.ionelmc.ro/2014/05/25/python-packaging. Further, there is no setup configuration that encodes the
   dependencies or facilitates reuse of the code.
7. Does the code in the repository conform to an external linter (e.g., `black` for Python)?<br/>
   No. The Python code has not been linted, e.g., using [`black`](https://github.com/psf/black). Similarly, the Matlab
   code has not been linted, e.g. using [`checkcode`](https://de.mathworks.com/help/matlab/ref/checkcode.html).

Scientific integrity depends on enabling others to understand the methodology (written as computer code) and reproduce
the results generated from it. This reproducibility review reflects steps towards this goal that may be new for some
researchers, but will ultimately raise standards across our community and lead to better science. Because the work
presented in this article only yet address one of the seven points of the reproducibility review, I recommend rejecting
the article and inviting later resubmission following addressing the points.

For posterity, this review has also been included on https://github.com/Macau-LYXia/MVAE-DFDTnet/issues/1.

## The Future is Looking Good

The example above isn't so great - it's possible that these authors have never considered most of these points
about reproducibility before. The reality is that many computational scientists are not trained in this since their
mentors were not primarily trained as computational scientists themselves. Combine with the perverse incentive
structure, it's understandable how this can be left out from some publications. I experienced something similar in my
doctoral studies, and had to bootstrap my own philosophy on reproducibility as well as the practical skills to achieve
it.

That all being said, we are now entering an era where progressive and newly minted PIs actually have training as
computational scientists. The next paper in my queue for a reproducibility review is for
https://github.com/Steinbeck-Lab/cheminformatics-python-microservice, which will pass the 7 criteria with flying colors.
I'm looking forward to the future when we expect more excellent science on the regular. See you there!

---
I'm not sure how people will view the way I talk about reviews - I am quite open with posting reviews on GitHub and also
openly discussing the fact that I've reviewed something. Ideally, I don't accept reviews for papers that don't have
pre-prints, since I personally think the review process should be open. I hope it's the case that I haven't been rude
or unfair. If that's the case, someone can help me change the way I write about these topics.