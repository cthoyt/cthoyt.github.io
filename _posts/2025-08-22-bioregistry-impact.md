---
layout: post
title: Measuring the impact of the Bioregistry
date: 2025-08-22 16:54:00 +0200
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
Bioregistry's data, software, or web application. For example:

1. The [SSSOM-py](https://github.com/mapping-commons/sssom-py) Python package
   for interacting with semantic mappings uses the Bioregistry for supplying a
   comprehensive default prefix map during parsing of SSSOM files.
2. The [BridgeDB](https://www.bridgedb.org/) identifier mapping service uses the
   Bioregistry Python package to test its source metadata are properly
   standardized
   ([see here](https://github.com/bridgedb/datasources/blob/a238b40b915c7f7a69052afecfdc59ad26211b41/scripts/align_bioregistry.py#L6))
3. The [Protegé](https://github.com/protegeproject/protege/) ontology editor
   uses the Bioregistry's API to look up information about prefixes.
4. [WikiPathways](https://www.wikipathways.org) uses the Bioregistry's
   resolution service to linkify compact URIs ( CURIEs).

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

I think that because DO is built using tools that rely on the Bioregistry, it's
fair to claim that DO's (recent) impact is partially due to the Bioregistry.

The Bioregistry is in the excellent position where there are a variety of direct
and indirect usages, many of which are highly impactful, meaning that the
Bioregistry can share (a bit) in their glory. Later in this post, I'll give a
more quantitative justification for that statement.

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
impact of the proposed resource as part of their respective key performance
indicators (KPIs).

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

Note that this table is from mid-August 2025. Most of these numbers increase
over time. To give some further context to these statistics, here's a chart that
shows how the Bioregistry stacks up against other related resources. Keep in
mind, the Bioregistry is also a meta-resource that incorporates their important
parts, too. You can understand this chart by looking at the percentage in
parentheses (like +146% over Identifiers.org) and think: wow, those numbers are
much bigger than 0%, which means the Bioregistry is much more comprehensive!

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
`pip install bioregistry`. I used
[this query](https://github.com/search?q=%22import%20bioregistry%22%20OR%20%22from%20bioregistry%20import%22%20-user%3Acthoyt%20-user%3Asorgerlab%20-user%3Abiopragmatics%20-is%3Afork%20-user%3Apyobo%20-user%3Apybel%20-user%3Agyorilab&type=code)
to search GitHub for places where the `bioregistry` Python package is imported
and took detailed notes about their context (see details
[here](https://biopragmatics.github.io/bioregistry/usages)).

I found a large variety of usages across software packages, databases,
ontologies, knowledge graphs, frameworks, and data models. Because the
[LinkML](https://linkml.io/) modeling language's runtime indirectly depends on
the Bioregistry, there are also dozens to hundreds of projects that indirectly
use it. I also noted some usages from large organizations in the bioinformatics
space, such as SciBite, Synapse, and the NFDI.

<a href="https://docs.google.com/drawings/d/1TqjUc2lxgBaAKhOknYL2erxiqcswevVkhf3mu-7jNtE/edit?usp=sharing">
<img src="https://docs.google.com/drawings/d/e/2PACX-1vQmRTV8DxPfj0UL0i1dgkiFTgnhvI3mRQxt-sekL5tWCc8d4DLthv-48oBxXRisCdGUluovp4CXcEgN/pub?w=1440&amp;h=1080" />
</a>

## Indirect Usage

I used Wikidata as a backend to assess the indirect usage of the Bioregistry. I
did this in a few steps:

1. Make sure all direct usages have a Wikidata item that has a relationship to
   the [Bioregistry Wikidata item](https://www.wikidata.org/wiki/Q109302681) via
   the uses
   [P1547 (depends on software)](https://www.wikidata.org/wiki/Property:P1547)
   or [P2283 (uses)](https://www.wikidata.org/wiki/Property:P2283) predicates.
2. Identify well-known usages of direct usages, make sure they have Wikidata
   items, and are connected to them
3. Automate querying Wikidata for all direct and indirect usages
4. Search PubMed and quantify mentions of all direct and indirect usages

### Indirect Software Dependencies

I've been developing
[quickstatements-client](https://github.com/cthoyt/quickstatements_client) for
automating adding content to Wikidata. I added an extension to it that pulls
metadata from the Python Package Index (PyPI) and adds Python software packages.
It does this recursively for a given package and its dependencies while adding
appropriate
[P1547 (depends on software)](https://www.wikidata.org/wiki/Property:P1547)
relations between them.

Unfortunately, this workflow is still limited because it doesn't find depedent
software. This could be solved by doing a bulk download of PyPI and a
large-scale network analysis. It might also be possible to extract this
information from GitHub. However, for now, this is a good first step.

### Indirect Ontology Dependencies via ODK

The Ontology Development Kit (ODK) uses the Bioregistry in several ways. It is
used by many ontologies both in and out of the OBO Foundry. I
[developed a workflow](https://github.com/biopragmatics/bioregistry/pull/1650)
for identifying ODK usage by searching GitHub and iteratively filtering out
false positives. This resulted in over 140 repositories, more than half of which
could directly be mapped back to the Bioregistry, given it tracks the repository
associated with each prefix.

I have previously used
[quickstatements-client](https://github.com/cthoyt/quickstatements_client) for
automatically adding records for OBO Foundry ontologies. In next steps, I will
extend this for the other ontologies identified by this analysis and also map
them back to the ODK using the
[P1547 (depends on software)](https://www.wikidata.org/wiki/Property:P1547)
relation.

As a side note, for repositories using the ODK that couldn't be mapped, I
automated making stub curations in the Bioregistry, which lead to the curation
of dozens of new prefixes.

### Querying Wikidata

There's a long tail of different ways to curate indirect usages of the
Bioregistry. However, I believe that the largest cumulative impact for now will
be though the lens of the ontologies built using it. After working through the
scenarios above, I wrote a SPARQL query that recovers all direct and indirect
dependencies (see live table below).

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#SELECT%20DISTINCT%0A%3Fitem%20%3FshortName%20%3FitemLabel%20%3FitemDescription%20(GROUP_CONCAT(DISTINCT%20%3Ftype%3B%20separator%3D%22%7C%22)%20as%20%3Ftypes)%0AWHERE%20%7B%0A%20%20VALUES%20%3Fsoftware%20%7B%20wd%3AQ109302681%20wd%3AQ116738064%20%7D%0A%20%20%3Fitem%20(wdt%3AP1547%7Cwdt%3AP2283)%2B%20%3Fsoftware%20.%0A%20%20OPTIONAL%20%7B%20%3Fitem%20wdt%3AP1813%20%3FshortName%20.%20%7D%0A%20%20%3Fitem%20wdt%3AP31%2Frdfs%3Alabel%20%3Ftype%20.%0A%20%20FILTER(lang(%3Ftype)%20%3D%20'en')%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22.%20%7D%0A%7D%0AGROUP%20BY%20%3Fitem%20%3FshortName%20%3FitemLabel%20%3FitemDescription%0A" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>

### Literature Analysis

The final step was to analyze the literature for mentions of each of these
direct and indirect dependencies. In typical Charlie fashion, I wanted to
develop high-quality, modular, reusable software for doing this analysis, which
lead to [pubmed-downloader](https://github.com/cthoyt/pubmed-downloader) for
wrapping API-based and bulk queries to PubMed (in addition to bulk downloading
and processing, but that's a story for a different blog post).

![](https://raw.githubusercontent.com/cthoyt/bioregistry-impact/refs/heads/main/data/output.png)

This is pretty great, it shows there are potentially thousands of papers that
mention software, ontologies, databases, etc. that either directly or indirectly
use the Bioregistry. It also shows, unsurprisingly, that there's a power-law
distribution in which is mentioned most in the literature.

The code for the literature analysis is available in its
[own repository](https://github.com/cthoyt/bioregistry-impact). Of course, there
is still lots of room for improvement and optimization, such as:

1. Making the image above nicer!
2. Using synonyms for search
3. Removing false positives
4. Incorporating citation networks

I'm interested to also make this work flow semi-automated to help assess the
impact of other software/data resources, especially other key software that's
supporting the OBO Foundry like
[SSSOM-py](https://github.com/mapping-commons/sssom-py).

---

Parting thoughts: it does seem like the Bioregistry is having a meaningful
impact as a relatively young project. However, it's still an uphill climb to get
more direct recognition and adoption, which requires investing a lot of time in
community building. This isn't easy for me as an early career researcher not
only because of lack of time/funding but also because of my relative lack of
authority in the community of scientists who would benefit most from the
Bioregistry (which comes with time).

I consider Chris Mungall and his group as the gold standard of being able to
make large impact fast - they are known and trusted in the community, they have
dedicated support staff that can focus on community management, they have many
developers, and many projects where they can push their technologies. I'll get
there eventually!
