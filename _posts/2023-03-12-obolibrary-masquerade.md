---
layout: post
title: Resources masquerading as OBO Foundry ontologies
date: 2023-03-12 00:11:23 +0100
author: Charles Tapley Hoyt
tags: bioregistry obo ontologies
---

Several controlled vocabularies and ontologies that aren't themselves
[OBO Foundry](https://obofoundry.org/) ontologies use unsanctioned OBO PURLs.
This post is about how to use [the Bioregistry](https://bioregistry.io/) to
identify which resources are doing this and to give some insight into how we
arrived in this situation.

## Background on the OBO Foundry

The [OBO Foundry](https://obofoundry.org/) is a set of independent,
interoperable biomedical ontologies that aspire to using
[shared development principles](https://obofoundry.org/principles/fp-000-summary.html).
One such principle is to use a principled approach for creating persistent
uniform resource locators (PURLs) for local unique identifiers in each ontology.
These PURLs follow the form
`http://purl.obolibrary.org/obo/<PREFIX>_<LOCAL UNIQUE IDENTIFIER>`. For
example, a prefix might be `GO` (for the Gene Ontology) and local unique
identifier might be `0032571` (for _response to vitamin K_ in GO) resulting in
the PURL
[http://purl.obolibrary.org/obo/GO_0032571](http://purl.obolibrary.org/obo/GO_0032571).

While most semantic web resources allow the use of any IRIs (internationalized
resource identifiers), the OBO Foundry enforces that its PURLs resolve to
something useful for readers (e.g., to the
[Ontology Lookup Service](https://www.ebi.ac.uk/ols)). The resolver behind
[http://purl.obolibrary.org](http://purl.obolibrary.org) is implemented and
maintained in a
[GitHub repository](https://github.com/OBOFoundry/purl.obolibrary.org/) with
corresponding `.htaccess` files for each OBO Foundry ontology. Correct and
useful configuration for each ontology are a requirement for acceptance to the
OBO Foundry.

At the core of the OBO Foundry are several high quality, well-known, generally
useful ontologies such as the [Gene Ontology](https://bioregistry.io/go) and the
[Cell Ontology](https://bioregistry.io/go). Inclusion in the OBO Foundry has
therefore become a _de facto_ stamp of approval for ontologies that (until now)
254 ontologies have (for better or worse) successfully sought out.

## The Masquerade

Unfortunately, some ontologies and controlled vocabularies have adopted OBO
PURLs even though they are not OBO Foundry ontologies. This is a problem for a
few reasons:

1. The PURLs are not registered in
   [https://github.com/OBOFoundry/purl.obolibrary.org/](https://github.com/OBOFoundry/purl.obolibrary.org/)
   and therefore do not resolve
2. The quality of the ontology has not been vetted, meaning that low-quality
   ontologies using OBO PURLs could damage community trust in the OBO Foundry
3. These PURLs might conflict with other URIs prefix synonyms, increasing
   complexity for data integration
4. Most importantly: it's confusing.

One of the jobs of [the Bioregistry](https://bioregistry.io/) is to catalog the
URI format strings for identifier resources useful for the life and natural
sciences. This allows us to assess how big the problem of non-OBO Foundry
ontologies are using OBO PURLs, and why. Without further ado, here's the list of
offending resources that appear in the Bioregistry:

| prefix                                                    | name                                            | evidence      | uri_prefix                                  |
| --------------------------------------------------------- | ----------------------------------------------- | ------------- | ------------------------------------------- |
| [aeon](https://bioregistry.io/aeon)                       | Academic Event Ontology                         | curated       | `http://purl.obolibrary.org/obo/AEON_`      |
| [cemo](https://bioregistry.io/cemo)                       | COVID-19 epidemiology and monitoring ontology   | extra         | `http://purl.obolibrary.org/obo/cemo.owl#`  |
| [covoc](https://bioregistry.io/covoc)                     | CoVoc Coronavirus Vocabulary                    | curated       | `http://purl.obolibrary.org/obo/COVOC_`     |
| [decipher](https://bioregistry.io/decipher)               | DECIPHER CNV Syndromes                          | biocontext    | `http://purl.obolibrary.org/obo/DECIPHER_`  |
| [dermo](https://bioregistry.io/dermo)                     | Human Dermatological Disease Ontology           | curated       | `http://purl.obolibrary.org/obo/DERMO_`     |
| [efo](https://bioregistry.io/efo)                         | Experimental Factor Ontology                    | biocontext    | `http://purl.obolibrary.org/obo/EFO_`       |
| [gorel](https://bioregistry.io/gorel)                     | GO Relations                                    | biolink       | `http://purl.obolibrary.org/obo/GOREL_`     |
| [hpath](https://bioregistry.io/hpath)                     | Histopathology Ontology                         | curated       | `http://purl.obolibrary.org/obo/MC_`        |
| [idocovid19](https://bioregistry.io/idocovid19)           | COVID-19 Infectious Disease Ontology            | curated       | `http://purl.obolibrary.org/obo/COVIDO_`    |
| [lbo](https://bioregistry.io/lbo)                         | Livestock Breed Ontology                        | curated       | `http://purl.obolibrary.org/obo/LBO_`       |
| [lpt](https://bioregistry.io/lpt)                         | Livestock Product Trait Ontology                | curated       | `http://purl.obolibrary.org/obo/LPT_`       |
| [mesh](https://bioregistry.io/mesh)                       | Medical Subject Headings                        | biocontext    | `http://purl.obolibrary.org/obo/MESH_`      |
| [msio](https://bioregistry.io/msio)                       | Metabolomics Standards Initiative Ontology      | curated       | `http://purl.obolibrary.org/obo/MSIO_`      |
| [omia](https://bioregistry.io/omia)                       | Online Mendelian Inheritance in Animals         | biocontext    | `http://purl.obolibrary.org/obo/OMIA_`      |
| [omim](https://bioregistry.io/omim)                       | Online Mendelian Inheritance in Man             | biocontext    | `http://purl.obolibrary.org/obo/OMIM_`      |
| [pride](https://bioregistry.io/pride)                     | PRIDE Controlled Vocabulary                     | curated       | `http://purl.obolibrary.org/obo/PRIDE_`     |
| [reo](https://bioregistry.io/reo)                         | Reagent Ontology                                | curated       | `http://purl.obolibrary.org/obo/REO_`       |
| [roleo](https://bioregistry.io/roleo)                     | Role Ontology                                   | curated       | `http://purl.obolibrary.org/obo/RoleO_`     |
| [soybase](https://bioregistry.io/soybase)                 | SoyBase                                         | prefixcommons | `http://purl.obolibrary.org/obo/`           |
| [uniprot.isoform](https://bioregistry.io/uniprot.isoform) | UniProt Isoform                                 | extra         | `http://purl.obolibrary.org/obo/UniProtKB_` |
| [vido](https://bioregistry.io/vido)                       | Virus Infectious Disease Ontology               | curated       | `http://purl.obolibrary.org/obo/VIDO_`      |
| [vsmo](https://bioregistry.io/vsmo)                       | Ontology for vector surveillance and management | curated       | `http://purl.obolibrary.org/obo/VSMO_`      |
| [xl](https://bioregistry.io/xl)                           | Cross-linker reagents ontology                  | curated       | `http://purl.obolibrary.org/obo/XL_`        |

In the _evidence_ column, there are a few possible entries:

1. **curated** - this is the URI prefix manually curated in the Bioregistry.
   This happens when the primary ontology artifact uses OBO PURLs.
2. **extra** - this is when there's a manually curated extra URI prefix in the
   Bioregistry (in addition to the primary one) that uses an OBO PURL. This
   usually is done to enable the Bioregistry's IRI parser to handle cases that
   appear in third-party data that incorrectly constructs IRIs.
3. **biocontext**, **biolink**, and **prefixcommons** - this is when other
   registries have assigned OBO PURLs as their URI expansions

It's worth noting that there are probably _lots_ more resources doing this,
e.g., that are listed in [BioPortal](https://bioportal.bioontology.org/), but
have not been included in the Bioregistry because of their lack of notability,
utility, or reuse.

<details><summary>Here's the code that generated the table (before minor modifications)</summary>

```python
import bioregistry
from tabulate import tabulate

OBOLIBRARY_SUBSTRING = "purl.obolibrary.org/obo"
rows = []
for prefix, resource in bioregistry.read_registry().items():
    if resource.get_obofoundry_prefix() or prefix == "obo":
        continue
    name = resource.get_name()
    contact = resource.get_contact()
    l = f"[{prefix}](https://bioregistry.io/{prefix})"
    if resource.uri_format and OBOLIBRARY_SUBSTRING in resource.uri_format:
        rows.append((l, name, "curated", "", resource.uri_format))
        continue
    elif (uri_format := resource.get_uri_format()) and OBOLIBRARY_SUBSTRING in uri_format:
        rows.append((l, name, "default", "", uri_format))
        continue
    for metaprefix in resource.get_mappings():
        uri_format = (getattr(resource, metaprefix, None) or {}).get("uri_format")
        if uri_format and OBOLIBRARY_SUBSTRING in uri_format:
            rows.append((l, name, "mapped", metaprefix, uri_format))
    for p in resource.get_extra_providers():
        if OBOLIBRARY_SUBSTRING in p.uri_format:
            rows.append((l, name, "extra", p.code, p.uri_format))

print(tabulate(rows, headers=["prefix", "name", "type", "code", "uri_format"], tablefmt="github"))
```

</details>

## Rationalizations

Based on the table above, there are several situations in which an OBO PURL
appears:

1. Ontologies that are curated in the OBO flat file format then converted to the
   OWL format using [ROBOT](https://robot.obolibrary.org/) are automatically
   given OBO PURLs. For example, this occurs for the Livestock Breeding
   Ontology.
2. Similarly, ontologies that are uploaded to BioPortal likely undergo a similar
   procedure that results in BioPortal PURLs that themselves include OBO PURLs.
   For example, this occurs for FamPlex and the Vital Sign Ontology.
3. Ontologies are/were intended to be submitted to the OBO Foundry. For example,
   this includes:
   - The Academic Event Ontology (AEON) is still a work in progress and will be
     submitted to the OBO Foundry
   - The Reagent Ontology (REO) was abandoned and never submitted to the OBO
     Foundry
4. Ontologies that closely used by the OBO Foundry ecosystem, and are somtimes
   mistaken for being in it (e.g., EFO)
5. Not all ontologies, controlled vocabularies, or other semantic spaces have
   associated PURLs. Several registries (e.g., Prefix Commons, BioContext,
   BioLink Model) have "made up" OBO PURLs for non-OBO Foundry resources because
   of their use case-specific preferences.
6. In the case of XL, I think that this was an OBO Foundry ontology at some
   point but got renamed. It's very difficult to understand the history of the
   [HUPO Proteomics Standards Initiative](http://www.psidev.info/groups/controlled-vocabularies)
   from the outside
7. Some of these examples that appear with evidence "extra" are there because
   third-party resources incorrectly reference entities using unsanctioned OBO
   PURLs
8. In the case of CEMO, it appears the URI prefix is an artifact of incorrect
   configuration curation tooling (likely Protege).

It's hard to know for sure for the situation that lead to the
developers/maintainers of primary resources using unsanctioned OBO PURLs or the
developers/maintainers of third party resources using unsanctioned OBO PURLs.
Regardless, it's still valuable for the community to know about these problems
and potentially use comprehensive resources like the Bioregistry as a guide
towards improving interoperability and interpretability.
