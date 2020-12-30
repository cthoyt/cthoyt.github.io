---
layout: post
title: Pathway Relationships
date: 2020-12-30 00:00:00 -0800
author: Charles Tapley Hoyt
---
Domingo-Fernandez *et al.* published [ComPath: An ecosystem for exploring, analyzing,
and curating mappings across pathway databases.](https://doi.org/10.1038/s41540-018-0078-8)
in 2018 describing the overlap between human pathways in KEGG, Reactome, and WikiPathways.
A lot of the underlying machinery I developed to support this project has been improved since,
and it's time to spread the search to other organisms besides humans and other databases.
This blog post is about some additional relation types needed to capture the relations
between pathways appearing in these databases.

Like many blog posts, this one was inspired by a tweet. After the following discussion,
I thought it would be good to better organize the ideas and elaborate.

<blockquote class="twitter-tweet" data-partner="tweetdeck"><p lang="en" dir="ltr"><a href="https://twitter.com/hashtag/KEGG?src=hash&amp;ref_src=twsrc%5Etfw">#KEGG</a> provides a namespace of non-species-specific pathway terms that all of its species-specific pathways can map to. <a href="https://twitter.com/reactome?ref_src=twsrc%5Etfw">@reactome</a> could you provide the same?</p>&mdash; Charles Tapley Hoyt (@cthoyt) <a href="https://twitter.com/cthoyt/status/1344076052386238464?ref_src=twsrc%5Etfw">December 30, 2020</a></blockquote>

This blog post will follow apoptosis, one of the most ubiquitous pathways in biology that
covers all manners of programed cell death. This blog post isn't about the nitty-gritty difference between
pathways, biological processes, and mechanisms - so we will consider all variants of apoptosis
and apoptotic process effectively the same.

| Resource                                       | Prefix       | Identifier                                                |
| ---------------------------------------------- | ------------ | --------------------------------------------------------- |
| Gene Ontology (GO)                             | go           | [GO:0006915](https://identifiers.org/GO:0006915)          |
| Medical Subject Headings (MeSH)                | mesh         | [D017209](https://identifiers.org/mesh:D017209)           |
| Kyoto Encyclopedia of Genes and Genomes (KEGG) | kegg.pathway | [map04210](https://identifiers.org/kegg.pathway:map04210) |
| NCI Thesaurus (NCIT)                           | ncit         | [C17557](https://identifiers.org/ncit:C17557)             |

KEGG, Reactome, and WikiPathways all provide human-specific variants of these pathways
(below) as well as many other species, including both model organisms and not.

| Resource     | Prefix       | Identifier                                                    |
| ------------ | ------------ | ------------------------------------------------------------- |
| KEGG         | kegg.pathway | [hsa04210](https://identifiers.org/kegg.pathway:hsa04210)     |
| Reactome     | reactome     | [R-HSA-109581](https://identifiers.org/reactome:R-HSA-109581) |
| WikiPathways | wikipathways | [WP254](https://identifiers.org/wikipathways:WP254)           |

## Pathways are Equivalent

Two pathways are equivalent and can be represented with `skos:exactMatch` if they both
have the same species specificity. The following relationships are between the non-species
specific pathways for apoptosis:

| Subject                                              | Predicate       | Object                                                                 |
| ---------------------------------------------------- | --------------- | ---------------------------------------------------------------------- |
| [GO:0006915](https://identifiers.org/GO:0006915)     | skos:exactMatch | [mesh:D017209](https://identifiers.org/mesh:D017209)                   |
| [GO:0006915](https://identifiers.org/GO:0006915)     | skos:exactMatch | [kegg.pathway:map04210](https://identifiers.org/kegg.pathway:map04210) |
| [mesh:D017209](https://identifiers.org/mesh:D017209) | skos:exactMatch | [kegg.pathway:map04210](https://identifiers.org/kegg.pathway:map04210) |
| ...                                                  | ...             | ...                                                                    |

The following relationships are between the human-specific pathways for apoptosis in
KEGG, Reactome, and WikiPathways:

| Subject                                                                | Predicate       | Object                                                                 |
| ---------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------- |
| [kegg.pathway:hsa04210](https://identifiers.org/kegg.pathway:hsa04210) | skos:exactMatch | [reactome:R-HSA-109581](https://identifiers.org/reactome:R-HSA-109581) |
| [kegg.pathway:hsa04210](https://identifiers.org/kegg.pathway:hsa04210) | skos:exactMatch | [wikipathways:WP254](https://identifiers.org/wikipathways:WP254)       |
| [wikipathways:WP254](https://identifiers.org/wikipathways:WP254)       | skos:exactMatch | [reactome:R-HSA-109581](https://identifiers.org/reactome:R-HSA-109581) |

Similarly, the relationships between cow-specific (Bos Taurus; BTA)
pathways for apoptosis in KEGG, Reactome, and WikiPathways:

| Subject                                           | Predicate       | Object                                            |
| ------------------------------------------------- | --------------- | ------------------------------------------------- |
| [kegg.pathway:bta04210](https://identifiers.org/) | skos:exactMatch | [reactome:R-BTA-109581](https://identifiers.org/) |
| [kegg.pathway:bta04210](https://identifiers.org/) | skos:exactMatch | [wikipathways:WP1018](https://identifiers.org/)   |
| [wikipathways:WP1018](https://identifiers.org/)   | skos:exactMatch | [reactome:R-BTA-109581](https://identifiers.org/) |

While equivalences begins to tame the ontology of pathways, it is missing
links between the GO, MeSH, and NCIT terms to Reactome and WikiPathways.

## Species-Specific Variant of a Pathway

GO, MeSH, NCIT, and many other nomenclatures do not contain species-specific variants
of their pathways. However, KEGG contains both a parent pathway, prefixed with `map`
and species-specific pathway, prefixed with their internal 3 or 4-letter species code.

| Subject                                                                | Predicate       | Object                                                                 |
| ---------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------- |
| [kegg.pathway:hsa04210](https://identifiers.org/kegg.pathway:hsa04210) | speciesSpecific | [kegg.pathway:map04210](https://identifiers.org/kegg.pathway:map04210) |
| [kegg.pathway:bta04210](https://identifiers.org/kegg.pathway:bta04210) | speciesSpecific | [kegg.pathway:map04210](https://identifiers.org/kegg.pathway:map04210) |
| ...                                                                    | ...             | ...                                                                    |

It should generally hold that when `X speciesSpecific Y` and `Y skos:exactMatch Z`
are true, `X speciesSpecific Z`. This allows KEGG to serve as a bridge between
the species-specific and non-species-specific pathway worlds. However,
Domingo-Fernandez *et al.* showed that there are huge discrepancies between KEGG, Reactome,
and WikiPathways, so there is still need to curate/infer the same kinds relationships in
Reactome and WikiPathways.

Unfortunately, Reactome and WikiPathways do not (yet) have parent terms for
non-species-specific pathways. Asking about this was the point of the tweet that
inspired this blog post. Because Reactome uses a standardized nomenclature
where all variants of each pathway across  species have the same numerical part to
their identifier (e.g., [R-HSA-109581](https://identifiers.org/reactome:R-HSA-109581)
and [R-BTA-109581](https://identifiers.org/reactome:R-BTA-109581)), they could institute a
similar parent nomenclature like KEGG's. WikiPathways identifiers do not have
this sort of regularity, but they have the benefit of being highly receptive to external
input and improvements.

Side bar: I've seen an elegant solution for this in OBO that defines child terms
with an intersection of the [Relation Ontology](https://github.com/oborel/obo-relations)
relation [RO:0002160](https://identifiers.org/RO:0002160) (only in taxon) to a given species
and the parent term, but this is an unnecessarily complicated alternative for the goal of
representing the relation between two entities.
