---
layout: post
title: Representing Negative Knowledge
date: 2025-10-07 23:18:00 +0200
author: Charles Tapley Hoyt
tags:
  - knowledge graphs
---

Representing negative knowledge in the semantic web is an open problem. This
post is going to be a living document where I keep notes on use cases, potential
solutions, and awful hacks.

## SSSOM

In the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/),
we decided to represent negative knowledge by adding a modifier onto a
predicate. This means that a semantic mapping known to be false gets represented
like this in TSV:

```tsv
subject_id	subject-label	predicate_id	predicate_modifier	object_id	object_label	mapping_justification
CHEBI:8925	ryanodine	skos:exactMatch	Not	mesh:D031309	Ryania	semapv:ManualMappingCuration
```

Since SSSOM is heavily tied to the OBO community, this gets turned into RDF with
the following axiom:

```turtle
[] a owl:Axiom ;
    owl:annotatedSubject CHEBI:8925 ;
    owl:annotatedProperty skos:exactMatch ;
    owl:annotatedObject mesh:D031309 ;
    sssom:predicate_modifier sssom:NegatedPredicate .
```

It's debated whether asserting an axiom also requires the assertion of the
triple itself `CHEBI:8925 skos:exactMatch mesh:D031309`, however, in this case,
it's clear that triples represent true knowledge, so we would not want to
concretize it.

## RDF Surfaces

Damien Goutte-Gattat made me aware of
[RDF Surfaces](https://www.semantic-web-journal.net/system/files/swj3799.pdf) in
a
[discussion on a SSSOM PR](https://github.com/mapping-commons/sssom/pull/469/files#r2382049109).
To summarize his comment, RDF surfaces create a part of an RDF graph that
contains negated assertions, something like:

```n3
@prefix log: <http://www.w3.org/2000/10/swap/log#> .
@prefix FBbt: <http://purl.obolibrary.org/obo/FBbt_> .
@prefix UBERON: <http://purl.obolibrary.org/obo/FBbt_> .
@prefix skos: http://www.w3.org/2004/02/skos/core#> .

(_:x) log:onNegativeSurface {
  FBbt:00004508 skos:exactMatch UBERON:0000056 .
} .
```

This paper is still
[under review](https://www.semantic-web-journal.net/content/rdf-surfaces-enabling-classical-negation-and-first-order-expressivity-semantic-web)
and also might be of limited use because it uses sneaky N3 syntax `{` `}` which
are used to express [formulae](https://www.w3.org/TeamSubmission/n3/#Quoting).

---

I haven't actually gone out to do a deep survey on this. If you are aware of
something relevant, please let me know.
