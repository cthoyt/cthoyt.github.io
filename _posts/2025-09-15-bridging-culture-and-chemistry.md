---
layout: post
title: Bridging NFDI's culture and chemistry knowledge graphs
date: 2025-09-15 17:45:00 +0200
author: Charles Tapley Hoyt
tags:
  - knowledge graphs
  - sparql
---

At the sixth NFDI4Chem consortium meeting,
[Torsten Schrade](https://www.adwmainz.de/personen/mitarbeiterinnen/profil/torsten-schrade.html)
from the NFDI4Culture consortium gave a lovely and whimsical talk entitled _A
Data Alchemist's Journey through NFDI_ which explored ways that we might
federate and jointly query both consortia's knowledge via their respective
SPARQL endpoints. This post is about the steps I took to operationalize his toy
example of connecting paintings depicting alchemists trying to make gold to
experiments using gold as a reactant or catalyst, or more generally to
accomplish this for any chemical or compound covered by the Iconclass
vocabulary.

## Operationalizing Iconclass

[Iconclass](https://iconclass.org) is a controlled vocabulary used to annotate
parts of images with what they depict. For example,
[`iconclass:49E3911`](https://bioregistry.io/iconclass:49E3911) is used to
annotate a part of an image depicting an _alchemist trying to make gold_.
Iconclass identifiers implicitly contain the hierarchy:

- [`iconclass:49E391`](https://bioregistry.io/iconclass:49E391) is used to
  annotate an _alchemist at work_
- [`iconclass:49E39`](https://bioregistry.io/iconclass:49E39) is used to
  annotate _alchemy_
- [`iconclass:49E3`](https://bioregistry.io/iconclass:49E3) is used to annotate
  _chemistry_
- [`iconclass:49E`](https://bioregistry.io/iconclass:49E) is used to annotate
  _science and technology_
- [`iconclass:49`](https://bioregistry.io/iconclass:49) is used to annotate
  _education, science, and learning_
- [`iconclass:4`](https://bioregistry.io/iconclass:4) is used to annotate
  _Society, Civilization, Culture_

Note that unlike an ontology, the hierarchy implied by Iconclass is merely
organizational and isn't (formally) logical.

[![](/img/iconclass-alchemist.png)](https://bioregistry.io/iconclass:49E391)

I added a source to PyOBO to ingest Iconclass in
[biopragmatics/pyobo#433](https://github.com/biopragmatics/pyobo/pull/433). This
enables it to generate ontology-like artifacts in the OWL and OBO formats, as
well as gives access to the text mining utilities built on top of PyOBO.

Along the way, I found that Iconclass has a lot more weird and irregular
identifiers than I had earlier assumed. I was able to make an additional pull
request to the Bioregistry in
[biopragmatics/bioregistry#1686](https://github.com/biopragmatics/bioregistry/pull/1686)
to update the underlying regular expression pattern and add extra examples to
demonstrate the weirdness. This is important because PyOBO uses the Bioregistry
for regular expression validation of identifiers internally, and without this
update, the Iconclass source doesn't work!

## Curating Semantic Mappings

The [Biomappings](github.com/biopragmatics/biomappings) project provides tools
for predicting semantic mappings using lexical matching. It can quickly be used
to spin up a workflow for matching any two vocabularies available through PyOBO
with a few lines. I gave it a try to match Iconclass to the
[Chemical Methods Ontology (CHMO)](https://bioregistry.io/chmo):

```python
from biomappings.lexical import lexical_prediction_cli

if __name__ == "__main__":
    lexical_prediction_cli(__file__, "iconclass", "chmo")
```

This usually works well for matching entities in resources curated as
ontologies, but because Iconclass's labels aren't typical, it wasn't able to
generate more than a handful of matches.

This prompted me to take a different approach that relies on language models to
generate embeddings, which are better able to capture the subtle differences in
the way entities are labeled. This led me to making an improvement in

1. I added functionality to PyOBO to get a dataframe of embeddings for _all_
   entities in a given ontology or controlled vocabulary in
   [biopragmatics/pyobo#434](https://github.com/biopragmatics/pyobo/pull/434)
2. I extended the lexical prediction workflow in Biomappings to have a method
   that combines embedding generation in PyOBO with similarity calculation and
   finally the application of a similarity cutoff for calling mappings in
   [biopragmatics/biomappings#206](https://github.com/biopragmatics/biomappings/pull/206).

After this, I was able to update my workflow to look like this:

```python
from biomappings.lexical import lexical_prediction_cli

if __name__ == "__main__":
    lexical_prediction_cli(
        __file__,
        "iconclass",
        "chmo",
        method="embedding",
        cutoff=0.9
    )
```

## Federated Queries

- automate turning SSSOM into RDF
- Making a federated query 3 ways between chem, culture, and the bridge that
  finds links between culture objects tagged with icon classes mapped to
  chemicals mapped to notebooks.
