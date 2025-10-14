---
layout: post
title: HGNC as an ontology
date: 2025-10-14 10:14:00 +0200
author: Charles Tapley Hoyt
tags:
  - ontology
  - OWL
  - genes
  - HGNC
---

This is a post about how I converted HGNC to OWL

## PyOBO

1. original motivation
2. code examples, what does PyOBO get you
3. formats, need to move beyond OWLAPI/ROBOT since development is not accessible outside java world, want to reuse
   parsers (similar to OAK)

## Lexicalization

Related discussions:

- https://github.com/information-artifact-ontology/ontology-metadata/pull/197#discussion_r2428235955

## Logical Axioms

```mermaid
graph LR
    genegroup[Gene Group\nHGNC] -- " member of\n(RO:0002350) " --- gene[Gene]
    geneclass[Gene Class\nSO] -- is a --- gene
    gene -- " transcribed to\n(RO:0002511) " --> rna[RNA\nRNA Central, miRBase, snoRNABase]
    gene -- " has gene product\n(RO:0002205) " --> protein[Protein\nUniProt]
    gene -- " has exact match\n(skos:exactMatch) " --> external1[External\nNCBIGene, Ensembl, Orphanet, OMIM, RefSeq,...]
    gene -- " has database cross-reference\n(oboInOwl:hasDbXref) " --> externa2[External\nCCDS,...]
    gene -- " is orthologous to\n(RO:HOM0000017) " --> orthology[Orthologous Gene\nMGI, RGD]
    gene -- " gene product is member of\n(RO:0002205 + RO:0002350) " --> enzyme[Enzyme\nEC]
    gene -- " located in\n(RO:0001025) " --> chr[Chromosome Region\nCHR]
```

The relationship between a gene and its group is also unclear.

The relationship between a gene and an enzyme is currently mediated by
a property chain. In order to define it properly, we have to figure out how this diagram
should look - and more concretely, define what is the correct relationship to use between a protein
and an enzyme class.

<img src="https://docs.google.com/drawings/d/e/2PACX-1vQkR3OSIqN3GoYJvtNtzvUWIRLYHTyciQ-PdC9OeE72gyk_kZ0cSDpZZ1dc2zgYLi4ZBexP3iZtn0mV/pub?w=1542&amp;h=1116">

Related discussions:

- https://github.com/oborel/obo-relations/issues/783