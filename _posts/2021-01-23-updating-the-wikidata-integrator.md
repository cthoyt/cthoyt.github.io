---
layout: post
title: Adding New Literature Sources to the Wikidata Integrator
date: 2021-01-23 21:12:00 +0100
author: Charles Tapley Hoyt
tags: bibliometrics wikidata
---
[Scholia](https://scholia.toolforge.org) is a powerful frontend for summarizing authors, publications, institutions,
topics, etc. that draws content from [Wikidata](https://www.wikidata.org). However, the content that's available in
Wikidata depends on what the community has curated and what has been (semi-) automatically imported. The
[Wikidata Integrator](https://github.com/SuLab/WikidataIntegrator) from the [Su Lab](http://sulab.org) at Scripps
automates the import of bibliometric information from [Crossref](https://www.crossref.org/) and
[Europe PMC](https://europepmc.org/). This blog post is about how I added functionality to import from three prominent
preprint servers in the life sciences ([arXiv](https://arxiv.org/), [bioRxiv](https://www.biorxiv.org/), and
[ChemRxiv](https://chemrxiv.org/)) that can serve as a guide for others who want to have content about their field
included with this tool.

Because it's limited by the content available, it's important to automate importing content

While I've spent a lot of time manually curating information about myself and colleagues, automated

Unfortunately, it's limited by the data that has been manually curated or automatically added, so I've spent lots of
time adding information to make better pages for me, my colleagues, papers we've published, projects we've worked on,
and places we've worked. It turns out that there are also lots of awesome tools for (semi) automatically putting content
there. This blog post is about how

post is about how to add new publication types to the Wikidata Integrator project from the Su lab.

https://github.com/SuLab/WikidataIntegrator

A while back, I wanted to put an arXiv paper I helped co-author on Wikidata, but I didn't want to do it manually, so I
bothered all of the usual suspects until they pointed out that a lot of code has already been written in the Wikidata
Integrator project. THe problem was that it didn't support arXiv, so I had to figure out how it worked and ended up
sending [this pull request](https://github.com/SuLab/WikidataIntegrator/pull/140) to enable it. This blog post is going
to be written as a guide to adding more sources, since at the time of writing it, I'd like to add bioRxiv support but
completely forgot how I did it last time.

1. Add an entry to the `PROPS` dictionary
   in [`wikidataintegrator/wdi_helpers/__init__.py`](https://github.com/SuLab/WikidataIntegrator/blob/c0e16e4ba416979c9a6ae600b4edb2860a2772ed/wikidataintegrator/wdi_helpers/__init__.py#L23-L47)
   . where the key

https://github.com/SuLab/WikidataIntegrator/pull/169
---

I had a lot of fun working on this blog post, and had it was a reminder of the nice discussion I had with Andrew Su last
year. I hope this post enables others to add support for chemRxiv, Preprints.org, and other places where people are
leaving their pre-prints!