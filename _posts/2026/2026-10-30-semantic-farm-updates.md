---
layout: post
title: Semantic Farm and Bioregistry Updates - October 30th, 2026
date: 2026-10-30 16:40:00 +0100
author: Charles Tapley Hoyt
tags:
  - NFDI
  - NFDI4Chem
  - Bioregistry
  - Semantic Farm
---

This week saw the addition of the
[Library of Congress Class Schemes](https://semantic.farm/metaregistry/loc.classschemes)
registry, an overhaul of the alignment workflow with the
[Zazuko](https://semantic.farm/metaregistry/zazuko) registry, the addition of 18
new records, and finally the update of 222 records in the
[Semantic Farm](https://semantic.farm) and the
[Bioregistry](https://bioregistry.io).

## External Alignment

The Semantic Farm/Bioregistry ingests content from 36 external resources both to
reduce curation burden but also to increase its coverage of resources across a
variety of domains and disciplines.

### Adding Library of Congress Classification Schemes

The United States Library of Congress (LOC) Classification Schemes covers
various classification systems across the natural sciences, humanities, and
library sciences, such as the
[Medical Subject Headings (MeSH)](https://semantic.farm/mesh),
[Iconclass](https://semantic.farm/iconclass), and
[Dewey Decimal Classification (DDC)](https://semantic.farm/ddc). I implemented
an alignment workflow that ingests its entries and semi-automatically maps them
to Semantic Farm/Bioregistry records based on lexical matching of prefixes in
[biopragmatics/bioregistry#2156](https://github.com/biopragmatics/bioregistry/issues/2156).

Compared to other external registries, LOC Classification Schemes is information
poor - it only contains prefixes and names for its records, whereas external
registries like Identifiers.org have higher minimum metadata standards. A
comparison of metadata standards across all 36 external registries is available
[here](https://semantic.farm/related) and is automatically updated when new ones
(like LOC) are added!

### Updating Zazuko

[Zazuko](https://zazuko.com) is a company that builds semantic web technologies
and solutions. It develops several of its own controlled vocabularies and
ontologies to support its work, and importantly hosts
<https://prefix.zazuko.com>, a unique frontend to many key semantic web
controlled vocabularies and ontologies.

I recently found that they host metadata about the resources they index that
isn't available through its API, but rather through RDF files in N-tuples format
on their GitHub repository (e.g., for
[Cube schema](https://raw.githubusercontent.com/zazuko/rdf-vocabularies/refs/heads/master/ontologies/cube/meta.nt)).
Therefore, I updated the alignment workflow in
[biopragmatics/bioregistry#2144](https://github.com/biopragmatics/bioregistry/issues/2144)
to parse key metadata such as names and descriptions. Given this new context, I
was motivated to curate the remaining information for dozens of these resources
in order to meet the Semantic Farm/Bioregistry's minimum metadata standards for
new records.

There are countless opportunities for ingesting new records from external
records, which are perfect for new curators who are interested to get involved.
If that sounds like you, have a look at
[this curation guide](https://github.com/biopragmatics/bioregistry/blob/main/docs/curation-import-external.md).

## New Records

The Semantic Farm/Bioregistry enables the community to submit new records to
best cover their resources and resources they use. This week had two external
contributions that were accepted (with several under review):

- [FAIR Mappings Schema (fairmap)](https://semantic.farm/fairmap) was
  contributed by [Nico Matentzoglu](https://orcid.org/0000-0002-7356-1779) as
  part of the ongoing work of the
  [RDA FAIR Mappings Working Group](https://mapping-commons.github.io/rda-fair-mappings/)
  in
  [biopragmatics/bioregistry#2147](https://github.com/biopragmatics/bioregistry/issues/2147).
- [Scholarly Entity International Persistent Identifier Infrastructure (seipid)](https://semantic.farm/seipid)
  was contributed by [Nasir Razzaq](https://orcid.org/0000-0001-6939-2856) on
  behalf of his firm [Xpertno Research Center](https://xrc.xpertno.com) in
  Pakistan in
  [biopragmatics/bioregistry#2148](https://github.com/biopragmatics/bioregistry/issues/2148)

I contributed [XHTML Datatypes (xh11d)](https://semantic.farm/xh11d), then
curated mappings from the LinkML core metamodel types to `xh11d` in
[linkml/linkml-model#289](https://github.com/linkml/linkml-model/pull/289),
giving [LinkML](https://linkml.io) a better grounding to previously established
semantic web standards.

[Universal Decimal Classification (UDC)](https://semantic.farm/udc) was added in
[biopragmatics/bioregistry#2153](https://github.com/biopragmatics/bioregistry/issues/2153)
in order to complete the mapping from Dublin Core Terms
[encoding schemes](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-4)
to corresponding records in the Semantic Farm/Bioregistry. The other eight
schemes listed already had corresponding records.

The remaining new records were all ingested from
[Zazuko](https://semantic.farm/metaregistry/zazuko) and appropriately enriched
to meet minimum metadata requirements for the Semantic Farm/Bioregistry in
[biopragmatics/bioregistry#2144](https://github.com/biopragmatics/bioregistry/issues/2144).

| Prefix                                                             | Name                                                                |
|--------------------------------------------------------------------|---------------------------------------------------------------------|
| [b59](https://semantic.farm/b59)                                   | barnard59                                                           |
| [cube.meta](https://semantic.farm/cube.meta)                       | Cube Schema meta data extension                                     |
| [cube.relation](https://semantic.farm/cube.relation)               | Cube Schema relation vocabulary                                     |
| [cube.schema](https://semantic.farm/cube.schema)                   | Cube schema                                                         |
| [duv](https://semantic.farm/duv)                                   | Dataset Usage Vocabulary                                            |
| [fairmap](https://semantic.farm/fairmap)                           | FAIR Mappings Schema                                                |
| [qudt.constant](https://semantic.farm/qudt.constant)               | QUDT VOCAB Physical Constants Release 3.1.10                        |
| [qudt.currency](https://semantic.farm/qudt.currency)               | QUDT VOCAB Currency Units Release 3.0.0                             |
| [qudt.dimensionvector](https://semantic.farm/qudt.dimensionvector) | QUDT VOCAB Dimension Vectors Release 3.1.10                         |
| [qudt.discipline](https://semantic.farm/qudt.discipline)           | QUDT Disciplines Ontology                                           |
| [qudt.prefix](https://semantic.farm/qudt.prefix)                   | QUDT VOCAB Decimal Prefixes                                         |
| [qudt.quantitykind](https://semantic.farm/qudt.quantitykind)       | QUDT Quantity Kind Vocabulary                                       |
| [qudt.sou](https://semantic.farm/qudt.sou)                         | QUDT VOCAB Systems of Units Release 3.1.10                          |
| [qudt.unit](https://semantic.farm/qudt.unit)                       | QUDT VOCAB Units of Measure                                         |
| [rr](https://semantic.farm/rr)                                     | R2RML vocabulary                                                    |
| [seipid](https://semantic.farm/seipid)                             | Scholarly Entity International Persistent Identifier Infrastructure |
| [udc](https://semantic.farm/udc)                                   | Universal Decimal Classification                                    |
| [xh11d](https://semantic.farm/xh11d)                               | XHTML Datatypes                                                     |

## Updated Records

There were 238 updates, which came from a combination of alignment to LOC Class
Schemes, enrichment from metadata from Zazuko, and other updates ingested from
external registries.

Of those updates, only one was done as a stand-alone contribution. I updated the
record for the
[Gainesville Core Ontology](https://semantic.farm/gainesville.core) record in
[biopragmatics/bioregistry#2152](https://github.com/biopragmatics/bioregistry/issues/2152)
to ensure that it links to a downloadable OWL file in preparation for the
[Ontologies4Chem](https://nfdi4chem.de/event/5th-ontologies4chem-workshop/)
conference next week.

| Updated Prefix                                                 | Name                                                                              |
|----------------------------------------------------------------|-----------------------------------------------------------------------------------|
| [ac](https://semantic.farm/ac)                                 | Activity Streams                                                                  |
| [acl](https://semantic.farm/acl)                               | Basic Access Control ontology                                                     |
| [afo](https://semantic.farm/afo)                               | Allotrope Merged Ontology Suite                                                   |
| [agricola](https://semantic.farm/agricola)                     | Agricultural Online Access                                                        |
| [ahol](https://semantic.farm/ahol)                             | Animal Health Ontology for Livestock                                              |
| [aio](https://semantic.farm/aio)                               | The Artificial Intelligence Ontology                                              |
| [APO](https://semantic.farm/apo)                               | Ascomycete phenotype ontology                                                     |
| [APOLLO_SV](https://semantic.farm/apollosv)                    | Apollo Structured Vocabulary                                                      |
| [atc](https://semantic.farm/atc)                               | Anatomical Therapeutic Chemical Classification System                             |
| [atol](https://semantic.farm/atol)                             | Animal Trait Ontology for Livestock                                               |
| [bao](https://semantic.farm/bao)                               | BioAssay Ontology                                                                 |
| [bcio](https://semantic.farm/bcio)                             | The Behaviour Change Intervention Ontology                                        |
| [BERVO](https://semantic.farm/bervo)                           | Biological and Environmental Research Variable Ontology                           |
| [bibo](https://semantic.farm/bibo)                             | The Bibliographic Ontology                                                        |
| [biodivthes](https://semantic.farm/biodivthes)                 | Biodiversity Thesaurus                                                            |
| [biolink](https://semantic.farm/biolink)                       | BioLink Model                                                                     |
| [biomodels.teddy](https://semantic.farm/biomodels.teddy)       | Terminology for Description of Dynamics                                           |
| [biotop](https://semantic.farm/biotop)                         | BioTop                                                                            |
| [birnlex](https://semantic.farm/birnlex)                       | Biomedical Informatics Research Network Lexicon                                   |
| [bko](https://semantic.farm/bko)                               | SBGN Bricks data and ontology                                                     |
| [cc](https://semantic.farm/cc)                                 | Creative Commons Rights Expression Language                                       |
| [ccf](https://semantic.farm/ccf)                               | Human Reference Atlas Common Coordinate Framework Ontology                        |
| [cco](https://semantic.farm/cco)                               | Cell Cycle Ontology                                                               |
| [ccon](https://semantic.farm/ccon)                             | Cerrado Concepts Ontology                                                         |
| [cellosaurus](https://semantic.farm/cellosaurus)               | Cellosaurus                                                                       |
| [cert](https://semantic.farm/cert)                             | The Cert Ontology                                                                 |
| [CHEBI](https://semantic.farm/chebi)                           | Chemical Entities of Biological Interest                                          |
| [chemfont.chemical](https://semantic.farm/chemfont.chemical)   | ChemFOnt chemical                                                                 |
| [ChEMROF](https://semantic.farm/chemrof)                       | Chemical Entity Materials and Reactions Ontological Framework                     |
| [CHMO](https://semantic.farm/chmo)                             | Chemical Methods Ontology                                                         |
| [CHR](https://semantic.farm/chr)                               | Chromosome Ontology                                                               |
| [cidoc.crm](https://semantic.farm/cidoc.crm)                   | CIDOC Conceptual Reference Model                                                  |
| [CL](https://semantic.farm/cl)                                 | Cell Ontology                                                                     |
| [cmc.umg](https://semantic.farm/cmc.umg)                       | Cell Model Catalogue Göttingen                                                    |
| [cmpo](https://semantic.farm/cmpo)                             | Cellular Microscopy Phenotype Ontology                                            |
| [cnt](https://semantic.farm/cnt)                               | Representing Content in RDF                                                       |
| [covid19](https://semantic.farm/covid19)                       | SARS-CoV-2                                                                        |
| [cryoem](https://semantic.farm/cryoem)                         | Cryo Electron Microscopy ontology                                                 |
| [csp](https://semantic.farm/csp)                               | Computer Retrieval of Information on Science Projects Thesaurus                   |
| [csvw](https://semantic.farm/csvw)                             | CSV on the Web Vocabulary                                                         |
| [ctcae](https://semantic.farm/ctcae)                           | Common Terminology Criteria for Adverse Events                                    |
| [DataCite](https://semantic.farm/datacite)                     | DataCite Ontology                                                                 |
| [dbo](https://semantic.farm/dbo)                               | DBPedia Ontology                                                                  |
| [dc](https://semantic.farm/dc)                                 | Dublin Core Elements (1.1)                                                        |
| [dcam](https://semantic.farm/dcam)                             | Dublin Core Metadata Initiative Abstract Model                                    |
| [dcat](https://semantic.farm/dcat)                             | Data Catalog                                                                      |
| [dcmitype](https://semantic.farm/dcmitype)                     | DCMI Type Vocabulary                                                              |
| [dcterms](https://semantic.farm/dcterms)                       | Dublin Core Metadata Initiative Terms                                             |
| [ddc](https://semantic.farm/ddc)                               | Dewey Decimal Classification                                                      |
| [ddi](https://semantic.farm/ddi)                               | Data Documentation Initiative Vocabulary                                          |
| [dermo](https://semantic.farm/dermo)                           | Human Dermatological Disease Ontology                                             |
| [dicom](https://semantic.farm/dicom)                           | Digital Imaging and Communications in Medicine ontology                           |
| [doap](https://semantic.farm/doap)                             | Description of a Project                                                          |
| [DOID](https://semantic.farm/doid)                             | Human Disease Ontology                                                            |
| [DPO](https://semantic.farm/dpo)                               | Drosophila Phenotype Ontology                                                     |
| [dqv](https://semantic.farm/dqv)                               | Data Quality Vocabulary                                                           |
| [DRON](https://semantic.farm/dron)                             | The Drug Ontology                                                                 |
| [dsw](https://semantic.farm/dsw)                               | Darwin Semantic Web Ontology                                                      |
| [earl](https://semantic.farm/earl)                             | Evaluation and Report Language                                                    |
| [ecg](https://semantic.farm/ecg)                               | Electrocardiogram Ontology                                                        |
| [ECOCORE](https://semantic.farm/ecocore)                       | An ontology of core ecological entities                                           |
| [ecso](https://semantic.farm/ecso)                             | The Ecosystem Ontology                                                            |
| [ECTO](https://semantic.farm/ecto)                             | Environmental conditions, treatments and exposures ontology                       |
| [edda](https://semantic.farm/edda)                             | EDDA Study Designs Taxonomy                                                       |
| [EFO](https://semantic.farm/efo)                               | Experimental Factor Ontology                                                      |
| [ENVO](https://semantic.farm/envo)                             | Environment Ontology                                                              |
| [envthes](https://semantic.farm/envthes)                       | Thesaurus for long-term ecological research, monitoring, experiments              |
| [eol](https://semantic.farm/eol)                               | Environment Ontology for Livestock                                                |
| [epso](https://semantic.farm/epso)                             | Epilepsy and Seizure Ontology                                                     |
| [evorao](https://semantic.farm/evorao)                         | EVORA Ontology                                                                    |
| [exif](https://semantic.farm/exif)                             | Exif data description vocabulary                                                  |
| [fabio](https://semantic.farm/fabio)                           | The FRBR-aligned Bibliographic Ontology                                           |
| [faldo](https://semantic.farm/faldo)                           | Feature Annotation Location Description Ontology                                  |
| [FBbt](https://semantic.farm/fbbt)                             | Drosophila gross anatomy                                                          |
| [FBcv](https://semantic.farm/fbcv)                             | FlyBase Controlled Vocabulary                                                     |
| [FBdv](https://semantic.farm/fbdv)                             | Drosophila development                                                            |
| [FBSP](https://semantic.farm/fbsp)                             | Fly taxonomy                                                                      |
| [FLOPO](https://semantic.farm/flopo)                           | Flora Phenotype Ontology                                                          |
| [FMA](https://semantic.farm/fma)                               | Foundational Model of Anatomy                                                     |
| [foaf](https://semantic.farm/foaf)                             | Friend of a Friend                                                                |
| [FOODON](https://semantic.farm/foodon)                         | The Food Ontology                                                                 |
| [fplx](https://semantic.farm/fplx)                             | FamPlex                                                                           |
| [FRBR](https://semantic.farm/frbr)                             | Functional Requirements for Bibliographic Records                                 |
| [FYPO](https://semantic.farm/fypo)                             | Fission Yeast Phenotype Ontology                                                  |
| [gainesville.core](https://semantic.farm/gainesville.core)     | Gainesville Core Ontology                                                         |
| [galen](https://semantic.farm/galen)                           | GALEN                                                                             |
| [geonames.ontology](https://semantic.farm/geonames.ontology)   | GeoNames Ontology                                                                 |
| [geosparql](https://semantic.farm/geosparql)                   | GeoSPARQL                                                                         |
| [geosparql.function](https://semantic.farm/geosparql.function) | GeoSPARQL Function                                                                |
| [geosparql.rule](https://semantic.farm/geosparql.rule)         | GeoSPARQL Rule                                                                    |
| [gexo](https://semantic.farm/gexo)                             | Gene Expression Ontology                                                          |
| [gfo](https://semantic.farm/gfo)                               | General Formal Ontology                                                           |
| [gist](https://semantic.farm/gist)                             | gist ontology                                                                     |
| [GO](https://semantic.farm/go)                                 | Gene Ontology                                                                     |
| [gpml](https://semantic.farm/gpml)                             | WikiPathways GPML Vocabulary                                                      |
| [gr](https://semantic.farm/gr)                                 | GoodRelations                                                                     |
| [GRO](https://semantic.farm/gramene.growthstage)               | Gramene Growth Stage Ontology                                                     |
| [grddl](https://semantic.farm/grddl)                           | Gleaning Resource Descriptions from Dialects of Languages                         |
| [gs1](https://semantic.farm/gs1)                               | GS1 Web Vocabulary                                                                |
| [hcpcs](https://semantic.farm/hcpcs)                           | Healthcare Common Procedure Coding System                                         |
| [hgnc](https://semantic.farm/hgnc)                             | HUGO Gene Nomenclature Committee                                                  |
| [hl7](https://semantic.farm/hl7)                               | HL7 External Code System                                                          |
| [hoip](https://semantic.farm/hoip)                             | Homeostasis imbalance process ontology                                            |
| [HP](https://semantic.farm/hp)                                 | Human Phenotype Ontology                                                          |
| [hydra](https://semantic.farm/hydra)                           | The Hydra Core Vocabulary                                                         |
| [icaltzd](https://semantic.farm/icaltzd)                       | iCalendar with Time Zone                                                          |
| [icd10cm](https://semantic.farm/icd10cm)                       | International Classification of Diseases, 10th Revision, Clinical Modification    |
| [icd10pcs](https://semantic.farm/icd10pcs)                     | International Classification of Diseases, 10th Revision, Procedure Coding System  |
| [icd9](https://semantic.farm/icd9)                             | International Classification of Diseases, 9th Revision                            |
| [icd9cm](https://semantic.farm/icd9cm)                         | International Classification of Diseases, 9th Revision, Clinical Modification     |
| [icf](https://semantic.farm/icf)                               | International Classification of Functioning, Disability and Health                |
| [iconclass](https://semantic.farm/iconclass)                   | Iconclass Classification                                                          |
| [idocovid19](https://semantic.farm/idocovid19)                 | The COVID-19 Infectious Disease Ontology                                          |
| [idoden](https://semantic.farm/idoden)                         | Dengue Fever Ontology                                                             |
| [inbio](https://semantic.farm/inbio)                           | Invasion Biology Ontology                                                         |
| [inchi](https://semantic.farm/inchi)                           | International Chemical Identifier                                                 |
| [interlex](https://semantic.farm/interlex)                     | InterLex                                                                          |
| [iobc](https://semantic.farm/iobc)                             | Interlinking Ontology for Biological Concepts                                     |
| [ito](https://semantic.farm/ito)                               | Intelligence Task Ontology                                                        |
| [jcrb](https://semantic.farm/jcrb)                             | Japanese Collection of Research Bioresources Cell Bank                            |
| [lbo](https://semantic.farm/lbo)                               | Livestock Breed Ontology                                                          |
| [ldp](https://semantic.farm/ldp)                               | Linked Data Platform Vocabulary                                                   |
| [legacy.capcldb](https://semantic.farm/legacy.capcldb)         | Prostate Cancer Cell Line Database                                                |
| [lexvo.ontology](https://semantic.farm/lexvo.ontology)         | Lexvo Ontology                                                                    |
| [loc.classschemes](https://semantic.farm/loc.classschemes)     | Library of Congress Classification Schemes                                        |
| [locn](https://semantic.farm/locn)                             | ISA Programme Location Core Vocabulary                                            |
| [log](https://semantic.farm/log)                               | SWAP Logic Ontology                                                               |
| [loinc](https://semantic.farm/loinc)                           | Logical Observation Identifiers Names and Codes                                   |
| [lpt](https://semantic.farm/lpt)                               | Livestock Product Trait Ontology                                                  |
| [m4i](https://semantic.farm/m4i)                               | Metadata4Ing                                                                      |
| [medlineplus](https://semantic.farm/medlineplus)               | MedlinePlus                                                                       |
| [mesh](https://semantic.farm/mesh)                             | Medical Subject Headings                                                          |
| [metabobank](https://semantic.farm/metabobank)                 | MetaboBank                                                                        |
| [METPO](https://semantic.farm/metpo)                           | Microbial Ecophysiological Trait and Phenotype Ontology                           |
| [MIXS](https://semantic.farm/mixs)                             | Minimum Information about any (x) Sequence                                        |
| [MOD](https://semantic.farm/mod)                               | PSI-MOD Protein Modifications Ontology                                            |
| [modsci](https://semantic.farm/modsci)                         | Modern Science Ontology                                                           |
| [MOLSIM](https://semantic.farm/molsim)                         | Molecular Simulation Ontology                                                     |
| [mosaic](https://semantic.farm/mosaic)                         | MOSAiC Ontology                                                                   |
| [MRO](https://semantic.farm/mro)                               | MHC Restriction Ontology                                                          |
| [msc](https://semantic.farm/msc)                               | Mathematics Subject Classification                                                |
| [mwo](https://semantic.farm/mwo)                               | NFDI MatWerk Ontology                                                             |
| [nando](https://semantic.farm/nando)                           | Nanbyo Disease Ontology                                                           |
| [nemo2](https://semantic.farm/nemo2)                           | Neural ElectroMagnetic Ontology                                                   |
| [nexus](https://semantic.farm/nexus)                           | NeXus Ontology                                                                    |
| [NIF_CELL](https://semantic.farm/nif.cell)                     | NIF Cell                                                                          |
| [nlm](https://semantic.farm/nlm)                               | National Library of Medicine Catalog                                              |
| [npo](https://semantic.farm/npo)                               | NanoParticle Ontology                                                             |
| [oa](https://semantic.farm/oa)                                 | Web Annotation Ontology                                                           |
| [OBA](https://semantic.farm/oba)                               | Ontology of Biological Attributes                                                 |
| [OBI](https://semantic.farm/obi)                               | Ontology for Biomedical Investigations                                            |
| [og](https://semantic.farm/og)                                 | Open Graph protocol                                                               |
| [ogc.sf](https://semantic.farm/ogc.sf)                         | Open Geospatial Consortium Simple Features Vocabulary                             |
| [OHD](https://semantic.farm/ohd)                               | Oral Health and Disease Ontology                                                  |
| [oidc](https://semantic.farm/oidc)                             | Solid OpenID Connect vocabulary                                                   |
| [om](https://semantic.farm/om)                                 | Ontology of units of Measure                                                      |
| [omim](https://semantic.farm/omim)                             | Online Mendelian Inheritance in Man                                               |
| [OMO](https://semantic.farm/omo)                               | OBO Metadata Ontology                                                             |
| [OMRSE](https://semantic.farm/omrse)                           | Ontology for Modeling and Representation of Social Entities                       |
| [OOSTT](https://semantic.farm/oostt)                           | Ontology of Organizational Structures of Trauma centers and Trauma systems        |
| [opb](https://semantic.farm/opb)                               | Ontology of Physics for Biology                                                   |
| [org](https://semantic.farm/org)                               | Core organization ontology                                                        |
| [orphanet.ordo](https://semantic.farm/orphanet.ordo)           | Orphanet Rare Disease Ontology                                                    |
| [orth](https://semantic.farm/orth)                             | Orthology Ontology                                                                |
| [owl](https://semantic.farm/owl)                               | Web Ontology Language                                                             |
| [panet](https://semantic.farm/panet)                           | Photon and Neutron Experimental Techniques Ontology                               |
| [PATO](https://semantic.farm/pato)                             | Phenotype And Trait Ontology                                                      |
| [phenx](https://semantic.farm/phenx)                           | PhenX Toolkit                                                                     |
| [PHIPO](https://semantic.farm/phipo)                           | Pathogen Host Interaction Phenotype Ontology                                      |
| [plos](https://semantic.farm/plos)                             | PLOS Thesaurus                                                                    |
| [PREFER](https://semantic.farm/prefer)                         | Precision Fermentation Ontology                                                   |
| [prov](https://semantic.farm/prov)                             | PROV Namespace                                                                    |
| [qb](https://semantic.farm/qb)                                 | The data cube vocabulary                                                          |
| [qudt](https://semantic.farm/qudt)                             | Quantities, Units, Dimensions, and Types Ontology                                 |
| [radlex](https://semantic.farm/radlex)                         | RSNA Informatics RadLex                                                           |
| [rcb](https://semantic.farm/rcb)                               | RIKEN Bioresource Center Cell Bank                                                |
| [rdf](https://semantic.farm/rdf)                               | Resource Description Framework                                                    |
| [rdfa](https://semantic.farm/rdfa)                             | RDFa Vocabulary for Term and Prefix Assignment, and for Processor Graph Reporting |
| [rdfs](https://semantic.farm/rdfs)                             | RDF Schema                                                                        |
| [reproduceme](https://semantic.farm/reproduceme)               | REPRODUCE-ME Ontology                                                             |
| [reto](https://semantic.farm/reto)                             | Regulation of Transcription Ontology                                              |
| [rexo](https://semantic.farm/rexo)                             | Regulation of Gene Expression Ontology                                            |
| [RO](https://semantic.farm/ro)                                 | Relation Ontology                                                                 |
| [RoleO](https://semantic.farm/roleo)                           | Role Ontology                                                                     |
| [ror](https://semantic.farm/ror)                               | Research Organization Registry                                                    |
| [rrid](https://semantic.farm/rrid)                             | Research Resource Identification                                                  |
| [rxnorm](https://semantic.farm/rxnorm)                         | RxNorm                                                                            |
| [salmon](https://semantic.farm/salmon)                         | Salmon Ontology                                                                   |
| [saref.ehaw](https://semantic.farm/saref.ehaw)                 | SAREF4EHAW: an extension of SAREF for eHealth Ageing Well domain                  |
| [sasap](https://semantic.farm/sasap)                           | The State of Alaska's Salmon and People Ontology                                  |
| [schema](https://semantic.farm/schema)                         | Schema.org                                                                        |
| [sd](https://semantic.farm/sd)                                 | SPARQL 1.1 Service Description                                                    |
| [sdmx](https://semantic.farm/sdmx)                             | SDMX-RDF vocabulary                                                               |
| [sh](https://semantic.farm/sh)                                 | Shapes Constraint Language                                                        |
| [shex](https://semantic.farm/shex)                             | Shape Expression Vocabulary                                                       |
| [shsh](https://semantic.farm/shsh)                             | SHACL in SHACL                                                                    |
| [sioc.core](https://semantic.farm/sioc.core)                   | Semantically-Interlinked Online Communities Core Ontology                         |
| [skos](https://semantic.farm/skos)                             | Simple Knowledge Organization System                                              |
| [skosxl](https://semantic.farm/skosxl)                         | Simple Knowledge Organization System eXtension for Labels                         |
| [smiles](https://semantic.farm/smiles)                         | Simplified molecular-input line-entry system                                      |
| [solid](https://semantic.farm/solid)                           | Solid Terms                                                                       |
| [sosa](https://semantic.farm/sosa)                             | Sensor, Observation, Sample, and Actuator Ontology                                |
| [ssn](https://semantic.farm/ssn)                               | Semantic Sensor Network Ontology                                                  |
| [sstim](https://semantic.farm/sstim)                           | Sensory Stimulation Ontology                                                      |
| [stemmcellbank](https://semantic.farm/stemmcellbank)           | CReM iPSC Catalog                                                                 |
| [sty](https://semantic.farm/sty)                               | UMLS Semantic Types Ontology                                                      |
| [suzhou.cell](https://semantic.farm/suzhou.cell)               | Suzhou Research Institute Cell Bank                                               |
| [SYMP](https://semantic.farm/symp)                             | Symptom Ontology                                                                  |
| [tib.bk](https://semantic.farm/tib.bk)                         | Basic Classification                                                              |
| [time](https://semantic.farm/time)                             | Time Ontology in OWL                                                              |
| [ubigene](https://semantic.farm/ubigene)                       | UbiGene                                                                           |
| [uniprot](https://semantic.farm/uniprot)                       | UniProt Protein                                                                   |
| [uniprot.core](https://semantic.farm/uniprot.core)             | Uniprot Core Ontology                                                             |
| [UO](https://semantic.farm/uo)                                 | Units of measurement ontology                                                     |
| [UPHENO](https://semantic.farm/upheno)                         | Unified Phenotype Ontology                                                        |
| [valuesets](https://semantic.farm/valuesets)                   | Value Sets                                                                        |
| [vandf](https://semantic.farm/vandf)                           | Veterans Administration National Drug File                                        |
| [vann](https://semantic.farm/vann)                             | A vocabulary for annotating vocabulary descriptions                               |
| [vcard](https://semantic.farm/vcard)                           | Virtual Contact File                                                              |
| [vido](https://semantic.farm/vido)                             | Virus Infectious Disease Ontology                                                 |
| [vivo](https://semantic.farm/vivo)                             | VIVO Ontology                                                                     |
| [vmh.gene](https://semantic.farm/vmh.gene)                     | Virtual Metabolic Human gene                                                      |
| [vmh.metabolite](https://semantic.farm/vmh.metabolite)         | Virtual Metabolic Human metabolite                                                |
| [vmh.reaction](https://semantic.farm/vmh.reaction)             | Virtual Metabolic Human reaction                                                  |
| [VO](https://semantic.farm/vo)                                 | Vaccine Ontology                                                                  |
| [void](https://semantic.farm/void)                             | Vocabulary of Interlinked Datasets                                                |
| [vs](https://semantic.farm/vs)                                 | SemWeb Vocab Status ontology                                                      |
| [vso](https://semantic.farm/vso)                               | Vital Sign Ontology                                                               |
| [VT](https://semantic.farm/vt)                                 | Vertebrate trait ontology                                                         |
| [WBPhenotype](https://semantic.farm/wbphenotype)               | C. elegans phenotype                                                              |
| [wdrs](https://semantic.farm/wdrs)                             | Protocol for Web Description Resources (POWDER): POWDER-S Vocabulary              |
| [wgs84](https://semantic.farm/wgs84)                           | WGS84 Geo Positioning                                                             |
| [XCO](https://semantic.farm/xco)                               | Experimental condition ontology                                                   |
| [xhv](https://semantic.farm/xhv)                               | XHTML Vocabulary                                                                  |
| [xkos](https://semantic.farm/xkos)                             | An SKOS extension for representing statistical classifications                    |
| [xsd](https://semantic.farm/xsd)                               | XML Schema Definition                                                             |
| [ZFA](https://semantic.farm/zfa)                               | Zebrafish anatomy and development ontology                                        |
| [ZFS](https://semantic.farm/zfs)                               | Zebrafish developmental stages ontology                                           |
