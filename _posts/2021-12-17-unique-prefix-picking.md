---
layout: post
title: How to Pick a Unique Prefix
date: 2021-12-17 14:17:00 +0100
author: Charles Tapley Hoyt
tags: semantics
---

After the
[recent incident](https://github.com/OBOFoundry/OBOFoundry.github.io/pull/1703)
on the OBO Foundry where an inexperienced group submitted a new ontology request
using a prefix that already existed in the
[BioPortal](https://bioportal.bioontology.org), there has been a
[renewed interest](https://github.com/OBOFoundry/OBOFoundry.github.io/issues/1704)
in implementing an automated solution to protect against this.

## The Big Picture

A more general issue is that there can be prefix conflicts between different
registries. I found a few examples of this happening while building the
[Bioregistry](https://bioregistry.io) in the Spring 2021. Notably, this included
the conflict between the
[Geographical Entity Ontology](https://github.com/ufbmi/geographical-entity-ontology)
and the [Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/) which both
used the prefix `geo` in the [OBO Foundry](https://obofoundry.org/ontology/geo)
and [Identifiers.org](https://registry.identifiers.org/registry/geo),
respectively. These conflicts needed thoughtful mediation. After
[discussing on GitHub](https://github.com/ufbmi/geographical-entity-ontology/issues/19)
with [Bill Hogan](https://github.com/hoganwr), the responsible author of the
Geographical Entity Ontology, we decided that to use the prefix
[`geogeo`](https://bioregistry.io/registry/geogeo) in the Bioregistry. The Gene
Expression Omnibus maintained its usage of
[`geo`](https://bioregistry.io/registry/geo) due to its much wider usage and
longer history.

As a follow-up, I began curating a
[list of conflicts](https://github.com/biopragmatics/bioregistry/blob/main/src/bioregistry/data/mismatch.json)
and
[implemented a technical solution](https://github.com/biopragmatics/bioregistry/pull/62)
in the Bioregistry's nightly automated alignment workflow to prevent automated
alignment between known conflicting prefixes from different registries, but this
only a partial solution to a problem that is ultimately dependent on having
confidence in the external resources (which is indeed its own issue).

## What the Bioregistry Aligns

A small, select set of registries are fully automatically ingested in the
Bioregistry which includes (at the time of writing) Identifiers.org,
Name-to-Thing, the OBO Foundry, and the Ontology Lookup Service. The remaining
registries are excluded for a variety of reasons including redundancy with other
resources (e.g., AberOWL and OntoBee), a lack of modernization or alignment
(e.g., NCBI's registry), general inclusion of non-nomenclature resources (e.g.,
UniProt's registry, FAIRsharing), and a lack of minimum quality standards (e.g.,
BioPortal). A summary and slightly more detailed explanation about these sources
can be found [here](https://bioregistry.io/summary).

In many ways, the fact that the Bioregistry fully imports some resources and
automatically aligns with others

The Bioregistry imports Identifiers.org, OBO Foundry, and N2T as well as many
other resources (see for a full list), so it can be a one-stop shop for most
resources. However, it does not import all of BioPortal, so users should check
there too.

## How to Check Your Prefix is Unique

Ultimately the point of this post is to present a workflow for any potential who
want to check their new ontology request has a unique prefix (which will soon be
a technical requirement in the OBO Foundry). Because the Bioregistry imports
many resources, it's sufficient to just check the Bioregistry and BioPortal
(assuming you're interested in respecting the BioPortal content).

### Manual Check

The first way to check if your prefix is unique is to manually read through some
of the sites.

| Resource    | Home Page                         | Prefix List                                  |
| ----------- | --------------------------------- | -------------------------------------------- |
| Bioregistry | https://bioregistry.io            | https://bioregistry.io/registry              |
| Bioportal   | https://bioportal.bioontology.org | https://bioportal.bioontology.org/ontologies |

While the BioPortal API is locked behind API key access, the Bioregistry
additionally has a search endpoint at `https://bioregistry.io/api/search?q=...`

### Data Dumps

The second way to check if your prefix is unique is by comparing it to full
dumps of the Bioregistry and BioPortal. The Bioregistry can be downloaded in
several formats that are updated on a nightly basis:

- [TSV](https://github.com/biopragmatics/bioregistry/blob/main/exports/registry/registry.tsv)
- [JSON](https://github.com/biopragmatics/bioregistry/blob/main/exports/registry/registry.json)
- [YAML](https://github.com/biopragmatics/bioregistry/blob/main/exports/registry/registry.yml)
- [RDF](https://github.com/biopragmatics/bioregistry/tree/main/exports/rdf)

BioPortal doesn't offer any first-party data dumps, but the Bioregistry
generates one nightly
[here](https://github.com/biopragmatics/bioregistry/blob/main/src/bioregistry/data/external/bioportal/raw.json)

### Programmatic Access

The third way to check if your prefix is unique is by comparing it to the
Bioregistry and BioPortal using code from the `bioregistry` python package
(which is updated nightly).

Programmatic way to check if something is in the Bioregistry:

```python
import bioregistry

query = "EPSO"
available_in_bioregistry = bioregistry.normalize_prefix(query) is None
```

Programmatic way to check if something is in BioPortal:

```python
from bioregistry.external.bioportal import get_bioportal

query = "EPSO"
bioportal_dict = get_bioportal()
available_in_bioportal = query not in bioportal_dict
```

---

Being high quality and enabling external contribution and improvements are core
to the philosophy of the Bioregistry. While no solution is perfect for listing
all possible prefixes and it might be necessary to do a bit of extra googling
before picking a prefix, this is a great place to start. If during the process
of choosing a prefix you find you might create a conflict, please consider also
[suggesting a new entry](https://github.com/biopragmatics/bioregistry/issues/new/choose)
in the Bioregistry.
