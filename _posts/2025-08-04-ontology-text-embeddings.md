---
layout: post
title: Text-based Embeddings of Ontology Terms
date: 2025-08-05 9:32:00 +0200
author: Charles Tapley Hoyt
tags:
  - ontology
  - embeddings
  - bert
  - sbert
  - similarity
  - cosine similarity
---

The [Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/) is now indexing
dense embeddings for ontology terms that it constructs from term labels,
synonyms, and descriptions using LLMs. I maintain a Python client library for
the OLS (aptly named [`ols-client`](https://github.com/cthoyt/ols-client)) and
was asked to implement a wrapper to the API endpoint that looks up those
embeddings. This post is a demo of how to do that, and how I replicated the same
embedding functionality with [PyOBO](https://github.com/biopragmatics/pyobo) to
extend it to ontologies and databases not in OLS.

I've been [working on modeling clinical
trials]({% post_url 2025-01-23-clinical-trials-data-modeling %}) in
collaboration with [Sebastian Duesing](https://github.com/sebastianduesing) at
the [Ontology for Biomedical Investigations (OBI)](https://bioregistry.io/obi),
so I'm going to use the OBI term for
[clinical trial (OBI:0003699)](https://www.ebi.ac.uk/ols4/ontologies/obi/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FOBI_0003699)
that we recently minted together as an example.

## Embeddings from OLS

Below is a screenshot of the OLS page for this term, as of August
4<sup>th</sup>, 2025:

![ols-clinical-trial-2025-08-04.png](/img/ols-clinical-trial-2025-08-04.png)

There's a newly added section on similar terms. Here's what it says about these:

> Similarity results are derived from LLM embeddings and have not been manually
> curated. Model:
> [text-embedding-3-small](https://platform.openai.com/docs/models/text-embedding-3-small)

From a first glance, the results here have very high precision. This shouldn't
be surprising, considering that labels, synonyms, and descriptions contain very
high signal. Of course, there's room for arguing about the nuance of ontological
differences, but this is a largely unhelpful discussion in my experience when
the goal is to do ontology merging and data integration. In [my recent
post]({% post_url 2025-01-23-clinical-trials-data-modeling %}) where I described
the landscape of clinical trial modeling in the OBO Foundry and related
biomedical ontologies, I actually had already curated several of these semantic
mappings by hand, which I'm hoping to
[add to OBI via SSSOM](https://github.com/obi-ontology/obi/issues/1893). Looking
forward for the OLS, it would be great if there were a mini curation interface
where these could be confirmed or rejected as exact mappings, and persist the
resulting curations as SSSOM.

There was [a request](https://github.com/cthoyt/ols-client/issues/9) to expose
the embeddings via my OLS client package, which I solved with only a few lines
of code [here](https://github.com/cthoyt/ols-client/pull/10/files). Now, you can
get the embedding for _clinical trial_ (or any other term, based on the
ontology/IRI combination) as a list of floating point numbers:

```python
from ols_client import EBIClient

client = EBIClient()
embedding: list[float] = client.get_embedding(
    "obi", "http://purl.obolibrary.org/obo/OBI_0003699"
)
```

The next step is to be able to calculate the similarity between two terms, which
can be done between the OBI term for _clinical trial_, and the
[National Cancer Institute Thesaurus (NCIT)](https://bioregistry.io/ncit) term
for clinical trial as a single floating point number:

```python
from ols_client import EBIClient

client = EBIClient()
similarity: float = client.get_embedding_similarity(
    "obi",
    "http://purl.obolibrary.org/obo/OBI_0003699",
    "ncit",
    "http://purl.obolibrary.org/obo/NCIT_C71104",
)
```

## Embeddings from PyOBO

Personally, I think using an OpenAI model is a bit overkill for two reasons.
First, there are smaller, non-large language models like
[BERT](https://huggingface.co/docs/transformers/en/model_doc/bert) that can get
the same job done. Second, they're free to download and can be run on commodity
hardware, versus needing to pay OpenAI for access to their embeddings.
Specifically, I've been looking at [SBERT (Sentence-BERT)](https://sbert.net),
which is a variant of the BERT architecture that works better on sentences and
can be easily used via the
[`sentence-transformers`](https://pypi.org/project/sentence-transformers/)
Python package.

I've developed the [`pyobo`](https://github.com/biopragmatics/pyobo) package,
which gives unified access to ontologies and databases that are ontology-like.
It has functionality for getting the labels, synonyms, and descriptions for
terms in both.

It wasn't difficult to
[re-implement the same functionality as the OLS in PyOBO](https://github.com/biopragmatics/pyobo/pull/412)
such that it can be run locally on a larger variety of resources. Here's the
same lookup for text embedding and similarity:

```python
import pyobo

>>> pyobo.get_text_embedding("OBI:0003699")
[-5.68335280e-02  7.96175096e-03 -3.36112119e-02  2.34440481e-03 ... ]

>>> pyobo.get_text_embedding_similarity("OBI:0003699", "NCIT:C71104")
0.24702128767967224
```

This could be improved with the ability to do batch lookup, which is probably
the way people would want to use this functionality. Even better, because of how
ML is implemented on GPUs and related hardware, batching effectively comes for
free, only limited by memory contraints.

---

Text embeddings aren't the end - I've been working for years on graph machine
learning, and specifically knowledge graph embedding models. A lot of the
methodological and software engineering ideas have gone into the
[PyKEEN](https://github.com/pykeen/pykeen) library. I'm interested in ways to
jointly leverage text- and graph embeddings, one of which is demonstrated with
Michael Galkin's
[NodePiece](https://pykeen.readthedocs.io/en/stable/tutorial/inductive_lp.html)
model.
