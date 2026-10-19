---
layout: post
title: Semantic Farm Updates from Early October 2026
date: 2026-10-19 12:44:00 +0200
author: Charles Tapley Hoyt
tags:
  - NFDI
  - NFDI4Chem
  - Bioregistry
  - Semantic Farm
---

We added 80 new records, updated 54 records, and made a constellation of
improvements and updates to the [Semantic Farm](https://semantic.farm) and
[Bioregistry](https://bioregistry.io) in the first two weeks of October 2026.
This post gives more detail and links to external resources for further reading.

For new readers, a brief reminder that the Semantic Farm is a domain-agnostic
generalization on the Bioregistry to better serve other natural sciences,
engineering sciences, and humanities and social sciences communities, especially
within the context of the NFDI.

## Highlights

1. Records were added for ontologies from the
   [World Avatar](https://theworldavatar.io), which support multiscale modeling
   from the molecular level to municipal systems and weather patterns. I wrote
   about this in detail in [my previous post]({% post_url
   2026/2026-10-02-world-avatar %})
2. A record describing the
   [European Synchrotron Radiation Facility (ESFR) Experimental Techniques Ontology (ESRFET)](https://semantic.farm/esrfet)
   was added and members of DAPHNE4NFDI suggested several improvements to
   physics-related ontologies, including the
   [NeXus Ontology (`nexus`)](https://semantic.farm/nexus) (also used
   DAPHNE4NFDI, FAIRmat, and NFDI-MatWerk) and the
   [Photon and Neutron Experimental Techniques Ontology (`PaNET`)](https://semantic.farm/panet)).
   This demonstrates the relatively low barrier for community involvement in the
   Semantic Farm and that NFDI consortia and their respective members can take
   initiative to maintain records describing both their first-party resources
   and third-party resources they use.
3. Improved workflow for ingesting and aligning records for ontologies in the
   [Open Biological and Biomedical Ontology (OBO) Foundry](https://obofoundry.org/).
   I wrote about this in detail [here]({% post_url
   2026/2026-10-19-obofoundry-custom-uri-prefixes %}).
4. Implemented a draft workflow for calculating ontology reuse as part of NFDI
   Section Metadata Working Group for Ontology Harmonization and Mapping's
   agenda for summarizing ontology usage across NFDI consortia. See the
   [pull request](https://github.com/biopragmatics/bioregistry/pull/2132) and
   [results](https://github.com/biopragmatics/bioregistry/blob/main/exports/analyses/usage/README.md).

## New Prefixes

Aside from the 74 new records added for ontologies from the World Avatar
project, six new records were added, five of which cover cell and cell line
resources appearing in [Cellosaurus](https://cellosaurus.org) cross-references.

| Added Prefix                                           | Name                                |
|--------------------------------------------------------|-------------------------------------|
| [cmc.umg](https://semantic.farm/cmc.umg)               | Cell Model Catalogue Göttingen      |
| [legacy.capcldb](https://semantic.farm/legacy.capcldb) | Prostate Cancer Cell Line Database  |
| [metabobank](https://semantic.farm/metabobank)         | MetaboBank                          |
| [stemmcellbank](https://semantic.farm/stemmcellbank)   | CReM iPSC Catalog                   |
| [suzhou.cell](https://semantic.farm/suzhou.cell)       | Suzhou Research Institute Cell Bank |
| [ubigene](https://semantic.farm/ubigene)               | UbiGene                             |

## Updated Prefixes

In total, 54 prefixes were updated

| Prefix                                                             | Name                                                                        |
|--------------------------------------------------------------------|-----------------------------------------------------------------------------|
| [addicto](https://semantic.farm/addicto)                           | Addiction Ontology                                                          |
| [afo](https://semantic.farm/afo)                                   | Allotrope Merged Ontology Suite                                             |
| [agrovoc](https://semantic.farm/agrovoc)                           | AGROVOC                                                                     |
| [APO](https://semantic.farm/apo)                                   | Ascomycete phenotype ontology                                               |
| [CHEBI](https://semantic.farm/chebi)                               | Chemical Entities of Biological Interest                                    |
| [chemfont.chemical](https://semantic.farm/chemfont.chemical)       | ChemFOnt chemical                                                           |
| [chemfont.ontology](https://semantic.farm/chemfont.ontology)       | ChemFOnt Ontology                                                           |
| [CMO](https://semantic.farm/cmo)                                   | Clinical measurement ontology                                               |
| [cmpo](https://semantic.farm/cmpo)                                 | Cellular Microscopy Phenotype Ontology                                      |
| [coho](https://semantic.farm/coho)                                 | Cohort Ontology                                                             |
| [dicom](https://semantic.farm/dicom)                               | Digital Imaging and Communications in Medicine ontology                     |
| [DOID](https://semantic.farm/doid)                                 | Human Disease Ontology                                                      |
| [DPO](https://semantic.farm/dpo)                                   | Drosophila Phenotype Ontology                                               |
| [dsw](https://semantic.farm/dsw)                                   | Darwin Semantic Web Ontology                                                |
| [ECOCORE](https://semantic.farm/ecocore)                           | An ontology of core ecological entities                                     |
| [EMAPA](https://semantic.farm/emapa)                               | Mouse Developmental Anatomy Ontology                                        |
| [fabio](https://semantic.farm/fabio)                               | The FRBR-aligned Bibliographic Ontology                                     |
| [FBbt](https://semantic.farm/fbbt)                                 | Drosophila gross anatomy                                                    |
| [FBcv](https://semantic.farm/fbcv)                                 | FlyBase Controlled Vocabulary                                               |
| [FBdv](https://semantic.farm/fbdv)                                 | Drosophila development                                                      |
| [FLOPO](https://semantic.farm/flopo)                               | Flora Phenotype Ontology                                                    |
| [frbrer](https://semantic.farm/frbrer)                             | Functional Requirements for Bibliographic Records Entity-Relationship Model |
| [grddl](https://semantic.farm/grddl)                               | Gleaning Resource Descriptions from Dialects of Languages                   |
| [icd10](https://semantic.farm/icd10)                               | International Classification of Diseases, 10th Revision                     |
| [icd9](https://semantic.farm/icd9)                                 | International Classification of Diseases, 9th Revision                      |
| [inchi](https://semantic.farm/inchi)                               | International Chemical Identifier                                           |
| [iso.3166](https://semantic.farm/iso.3166)                         | ISO 3166-1 Country Code                                                     |
| [jcrb](https://semantic.farm/jcrb)                                 | Japanese Collection of Research Bioresources Cell Bank                      |
| [loc.relator](https://semantic.farm/loc.relator)                   | Library of Congress Relator                                                 |
| [lpt](https://semantic.farm/lpt)                                   | Livestock Product Trait Ontology                                            |
| [MMO](https://semantic.farm/mmo)                                   | Measurement method ontology                                                 |
| [MONDO](https://semantic.farm/mondo)                               | Mondo Disease Ontology                                                      |
| [MOP](https://semantic.farm/mop)                                   | Molecular Process Ontology                                                  |
| [nlm](https://semantic.farm/nlm)                                   | National Library of Medicine Catalog                                        |
| [OBA](https://semantic.farm/oba)                                   | Ontology of Biological Attributes                                           |
| [OHD](https://semantic.farm/ohd)                                   | Oral Health and Disease Ontology                                            |
| [ontocape](https://semantic.farm/ontocape)                         | Ontology for computer aided process engineering                             |
| [orphanet.ordo](https://semantic.farm/orphanet.ordo)               | Orphanet Rare Disease Ontology                                              |
| [PAIN](https://semantic.farm/pain)                                 | The Pain Ontology                                                           |
| [PATO](https://semantic.farm/pato)                                 | Phenotype And Trait Ontology                                                |
| [pfam](https://semantic.farm/pfam)                                 | Pfam protein family                                                         |
| [rcb](https://semantic.farm/rcb)                                   | RIKEN Bioresource Center Cell Bank                                          |
| [smiles](https://semantic.farm/smiles)                             | Simplified molecular-input line-entry system                                |
| [uat](https://semantic.farm/uat)                                   | Unified Astronomy Thesaurus                                                 |
| [UBERON](https://semantic.farm/uberon)                             | Uber Anatomy Ontology                                                       |
| [vmh.gene](https://semantic.farm/vmh.gene)                         | Virtual Metabolic Human gene                                                |
| [vmh.metabolite](https://semantic.farm/vmh.metabolite)             | Virtual Metabolic Human metabolite                                          |
| [vmh.reaction](https://semantic.farm/vmh.reaction)                 | Virtual Metabolic Human reaction                                            |
| [voc4cat](https://semantic.farm/voc4cat)                           | A vocabulary for the catalysis disciplines                                  |
| [VT](https://semantic.farm/vt)                                     | Vertebrate trait ontology                                                   |
| [worldavatar.compchem](https://semantic.farm/worldavatar.compchem) | WorldAvatar computational chemistry ontology                                |
| [worldavatar.kin](https://semantic.farm/worldavatar.kin)           | WorldAvatar ontology for chemical kinetic reaction mechanisms               |
| [WormBase](https://semantic.farm/wormbase)                         | WormBase                                                                    |
| [ZP](https://semantic.farm/zp)                                     | Zebrafish Phenotype Ontology                                                |

---

The Semantic Farm is an open data resource, so if you want to see more detail
about the everyday churn, have a look at recent
[pull requests](https://github.com/biopragmatics/bioregistry/pulls?q=is%3Apr) to
the GitHub repository
