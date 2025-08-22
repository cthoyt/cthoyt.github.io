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

The [Bioregistry](https://bioregistry.io) is a database and toolchain for
standardization of prefixes, CURIEs, and URIs that appear in linked (open) data.
While I created it in 2019 as a component of
[PyOBO](https://github.com/biopragmatics/pyobo) in order to support parsing
database cross-references appearing in biomedical ontologies, it has since
become an independent project with a community-driven governance model and much
broader applications. This post is a first attempt to quantify its usage and
impact.

## What are Usage and Impact?

For a foundational resource like the Bioregistry, there are two kinds of usage.
First, direct usage encompasses when a workflow directly reuses the
Bioregistry's data, software, or web application. For example,

1. the [SSSOM-py](https://github.com/mapping-commons/sssom-py) Python package
   for interacting with semantic mappings uses the Bioregistry for supplying a
   comprehensive default prefix map during parsing of SSSOM files.
2. the [BridgeDB](https://www.bridgedb.org/) identifier mapping service uses the
   Bioregistry Python package to test its source metadata are properly
   standardized
   ([see here](https://github.com/bridgedb/datasources/blob/a238b40b915c7f7a69052afecfdc59ad26211b41/scripts/align_bioregistry.py#L6))
3. the [Protegé](https://github.com/protegeproject/protege/) ontology editor
   uses the Bioregistry's API to look up information about prefixes

Second, indirect usage encompasses any other data, software, web application,
etc. that builds on direct usages. For example, any ontology that is edited
using Protegé indirectly uses the Bioregistry, like the
[Disease Ontology (DO)](https://github.com/DiseaseOntology/HumanDiseaseOntology).

I consider usage to be a very good proxy for impact, especially when considering
indirect usage. Allen Baron _et al._ recently published
[The DO-KB Knowledgebase: a 20-year journey developing the disease open science ecosystem](https://doi.org/10.1093/nar/gkad1051),
which made a quantification of DO's cumulative impact over the last decades. One
area of this study focused on literature citations and resulted in the
development of a
[reusable, open-source software package](https://github.com/DiseaseOntology/DO.utils)
for such analyses. I don't think anyone would disagree that the DO has had high
impact.

I think it's fair to say that because DO is built using tools that rely on the
Bioregistry, that it's fair to claim that DO's (recent) impact is partly due to
the Bioregistry. I think the Bioregistry is in the excellent position where
there are a variety of direct and indirect usages, many of which are highly
impactful, meaning that the Bioregistry can share (a bit) in their glory. Later
in this post, I'll give a more quantitative justification for that statement.

## Why Quantify Usage and Impact?

I think some of the main reasons for quantifying a project's usage and impact
are to:

1. justify its continued maintenance and improvement
2. get credit for making something important
3. use previous usage as examples for increased adoption
4. get funding to continue maintaining and improving it

At the moment, I am preparing to apply for the Bioregistry to be recognized by
the Global Biodata Coalition as a
[Global Core Biodata Resource (GCBR)](https://globalbiodata.org/what-we-do/global-core-biodata-resources/).
I am also preparing an application on behalf of current affiliation, RWTH Aachen
University, to join the
[German Network for Bioinformatics Infrastructure (deNBI)](https://www.denbi.de),
which will include offering the Bioregistry as key bioinformatics
infrastructure. Both applications require quantitative evidence of the usage and
impact of the proposed resource. As a side note, these statistics are often
called key performance indicators (KPI), because simple ideas need good three
letter acronyms to be taken seriously.

## The Bioregistry by the Numbers

There are two kinds of statistics I think are important to convey about the
Bioregistry. The first is related to community involvement. I've carefully
planned the governance structure of the project to be sustainable (based on
[the open data, open code, and open infrastructure (O3) guidelines](https://doi.org/10.1038/s41597-024-03406-w)).
This was successful in no small part due the way that there is a very low
barrier for entry for small, external contributions (i.e., a
[drive-by curation](https://doi.org/10.32388/KBX9VO)). Therefore, it makes sense
to highlight the number of unique contributors there have been to the data/code
of the project as well as the volume of contributions in the forms of issues,
discussions, and pull requests:

| Statistic            | Count |
| -------------------- | ----: |
| Contributors         |    75 |
| Open Issues          |   146 |
| Closed Issues        |   471 |
| Total Issues         |   617 |
| Open pull requests   |    13 |
| Closed pull requests | 1,012 |
| Total pull requests  | 1,025 |

The second kind of statistic that's important describes the content of the
resource itself.

| Statistic                  | Count |
| -------------------------- | ----: |
| Prefixes                   | 2,024 |
| Prefix Synonyms            |   547 |
| External positive mappings | 9,162 |
| External negative mappings |   157 |
| Total external mappings    | 9,319 |
| Collections                |    18 |
| External Registries        |    33 |

To give some context to these statistic, here's a chart that shows how the
Bioregistry stacks up against other related resources. Keep in mind, the
Bioregistry is also a meta-resource that incorporates their important parts,
too. You can understand this chart by looking at the percentage in parentheses
(like +146% over Identifiers.org) and thinking, wow, those numbers are much
bigger than 0%, which means the Bioregistry is much more comprehensive!

![](https://raw.githubusercontent.com/biopragmatics/bioregistry/main/docs/img/bioregistry_coverage_bar.svg)

## Direct Usage

### Who uses the Bioregistry Website?

The Bioregistry website exposes metadata about ontologies, databases, and other
resources that mint identifiers. This enables biocurators, data stewards,
librarians, and others interested in identifying appropriate ontologies for
reuse in their resources, data management plans, etc. It also allows researchers
who consume linked (open) data to find context about the kinds of prefixes,
CURIEs, or URIs that appear.

The following chart breaks down the nearly 4,400 unique users of the
Bioregistry's website by country. It shows that the Bioregistry is having a
global impact, with potential for further growth in Africa (which I hope to do
by getting in touch with the
[Africa PID Alliance](http://www.africapidalliance.org)).

![](/img/bioregistry-ui-august-2025.png)

### API and Resolver Usage

Many usages of the Bioregistry are in the form of the resolution of links like
[https://bioregistry.io/chembl:CHEMBL4303805](https://bioregistry.io/chembl:CHEMBL4303805).
Under the hood, the Bioregistry can expand prefixes like
[`chembl:CHEMBL4303805`](https://bioregistry.io/chembl:CHEMBL4303805) to URLs.
This makes it a perfect service to support other applications that reference
entities and want to provide external links, without having to maintain the
links themselves.

![](/img/bioregistry-api-august-2025.png)

I'm just getting this working, so it should also be able to better keep track of
unique users (note it's just showing 1 so far) and their countries. Luckily, all
of this is GDPR-compliant from the beginning.

### Code Usage

The Bioregistry distributes a Python package that can be installed with
`pip install bioregistry`. The following
[search query](https://github.com/search?q=%22import%20bioregistry%22%20OR%20%22from%20bioregistry%20import%22%20-user%3Acthoyt%20-user%3Asorgerlab%20-user%3Abiopragmatics%20-is%3Afork%20-user%3Apyobo%20-user%3Apybel%20-user%3Agyorilab&type=code)
identifies places where the `bioregistry` Python package is imported.

<a href="https://docs.google.com/drawings/d/1TqjUc2lxgBaAKhOknYL2erxiqcswevVkhf3mu-7jNtE/edit?usp=sharing">
<img src="https://docs.google.com/drawings/d/e/2PACX-1vQmRTV8DxPfj0UL0i1dgkiFTgnhvI3mRQxt-sekL5tWCc8d4DLthv-48oBxXRisCdGUluovp4CXcEgN/pub?w=1440&amp;h=1080" />
</a>

A more detailed version of this is available
[here](https://biopragmatics.github.io/bioregistry/usages).

## Indirect Usage

## Identifying Ontologies using the ODK

https://github.com/biopragmatics/bioregistry/pull/1650

This PR adds a script that surveys ODK usage on GitHub and proposes new
Bioregistry prefixes for ontologies that aren't already listed.

The script takes the following steps:

    Search GitHub for ODK configurations in order to identify repositories containing ontologies
    Filter out known false positives and low quality repositories (manually curated in the Python file)
    Map repositories back to the Bioregistry, when possible
    Otherwise, make stub entries in the Bioregistry for new prefixes

After filtering, this left more than 140 ontologies. This lead to the curation
of dozens of new prefixes. I left several for later, because some of them were
in the weird space before they would have any usages, so they were not necessary
for this analysis. But they could be useful prefixes in the future!

## Rest

The Bioregistry is a part of other software that supports modern biocuration.

One way of doing this is to use Wikidata, which models software dependenceies.
to some extent, I curated these myself. I also created

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#SELECT%20DISTINCT%0A%3Fitem%20%3FshortName%20%3FitemLabel%20%3FitemDescription%20(GROUP_CONCAT(DISTINCT%20%3Ftype%3B%20separator%3D%22%7C%22)%20as%20%3Ftypes)%0AWHERE%20%7B%0A%20%20VALUES%20%3Fsoftware%20%7B%20wd%3AQ109302681%20wd%3AQ116738064%20%7D%0A%20%20%3Fitem%20(wdt%3AP1547%7Cwdt%3AP2283)%2B%20%3Fsoftware%20.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1813%20%3FshortName%20.%20%7D%0A%20%20%3Fitem%20wdt%3AP31%2Frdfs%3Alabel%20%3Ftype%20.%0A%20%20FILTER(lang(%3Ftype)%20%3D%20'en')%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22.%20%7D%0A%7D%0AGROUP%20BY%20%3Fitem%20%3FshortName%20%3FitemLabel%20%3FitemDescription%0A" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>

the next step is then to do a literature analysis of each of these. In typical
charlie fashion, creating this blog post took weeks because I decided that each
piece of code I wrote was worthy of its own well-defined package

## Journey before Destination

- [pubmed-downloader](https://github.com/cthoyt/pubmed-downloader) for querying
  PubMed in bulk
- [wikidata-client](https://github.com/cthoyt/wikidata-client) for common
  SPARQL-based query functionality on Wikidata
- [quickstatements-client](https://github.com/cthoyt/quickstatements_client) for
  automatically creating entities for Python packages and OBO Foundry ontologies
- curated several new prefixes in the Bioregistry for ontologies that use the
  ODK
