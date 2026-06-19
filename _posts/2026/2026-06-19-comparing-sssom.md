---
layout: post
title: Comparing manually curated SSSOM
date: 2026-06-19 14:47:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - biocuration
  - curator agreement
---

I am currently supporting Philip Strömert and Noura Rayya in the efforts to
modernize and revitalize the
[Chemical Methods Ontology (CHMO)](https://semantic.farm/chmo) to support
annotation of instrumentation used to produce experimental data captured in the
[Chemotion](https://chemotion.net/) electronic laboratory notebook as part of
[NFDIChem](https://nfdi4chem.de).

They have already completed the important initial steps of assuming
maintainership from the Royal Society of Chemistry, porting the ontology to use
a standardized
[Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit/)
layout, and
[revising the definitions](https://github.com/rsc-ontology/rsc-cmo/pull/70) of
many classes based on the [IUPAC GoldBook](https://goldbook.iupac.org).

There are several other NFDI consortia including NFDI4Cat (catalysis),
DAPHNE4NFDI (photon and neutron physics), and FAIRmat (materials science) that
have similar goals to annotate instrumentation. While each reuse CHMO to some
extent for this purpose, DAPHNE4NFDI additionally develops the
[Photon and Neutron Experimental Techniques (PANET) Ontology](https://semantic.farm/panet)
and FAIRmat develops the [NeXus format](https://www.nexusformat.org/) and
associated [NeXus Ontology](https://semantic.farm/nexus) as part of the
[NOMAD](https://nomad-lab.eu/nomad-lab/index.html) materials science data
management platform. Further, there are several other resources with similar
goals including the
[Allotrope Foundation Ontology (AFO)](https://www.allotrope.org/ontologieshttps://www.allotrope.org/ontologies),
the deprecated
[Physico-chemical Methods and Properties (FIX)](https://semantic.farm/fix)
ontology, the deprecated
[Physico-chemical process (REX)](https://semantic.farm/rex) ontology,
[IUPAC GoldBook](https://goldbook.iupac.org), and
[Wikidata](https://wikidata.org).

[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)

I implemented a workflow for comparing the manually curated mappings in two
SSSOM documents in
[cthoyt/sssom-pydantic#141](https://github.com/cthoyt/sssom-pydantic/pull/141).

We needed this for recent updates to the as part of work for NFDI4Chem. We are
currently in the process of modernizing and reviving it as a hub for
experimental equipment for NFDI4Chem and other related

We are in the situation where there were two independent efforts to manually
curate semantic mappings between CHMO and external ontologies including PANET,
NEXUS, IUPAC GoldBook, Wikidata, AFO, FIX, and REX.

Our goal is to use the to consume these mappings during the release of CHMO to
both add annotation properties and generate ontology bridge files that can be
used during ontology merging.
