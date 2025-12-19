---
layout: post
title: Getting started annotating PubMed
date: 2025-12-19 12:01:00 +0100
author: Charles Tapley Hoyt
tags:
  - named entity recognition
  - text mining
  - natural language processing
  - named entity normalization
  - medical subject headings
  - MeSH
  - PubMed
  - PyOBO
  - SSSLM
---

Text mining used to be hard - getting text content, preparing dictionaries, and applying pre-existing implementations
were all a drag.

I've been building software for the last ten years that simplifies and democratizes access to these resources.
Here, I'm going to highlight three components:

1. `pubmed-downloader` provides a wrapper around PubMed's API and around bulk download and processing of the source data
2. `ssslm` provides a wrapper around named entity recognition (NER) methods such as `gilda` and `spacy`
3. `pyobo` provides a wrapper around fetching and processing ontologies, controlled vocabularies, databases, and other
   resources that can be used as a dictionary. It also has a high-level workflow, `pyobo.get_grounder()` for getting content into `ssslm`.

The following is a demonstration on how to get the abstracts of articles from PubMed, perform named entity
recognition (NER) using Medical Subject Headings (MeSH), and output the results as a table:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "click>=8.3.1",
#     "pubmed-downloader>=0.0.12",
#     "pyobo>=0.12.13",
#     "ssslm>=0.1.3",
#     "tabulate>=0.9.0",
# ]
# ///

import click
import pubmed_downloader
import pyobo
import ssslm
from tabulate import tabulate

# get a grounder loaded up with a specific version of MeSH.
# if you don't specify a version, the latest will be used.
grounder: ssslm.Grounder = pyobo.get_grounder("mesh", version="2018")

# get ten PubMed identifiers about diabetes. note that the
# PubMed API has been horrifically slow lately, so either
# be patient or consider processing PubMed in bulk, which
# is also slow, but more consitent
pubmed_ids: list[str] = pubmed_downloader.search("diabetes", backend="api", retmax=5)
click.echo(f"got {len(pubmed_ids)} pubmed IDs")

results = []
for article in pubmed_downloader.get_articles(pubmed_ids, error_strategy="skip", progress=True):
    abstract = article.get_abstract()

    # get a list of annotations, which contain the offsets of the entity
    # and the grounding to a Bioregistry-standardized CURIE
    annotations = grounder.annotate(abstract)

    # fill up a list for creating a table later
    for annotation in annotations:
        results.append((
            annotation.start,
            annotation.end,
            annotation.curie,
            annotation.name,
            round(annotation.score, 2),
            annotation.text,
        ))

click.echo(tabulate(results, headers=['start', 'end', 'curie', 'name', 'score', 'abstract'], tablefmt="github"))
```

Here are the results:
