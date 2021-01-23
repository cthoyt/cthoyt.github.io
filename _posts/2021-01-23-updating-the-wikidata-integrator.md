---
layout: post
title: Adding New Literature Sources to the Wikidata Integrator
date: 2021-01-23 21:12:00 +0100
author: Charles Tapley Hoyt
tags: bibliometrics wikidata
---
[Scholia](https://scholia.toolforge.org) is a powerful frontend for summarizing authors, publications, institutions,
topics, etc. that draws content from [Wikidata](https://www.wikidata.org). However, the content that's available in
Wikidata depends on what has been manually curated by community members and what has been (semi-) automatically imported
by scripts and bots. The [Wikidata Integrator](https://github.com/SuLab/WikidataIntegrator) from the
[Su Lab](http://sulab.org) at Scripps automates the import of bibliometric information from
[Crossref](https://www.crossref.org/) and [Europe PMC](https://europepmc.org/). This blog post is about how I added
functionality to it to import from three prominent preprint servers in the natural sciences
([arXiv](https://arxiv.org/), [bioRxiv](https://www.biorxiv.org/), and [ChemRxiv](https://chemrxiv.org/)) that can serve
as a guide to others who want to have content about their field included with this tool.

A while back, I wanted to put an arXiv paper
about [the role of metadata in reproducible computational research](https://arxiv.org/abs/2006.08589) that I co-authored
with Jeremy Leipzig ([@jermdemo](https://twitter.com/jermdemo)) on Wikidata so it would appear
on [my Scholia page](https://scholia.toolforge.org/author/Q47475003), but I didn't want to do it by hand. I had already
had good experiences using Magnus Manske's [SourceMD](https://sourcemd.toolforge.org/),
[Author Disambiguator](https://author-disambiguator.toolforge.org), and related tools for queuing import of
peer-reviewed papers with PubMed identifiers or digital object identifiers (DOIs), ORCID identifiers of co-authors, and
ultimately assisted disambiguation of author names.

The only problem was that the SourceMD tool doesn't deal with preprints. As an aside, both bioRxiv and ChemRxiv assign
DOIs to their preprints that can be queried through Crossref, but this doesn't exactly solve the problem of handling
preprints in a special way, and it doesn't solve the problem for arXiv. I asked around on Twitter and was turned towards
the Wikidata Integrator project, which already supported building both general pipelines for automating content import
in Wikidata and a specific one for publications. All I had to do was figure out how it works, and get hacking! I ended
up sending three pull requests.

| Server   | Pull Request                                                                         |
|----------|--------------------------------------------------------------------------------------|
| arXiv    | [SuLab/WikidataIntegrator#140](https://github.com/SuLab/WikidataIntegrator/pull/140) |
| bioRxiv  | [SuLab/WikidataIntegrator#169](https://github.com/SuLab/WikidataIntegrator/pull/169) |
| ChemRxiv | [SuLab/WikidataIntegrator#140](https://github.com/SuLab/WikidataIntegrator/pull/170) |

At the time of writing, the arXiv and bioRxiv ones have been accepted, and the ChemRxiv one is waiting for review - I
think the maintainer was busy at a conference this week, and now I'm writing on a Saturday. In another unrelated pull
request to the project, I added a vanity CLI, so when you install the code with `pip install wikidataintegrator`,
a program `wikidataintegrator-publication` is installed for direct usage from the shell. It can be used like this:

```shell
$ wikidataintegrator-publication --idtype arxiv 2101.05136
$ wikidataintegrator-publication --idtype biorxiv 2020.08.20.259226
$ wikidataintegrator-publication --idtype chemrxiv 13607438
```

If you're using a DOI or PubMed identifier as the `--idtype`, you also have to specify a `--source`, but since each
of arXiv, bioRxiv, and ChemRxiv have their own custom sources, this isn't necessary.

## Implementing a New Importer

1. Add an entry to the `PROPS` dictionary
   in [`wikidataintegrator/wdi_helpers/__init__.py`](https://github.com/SuLab/WikidataIntegrator/blob/c0e16e4ba416979c9a6ae600b4edb2860a2772ed/wikidataintegrator/wdi_helpers/__init__.py#L23-L47)
   . where the key

https://github.com/SuLab/WikidataIntegrator/pull/169
---

I had a lot of fun working on this blog post, and had it was a reminder of the nice discussion I had with Andrew Su last
year. I hope this post enables others to add support for chemRxiv, Preprints.org, and other places where people are
leaving their pre-prints!