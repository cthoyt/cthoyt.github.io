---
layout: post
title: Pathway Relationships
date: 2020-12-30 00:00:00 -0800
author: Charles Tapley Hoyt
---
When Daniel started the [ComPath](https://doi.org/10.1038/s41540-018-0078-8) project, he wanted to look into the overlap
of the human pathways in KEGG, Reactome, and WikiPathways.

This blog post will follow apoptosis, one of the most ubiquitous pathways in biology that
covers all manners of programed cell death. This blog post isn't about the nitty-gritty difference between
pathways, biological processes, and mechanisms - so we will consider all variants of apoptosis
and apoptotic process effectively the same.

| Resource                                | Prefix       | Identifier | Name                   |
| --------------------------------------- | ------------ | ---------- | -----------------------|
| Gene Ontology                           | go           | GO:0006915 |
| Medical Subject Headings                | mesh         | D017209    |
| Kyoto Encyclopedia of Genes and Genomes | kegg.pathway | map04210   |
| NCI Thesaurus                           | ncit         | C17557     |

## Pathways are Equivalent

Two pathways are equivalent and can be represented with `skos:exactMatch` if they both
have the same species specificity. The following relationships are between the non-species
specific pathways:

| Subject      | Predicate       | Object                 |
| ------------ | --------------- | ---------------------- |
| GO:0006915   | skos:exactMatch | mesh:D017209           |
| GO:0006915   | skos:exactMatch | kegg.pathway:map04210  |
| mesh:D017209 | skos:exactMatch | kegg.pathway:map04210  |

The following relationships are between the human-specific pathways in KEGG, Reactome, and WikiPathways:

| Subject               | Predicate       | Object                |
| --------------------- | --------------- | --------------------- |
| kegg.pathway:hsa04210 | skos:exactMatch | reactome:R-HSA-109581 |
| kegg.pathway:hsa04210 | skos:exactMatch | wikipathways:WP254    |
| wikipathways:WP254    | skos:exactMatch | reactome:R-HSA-109581 |

Similarly, the relationships between cow-specific pathways in KEGG, Reactome, and WikiPathways

| Subject               | Predicate       | Object                |
| --------------------- | --------------- | --------------------- |
| kegg.pathway:bta04210 | skos:exactMatch | reactome:R-BTA-109581 |
| kegg.pathway:bta04210 | skos:exactMatch | wikipathways:WP1018   |
| wikipathways:WP1018   | skos:exactMatch | reactome:R-BTA-109581 |

While equivalences begins to tame the ontology of pathways, it is missing
links between the GO, MeSH, and NCIT terms to Reactome and WikiPathways.

## Species-Specific Variant of a Pathway

GO, MeSH, NCIT, and many other nomenclatures do not contain species-specific variants
of their pathways. However, KEGG contains both a parent pathway, prefixed with `map`
and species-specific pathway, prefixed with their internal 3 or 4-letter species code.

| Subject               | Predicate       | Object                |
| --------------------- | --------------- | --------------------- |
| kegg.pathway:hsa04210 | speciesSpecific | kegg.pathway:map04210 |
| kegg.pathway:bta04210 | speciesSpecific | kegg.pathway:map04210 |
| ...                   | ...             | ...                   |

It should generally hold that when `X speciesSpecific Y` and `Y skos:exactMatch Z`
are true, `X speciesSpecific Z`. This allows KEGG to serve as a bridge between
the species-specific and non-species-specific pathway worlds. However, as
Domingo-Fernandez *et al* showed, there are huge discrepancies between KEGG, Reactome,
and WikiPathways, so there is still need to curate/infer the same kinds relationships in
Reactome and WikiPathways.

However, Reactome and WikiPathways do not (yet) have parent terms for non-species-specific pathways.
Because Reactome uses a standardized nomenclature where all variants of each pathway across
species have the same numerical part to their identifier (e.g., R-HSA-109581 and R-BTA-109581),
they could institute a similar parent nomenclature like KEGG's. WikiPathways does not have
this sort of regularity, but they have the benefit of being highly receptive to external
input and improvements.

Side bar: I've seen an elegant solution for this in OBO that defines child terms
with an intersection of the [Relation Ontology](https://github.com/oborel/obo-relations)
relation RO:0002160 (only in taxon) to a given species and the parent term, but this
is an unnecessarily complicated alternative for the goal of representing the relation
between two entities.

## Pathway are Orthologs

| Subject               | Predicate | Object                |
| --------------------- | ----------| --------------------- |
| kegg.pathway:hsa04210 | orthology | kegg.pathway:bta04210 |


## Pathway is About a Concept

KEGG, Reactome, and WikiPathways not only include pathways, but also
other schematics about specific topics such as diseases, families of
proteins, and other biological entities.

KEGG has an entry kegg.pathway:hsa05010 entitled "Alzheimer disease - Homo sapiens (human)".
When doing lexical matchings, the MeSH entry mesh:D000544 "Alzheimer Disease" appeared
highly ranked. However, KEGG's notion of pathway and MeSH's notion of a disease are not
the same, and these two terms should not be considered equivalent. For the many cases
like this not only KEGG but also Reactome and WikiPathways, we can introduce a new
relationship ``pathwayAbout``. It turns out that WikiPathways also has an Alzheimer's
disease "pathway" as well.

| Subject               | Predicate    | Object       |
| --------------------- | ------------ | ------------ |
| kegg.pathway:hsa05010 | pathwayAbout | mesh:D000544 |
| wikipathways:WP2059   | pathwayAbout | mesh:D000544 |

Note that KEGG and WikiPathways both have specificity in their pathways for organisms,
but diseases in MeSH and other nomenclatures aren't typically stratified by their
target organisms. Therefore, the mouse-specific Alzheimer's disease pathway in
WikiPathways (wikipathways:WP2075) could also have the same relationship.

Another example is opsins - a family of light-sensitive proteins.



When we were using Gilda to do lexical matching of pathways in 

1. Diseases
2. Families of Proteins

