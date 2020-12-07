---
layout: post
title: Generating Testing Knowledge Graphs with Literals
date: 2020-12-07 00:00:00 -0800
author: Charles Tapley Hoyt
---
[PyKEEN](https://github.com/pykeen/pykeen/) has a wide variety of functionality related
to knowledge graph embedding models  and handling various sources of knowledge graphs.
This post describes the journey towards  properly testing the functionality of an exotic
set of knowledge graph embedding models  that incorporate feature vectors for entities
via triples with numeric literals.

PyKEEN implements the [LiteralE](https://github.com/SmartDataAnalytics/LiteralE) class of
knowledge graph embedding models that allow for the inclusion of numeric features for each
entity. It then combines these features with the embedding for each entity using the `g`
function before calculating a score using an arbitrary interaction function. In the
[original paper](https://arxiv.org/abs/1802.00934), Kristiadi *et al.*  used the interaction
functions from the DistMult and ComplEx.

Unfortunately, the original paper used three datasets for benchmarking: FB15k-237, WN18RR,
and YAGO3-10. While these aren't the largest datasets PyKEEN can handle, they are too big
to be used during unit testing, which should run very quickly and be as minimal as possible.
Therefore, we punted writing proper tests for LiteralE models because of the lack of availability
of a small, well-studied dataset like Nations or Kinships.

Today, that came to bite us in the butt because we decided to improve the implementation
of the underlying interface for loading triples from files
(see [pykeen/pykeen#193](https://github.com/pykeen/pykeen/pull/193)). That meant that it
was time to set off on creating a dataset that was small and had literals  in it and
implementing proper tests for the LiteralE models.

My first idea was to take an arbitrary dataset, like Nations, and generate random features
for it. I implemented an algorithm that created (slightly meaningful) random
representations, but then [@mberr](https://github.com/mberr/) gave the excellent suggestion that the CIA's
[World FactBook](https://www.cia.gov/library/publications/the-world-factbook/) contains all sorts of
information for each country in tabular form, and that I could use that to extend the Nations dataset
to have literals. I did the dirty work of grabbing some features (area, population, etc.) for
the ten entities in the Nations dataset then a bit of improvement on the underlying PyKEEN code
for dataset loading. It all come to fruition in [pykeen/pykeen#199](https://github.com/pykeen/pykeen/pull/199)
where @mberr helped update the LiteralE implementations, but he rightfully pointed out that my
random dataset generation code was no longer necessary and didn't belong in the pull request.

Luckily, I have a blog, which seems like a great place to share my code and my thought process!

## Generating Random Literals

The algorithm was the following:

1. Pick a pre-existing dataset
2. Train a knowledge graph embedding model on the dataset
3. Generate a random transformation matrix that can be multiplied by each entity's embedding to
   generate a feature
4. Apply a bit of noise
5. Assign each feature a random name and write to a file whose rows are in the form of
   <entity> <random feature name> <random feature value>

While it would have been possible to directly generate random values for each dummy
feature, using a transformation on the entity embeddings means that each feature will
have some correlation to the embeddings itself, which could be useful for testing later.

I've posted the code to Gist in case we ever need it again. Please feel free to reuse,
this code is under the MIT License.

<script src="https://gist.github.com/cthoyt/fc0032168607b5b8bad342393fed0773.js"></script>
