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
| Medical Subject Headings (MeSH)                | mesh         | [D017209](https://identifiers.org/mesh:)                  |
| Kyoto Encyclopedia of Genes and Genomes (KEGG) | kegg.pathway | [map04210](https://identifiers.org/kegg.pathway:map04210) |
| NCI Thesaurus (NCIT)                           | ncit         | [C17557](https://identifiers.org/ncit:C17557)             |
