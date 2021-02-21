---
layout: post
title: Why Code Notebooks Aren't The Answer
date: 2021-02-22 21:12:00 +0100
author: Charles Tapley Hoyt
tags: reproducibility
---

<blockquote class="twitter-tweet" data-partner="tweetdeck"><p lang="en" dir="ltr">. <a href="https://twitter.com/PLOS?ref_src=twsrc%5Etfw">@PLOS</a> is investigating code notebooks as a way to improve reproducibility. <br><br>Take this survey by <a href="https://twitter.com/PLOSCompBiol?ref_src=twsrc%5Etfw">@PLOSCompBiol</a> to help inform the effort <a href="https://t.co/lzzJnPcLyg">https://t.co/lzzJnPcLyg</a></p>&mdash; Nikolai Slavov (@slavov_n) <a href="https://twitter.com/slavov_n/status/1363127377610625026?ref_src=twsrc%5Etfw">February 20, 2021</a></blockquote>

Laboratory scientists apply protocols from the literature, keep immaculate logs of their actions,
and thoroughly report what they did when they write manuscripts.

Links:

- https://survey.alchemer.com/s3/6147858/Interactive-Code-Notebooks-Survey
- https://theplosblog.plos.org/2021/02/exploring-code-notebooks-through-community-focused-collaboration

I believe there's a huge fallacy in using code notebooks (e.g., Jupyter notebooks) as a way of
sharing research. I believe they are an exceptional tool for hacking and research, but the inherent
interactivity of notebooks leads most researchers to writing code that can not be re-run from top to
bottom. Additionally, writers of notebooks often put very large functions (as seen in the example
notebook along with this survey) inside the notebook. This makes it difficult (if not impossible,
depending on the code quality standards of the author) to assess the domain logic behind the
analysis. Many times, this is the result of needing dozens of lines of code to create a nice image.
I am not advocating for authors to use less code for these purposes, but this code does not belong
in the notebook. This code belongs in a packaged context that can be imported in a notebook and run.
For scientists who are not familiar with packaging code, there are many resources available. As a
side node, I have spent lots of time generating resources and educating people in exactly this sort
of thing. It takes time and scientists have to learn a new skill set, but most enjoy the long term
benefits after initial skepticism. Ultimately, code that generates a plot can be stored in a
function in a package, imported, and simply called in the notebook. This allows a reader of the
notebook to understand the high-level logic of the work presented, and forces the author to organize
the code in a way such that a careful reviewer then knows exactly where to look for the details of
the implementation. The same can be said about the analytical portions of the code notebook - there
should not be auxiliary functions defined in the notebook itself. All should be imported from a
package context. This is true not only for Python, which is the popular choice of programming
language in computational science, but also R, Julia, and others.

## Separation of Methods and Application

Further, I advocate for the separation of the code that implements a given analysis from the
analysis itself. Many authors who share their code on a service like GitHub present both the
analytical code and results in the same repository. I believe that the analysis itself should be in
a separate repository, so it can focus only on data preprocessing, application of analysis (from a
high level), and presentation of results. The code notebook presents an alternative where the
analytical and visualization code can be in its own repository, which is imported in the notebook
and applied to the specific problem presented in the notebook itself.

With regards to data - if a manuscript relies on data to do its analysis, there should be a link to
a stable repository like Zenodo or Figshare. Alternatively, if data is processed from a primary
source, the code that does the processing should be available as well as the derived product,
assuming licensing permits. For example, cheminformatics papers often present analysis on data 
"derived from ChEBML" but very few reports the way they derived the data either in the methodology
sections of their papers, or more importantly, with the code that actually did it.

## Intractable Problems in Reproducibility

- when a machine learning model takes 3 months to train and costs thousands of dollars, a reviewer
  can't actually re-run to see it does what it says it does. Similarly to the problem with
  NP-completeness, we need ways to review that the results are good that are more efficient than
  just getting the solution itself.
- papers that are published using proprietary/closed source/paid software that are not generally
  available can't be reproduced, and they shouldn't be. the solution here is for journals to desk
  reject these kinds of papers and implore companies to publish white papers instead, that do not
  have the guise of science. I'm not sure what to say to academic labs who are engaging in this kind
  of practice except for :smh:
  