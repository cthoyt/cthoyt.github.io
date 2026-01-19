---
layout: post
title: Why are Semantic Mappings hard?
date: 2026-01-16 11:42:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - knowledge graphs
---

starting on slide 7 of
https://docs.google.com/presentation/d/1stuJbkSbvphYs8fYyj6JJX1JzYvxS4_lernmRovIWTU/edit?slide=id.g2bf67b64f65_0_764#slide=id.g2bf67b64f65_0_764

### Proliferation of Formats

![](/img/mappings-are-hard/formats.png)

### Scattered and partially overlapping

### Different Precision

[![](/img/mappings-are-hard/precision.svg)](https://docs.google.com/drawings/d/1jBK1-FxzfsBFd6Ro0YjQSvwJCZs1rqlLQq9FdtcEU-w/edit?usp=sharing)

### Different Entity Types

mapping between disease ontologies and phenotype ontologies is questionable

### Different Ontology Philosophy

mapping between different disease ontologies is hard because of arguments about
what kind of BFO thing a disease is (disposition, quality, etc.)

### Different Kinds of Evidence

[![](/img/mappings-are-hard/evidence.svg)](https://docs.google.com/drawings/d/1rBofcaQxBFuYX0OzhCvBkigSNFWLclAbQ_X7zG7PRKA/edit?usp=sharing)

### Inexact or Negative

### Mapping Based on Inference or Intent

linguists get really tripped up here.
mapping of logical definition -> use OWL exact match
mapping of meaning -> use SKOS, even if definitions/labels don't really match,
this can be chalked up to imprecision of language.

### Context-dependent interpretation

A gene is a region of a chromosome that encodes a transcript.

[SO:0000704](http://purl.obolibrary.org/obo/SO_0000704)
A protein is a chain of amino acids 


[PR:000000001](http://purl.obolibrary.org/obo/PR_000000001)

Genes represent a combination of the physical region on a chromosome
and the information contained within 

When assembling mechanistic biological knowledge into pathways.

Some mappings may be context-dependent. For example, many knowledge graphs
simplify the complexities of the central dogma of biology and consider
genes and gene products (such as proteins) to be equivalent. However,

![](/img/mappings-are-hard/context-dependent.svg)
