---
layout: post
title: Measuring the impact of the Bioregistry
date: 2025-08-18 13:20:00 +0200
author: Charles Tapley Hoyt
tags:
  - CURIE
  - URI
  - URN
  - IRI
  - identifiers
  - identifier schema
  - Bioregistry
  - biopragmatics
---

The [Bioregistry](https://bioregistry.io) is a database and toolchain
for standardization of prefixes, CURIEs, and URIs that appear in linked (open) data.
I originally wrote it in late 2019 as a submodule of
[PyOBO](https://github.com/biopragmatics/pyobo) to support parsing
database cross-references from OBO Foundry ontologies. Since then, it has
shifted towards a community model and been adopted in many downstream projects. This
post is an attempt to quantify its usage and impact.

Why do this?

1. Interest in making an application to GBCR
2. Interested in applying to deNBI/ELIXIR germany

## Statistics

Community statistics:

| Statistic            | Count | 
|----------------------|------:|
| Contributors         |    75 |
| Open Issues          |   146 |
| Closed Issues        |   471 |
| Total Issues         |   617 | 
| Open pull requests   |    13 |
| Closed pull requests | 1,012 |
| Total pull requests  | 1,025 |

Content statistics:

| Statistic                  | Count | 
|----------------------------|------:|
| Prefixes                   | 2,024 |
| Prefix Synonyms            |   547 |
| External positive mappings | 9,162 |
| External negative mappings |   157 | 
| Total external mappings    | 9,319 |
| Collections                |    18 |
| External Registries        |    33 |

## Website Usage

The following chart breaks down the nearly 4,400 unique users of the
Bioregistry's website by country. It shows that the Bioregistry is having a
global impact, with potential for further growth in Africa (which I hope to do
by getting in touch with the
[Africa PID Alliance](http://www.africapidalliance.org)).

![](/img/bioregistry-ui-august-2025.png)

## API and Resolver Usage

Many usages of the Bioregistry are in the form of the resolution of links like
[https://bioregistry.io/chembl:CHEMBL4303805](https://bioregistry.io/chembl:CHEMBL4303805).
Under the hood, the Bioregistry can expand prefixes like
[`chembl:CHEMBL4303805`](https://bioregistry.io/chembl:CHEMBL4303805) to URLs.
This makes it a perfect service to support other applications that reference
entities and want to provide external links, without having to maintain the
links themselves.

![](/img/bioregistry-api-august-2025.png)

I'm just getting this working, so it should also be able to better keep track of unique
users (note it's just showing 1 so far) and their countries. Luckily, all of this is GDPR-compliant from the beginning.

## Code Usages

The Bioregistry distributes a Python package that can be installed with
`pip install bioregistry`. The following
[search query](https://github.com/search?q=%22import%20bioregistry%22%20OR%20%22from%20bioregistry%20import%22%20-user%3Acthoyt%20-user%3Asorgerlab%20-user%3Abiopragmatics%20-is%3Afork%20-user%3Apyobo%20-user%3Apybel%20-user%3Agyorilab&type=code)
identifies places where the `bioregistry` Python package is imported.

<a href="https://docs.google.com/drawings/d/1TqjUc2lxgBaAKhOknYL2erxiqcswevVkhf3mu-7jNtE/edit?usp=sharing">
<img src="https://docs.google.com/drawings/d/e/2PACX-1vQmRTV8DxPfj0UL0i1dgkiFTgnhvI3mRQxt-sekL5tWCc8d4DLthv-48oBxXRisCdGUluovp4CXcEgN/pub?w=1440&amp;h=1080" />
</a>

A more detailed version of this is available
[here](https://biopragmatics.github.io/bioregistry/usages).

## Indirect Usages

The Bioregistry is a part of other software that supports modern biocuration.
