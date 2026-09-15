---
layout: post
title: Semantic Farm and the 3rd Base4NFDI User Conference
date: 2026-09-15 12:40:00 +0200
author: Charles Tapley Hoyt
tags:
  - Bioregistry
  - Semantic Farm
  - CURIEs
  - URIs
  - NFDI
  - NFDI4Chem
  - Base4NFDI
---

I submitted an abstract to the
[3rd Base4NFDI User Conference (UC4B2026)](https://base4nfdi.de/news-events/events/user-conference-2026)
on behalf of the
[NFDI Section Metadata Working Group for Ontology Harmonization and Mapping](https://github.com/nfdi-de/section-metadata-wg-onto/)
describing the current uses and future prospects for the
[Semantic Farm](https://semantic.farm) throughout the NFDI and Base4NFDI. This
post contains an extended version of the original submission.

I'd like to extend a special thanks to co-authors Mark Doerr (University
Greifswald), Ulrik Stervbo (Ruhr-Universität Bochum), Benjamin Zapilko (GESIS),
and Sonja Herres-Pawlis (RWTH Aachen). Their interest and support for the
Semantic Farm has been key in its integration in the NFDI Section Metadata
Working Group for Ontology Harmonzition and Mapping (WG Onto) and first steps
into other NFDI sections, working groups, and services.

We posted the original abstract to Zenodo such that it can be cited by
<https://doi.org/10.5281/zenodo.21686485>. The following abstract
below has minor embellishments (and many added links for context) and
an extra section.

## Abstract

**Title**: Operationalizing identifier interoperability across the NFDI with the
Semantic Farm

A key challenge in achieving the interoperability facet of the
[FAIR data principles](https://doi.org/10.1038/sdata.2016.18) is the consistent
identification of researchers, chemicals, paintings, and other entities relevant
for NFDI. Often, this means choosing the correct standard
[uniform resource identifier (URI)](https://www.rfc-editor.org/info/rfc3986/)
or [compact URI (CURIE)](https://www.w3.org/TR/2010/NOTE-curie-20101216/) for an
entity from an ontology, controlled vocabulary, persistent identifier (PID)
service, or database.

This presents a challenge when multiple CURIEs or URIs can be constructed for
the same entity, which is compounded by the independent evolution of tools and
services relevant for different NFDI consortia. For example, the entry for
[water](https://www.ebi.ac.uk/chebi/CHEBI:15377) in the
[Chemical Entities of Biomedical Interest (ChEBI)](https://www.ebi.ac.uk/chebi)
can be identified by either the URIs `https://www.ebi.ac.uk/chebi/CHEBI:15377`
or `http://purl.obolibrary.org/obo/CHEBI_15377` or by the CURIEs `chebi:15377`,
`CHEBI:15377`, or `CHEBIID:15377`. An organization-wide policy is required to
determine and communicate which is correct.

The NFDI has not yet adopted an actionable, organization-wide policy for
standardizing CURIEs and URIs. We present the
[Semantic Farm](https://semantic.farm) (previously called *The Bioregistry*) on
behalf of the
[NFDI Section Metadata Working Group for Ontology Harmonization and Mappings](https://github.com/nfdi-de/section-metadata-wg-onto/tree/main)
as a pre-existing, mature solution for the standardization of CURIEs and URIs.
It acts as a centralized index of metadata for resources that mint identifiers
that can be readily adopted on the NFDI-level and beyond.

Importantly, the Semantic Farm is a foundational service that can directly
support complementary base services
([PID4NFDI](https://base4nfdi.de/projects/pid4nfdi),
[TS4NFDI](https://base4nfdi.de/projects/ts4nfdi), and
[KGI4NFDI](https://base4nfdi.de/projects/kgi4nfdi)), NFDI sections, their
respective working groups, and researchers in NFDI consortia towards improving
interoperability. We highlight several existing applications of the Semantic
Farm within NFDI:

1. TS4NFDI uses both the flagship instance of the
   [Ontology Lookup Service](https://www.ebi.ac.uk/ols4/) (hosted by the
   European Bioinformatics Institute) and the
   [TIB Terminology Service](https://terminology.tib.eu/ts/) instance, which
   both use the Semantic Farm for URI compression, CURIE expansion, and
   generation of web links for database cross-references.
2. Section Metadata Working Group for Ontology Harmonization and Mapping uses
   the Semantic Farm capture ontology lists used by each consortium at
   <https://semantic.farm/nfdi>.
3. The Semantic Farm supports the construction of knowledge graphs with
   standardized URIs such as in Section EduTrain's
   [DALIA](https://search.dalia.education) platform for open educational
   resources and
   [Section International Engagement Working Group for Landscaping and Outreach's](https://github.com/nfdi-de/section-int-wg-landscape/)
   bibliometric knowledge graph. Standardization facilitates the integration of
   external data from ORCiD, ROR, CORDIS, and Wikidata.
4. The Semantic Farm's codebase is used by the [LinkML](https://linkml.io)
   runtime, which has growing adoption across consortia such as NFDI4Chem (e.g.,
   [MS DCAT AP](https://github.com/NFDI4Chem/ms_dcat_ap)), NFDI4Cat (e.g.,
   [CoreMeta4Cat](https://github.com/nfdi4cat/CoreMeta4Cat)), and GHGA (e.g.,
   [ghga-metadata-schema](https://github.com/ghga-de/ghga-metadata-schema)). It
   can be further used to standardize the prefix maps in LinkML schemas
5. The Semantic Farm supports consortia like NFDI4Chem that must standardize and
   ultimately harmonize a variety of ontology, database, and structural
   identifiers like InChI.

Further information on the Semantic Farm's KPIs can be found [here]({% post_url
2025/2025-08-22-bioregistry-impact %}). We aspire to submit Semantic Farm to
[Base4NFDI Service Support Track](https://base4nfdi.de/?view=article&id=211:service-support-track-application&catid=2)
and to support its integration in more NFDI services and usage in data
resources.

## Additional Context

This section was not part of the original abstract.

**Semantic Farm as a data standard** The Semantic Farm induces a standard prefix
map that is simultaneously a reflection of real-world usage as well as
community-curated standards for CURIE prefixes to URI prefixes. The flagship
Semantic Farm software package is implemented in Python, but the prefix map can
be operationalized as a data standard through the lower-level
[curies.rs](http://github.com/biopragmatics/curies.rs)
software package, which has bindings to Python, Java, R, Rust, and JavaScript
(via WASM) .makes this an actionable standard. For example:

1. LinkML schemas can be checked to use correct CURIE prefixes and URI prefixes,
   see this [previous post]({% post_url
   2026/2026-01-06-bioregistry-linkml-validation %}).
2. Prefix maps in triple stores, such as the NFDI4Culture
   [Culture Knowledge Graph](https://nfdi4culture.de/services/details/culture-knowledge-graph.html),
   can be contextualized and checked for standard CURIE prefix usage, see this
   [previous post]({% post_url 2025/2025-09-11-nfdi4culture-prefix-validation
   %}).
3. Turtle (and other RDF) artifacts, such as those produced for SKOS
   vocabularies and knowledge graphs, can be validated similarly, see this
   [previous post]({% post_url 2025/2025-09-04-bioregistry-turtle-validation
   %}).

**Semantic Farm enables data integration** The Semantic Farm was a key tool
that enabled the integration of the NFDI4Chem and
NFDI4Culture's KGs that wasn't possible using other NFDI tools like
TS4NFDI and KGI4NFDI. This scenario was described in detail [here]({% post_url
2025/2025-10-07-bridging-culture-and-chemistry %}).

**Semantic Farm has demonstrated widespread impact** While measuring the impact
of a data resource or software package is challenging, we collated a combination
of direct and indirect usages of the Semantic Farm across programming languages,
use cases, and countries in [this post]({% post_url
2025/2025-08-22-bioregistry-impact %}).
