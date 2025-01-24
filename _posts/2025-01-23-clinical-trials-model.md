---
layout: post
title: Data Integration with Clinical Trials and Clinical Studies
date: 2025-01-23 19:23:00 +0100
author: Charles Tapley Hoyt
tags:
  - clinical trials
  - ClinicalTrials.gov
  - ontologies
  - OBI
---

I've recently worked with clinical studies from
[ClinicalTrials.gov](https://clinicaltrials.gov) and
[other international registries](https://bioregistry.io/collection/0000012).
This post is a review on how to access data, a proposal for how it can be
modeled using the
[Ontology for Biomedical Investigations (OBI)](https://obi-ontology.org/), a
[proof-of-concept ontologization](https://w3id.org/biopragmatics/resources/clinicaltrials)
of ClinicalTrials.gov, and some insights into how this data can be integrated
with other resources to address classical problems in drug discovery from a
knowledge graph perspective.

## Table of Contents

1. [Automated download of ClinicalTrails.gov with `clinicaltrials-downloader`](#automated-download)
2. [Summarizing ClincialTrials.gov study types, allocations, and phases](#summarization)
3. [Example clinical studies](#example-clinical-studies)
4. [Proposing an ontology meta-model](#proposing-an-ontology-meta-model)
5. [Proof-of-concept ontology export of ClinicalTrials.gov](#proof-of-concept-ontology-export-of-clinicaltrialsgov)
6. [Reflections and what's missing](#reflections-and-whats-missing)
7. [What's this all useful for, anyway?](#whats-this-all-useful-for-anyway)

## Automated Download

Similar to [ChEMBL]({% post_url 2021-08-05-taming-chembl-sql %}),
[DrugBank]({% post_url 2020-12-14-taming-drugbank %}), and
[UMLS]({% post_url 2023-09-01-umls %}), I authored a Python package,
`clinicaltrials-downloader` that automates download and caching clinical studies
from [ClinicalTrials.gov](https://clinicaltrials.gov). Its source code is
available under the MIT license at
[https://github.com/cthoyt/clinicaltrials-downloader](https://github.com/cthoyt/clinicaltrials-downloader),
and it can be installed with:

```console
$ pip install clinicaltrials_downloader
```

`clinicaltrials-downloader` exposes two main functions for getting the raw,
unprocessed data:

```python
from clinicaltrials_downloader import get_studies, get_studies_slim

# contains all fields, (~2GB, gzipped)
studies = get_studies()

# contains a useful subset of the fields, much smaller (~70MB, gzipped)
studies_slim = get_studies_slim()
```

## Summarization

I generated a few summary tables over the slim subset of ClinicalTrials.gov.
Keep in mind that the data is updated daily, so these statistics reflect the
state of the database in mid-January 2025. Of course, they can be updated
anytime by passing `force=True` to the downloader function to update the local
cache of the database.

### Study Type and Allocation

ClinicalTrials.gov contains three main study types:

1. [interventional study](https://clinicaltrials.gov/study-basics/glossary#interventional-study-clinical-trial)
   (i.e., clinical trial) - a study in which participants are assigned zero or
   more diagnostic, therapeutic, or other types of interventions depending on
   the arm into which they are allocated
2. [observational study](https://clinicaltrials.gov/study-basics/glossary#observational-study) -
   a study in which participants are assessed for biomedical or health outcomes.
   They may receive interventions, but they are not assigned like in
   interventional studies
3. [expanded access](https://clinicaltrials.gov/study-basics/glossary#expanded-access)
   (i.e., compassionate use) - a mechanism through which patients who are not
   participants in a clinical trial to receive access to
   non-approved/experimental medicine.

Interventional studies can be divided into two categories based on their
[allocation](https://clinicaltrials.gov/study-basics/glossary#allocation) - the
used to assign participants to an arm of a clinical study. They are
[randomized](https://clinicaltrials.gov/study-basics/glossary#randomized-allocation)
and non-randomized.

The table below adjusts the internal labels for legibility, aggregates missing
values and `NA` entries, and sorts by most common.

| Study Type      | Allocation     |   Count |
| --------------- | -------------- | ------: |
| Interventional  | Randomized     | 261,643 |
| Observational   |                | 120,775 |
| Interventional  |                |  95,249 |
| Interventional  | Non-Randomized |  42,759 |
| Expanded Access |                |     966 |
|                 |                |     902 |

### Phases

![](https://www.hepb.org/assets/Uploads/_resampled/ResizedImageWzk2OSwzNzBd-Clinical-Trial-Process-FlowChart.png)

Image above from the
[Hepatitis B Foundation](https://www.hepb.org/research-and-programs/hepdeltaconnect/clinical-trials/).

The [phase](https://clinicaltrials.gov/study-basics/glossary#phase) primarily
communicates the objective of a clinical trial (i.e., interventional study).
Observational trials and expanded access studies therefore do not have phases.
There are six common phases appearing on ClinicalTrials.gov:

- [Early Phase 1](https://clinicaltrials.gov/study-basics/glossary#early-phase-1-formerly-listed-as-phase-0)
  (formerly, Phase 0) - Assess oral bioavailability, pharmacokinetics (very
  small group). This is not the same thing as pre-clinical trials, which are
  often done with biochemical assays, cellular assays, and work with model
  organisms.
- [Phase 1](https://clinicaltrials.gov/study-basics/glossary#phase-1) - Assess
  safety in healthy volunteers (small group)
- [Phase 2](https://clinicaltrials.gov/study-basics/glossary#phase-2) - Assess
  efficacy and side effects (medium group)
- [Phase 3](https://clinicaltrials.gov/study-basics/glossary#phase-3) - Assess
  efficacy, effectiveness, and safety ( large group)
- [Phase 4](https://clinicaltrials.gov/study-basics/glossary#phase-4) -
  Post-approval surveillance
- [Phase Not Applicable (N/A)](https://clinicaltrials.gov/study-basics/glossary#phase-not-applicable) -
  Applied to trials without phases, such as trials with devices or behavioral
  interventions

The table below adjusts the internal clinical trial phases' labels for
legibility, aggregates missing values and `NA` entries, and sorts by
progression.

| Phase          |   Count |
| -------------- | ------: |
| 0              |   5,434 |
| 1              |  44,195 |
| 1, 2           |  15,219 |
| 2              |  59,412 |
| 2, 3           |   6,982 |
| 3              |  39,160 |
| 4              |  33,129 |
| N/A or missing | 318,763 |

Some trials are annotated with multiple phases, either 1/2 or 2/3. These could
also be combined in a different way for "maximum clinical phase" aggregation
operations.

Unsurprisingly, there is an attrition through the progression of phases, but it
is not as stark as I would have expected. It might also be interesting to
stratify this by year to see if trials are more likely to succeed as time goes
on.

## Example Clinical Studies

Having examples and doing spot-checks is always helpful when exploring new data,
so I generated a table containing example clinical trials for each study type,
allocation, and phase. While there are many studies with more than one
intervention and/or condition, this table only shows trials with a single one of
each to reduce complexity.

| Study/Phase(s)             | NCT ID                                                           | Title                                                                           | Condition                                                        | Intervention                                                        | Structure                                                   |
| -------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------- | ----------------------------------------------------------- |
| Expanded Access            | [NCT01317953](https://bioregistry.io/clinicaltrials:NCT01317953) | Oral Green Tea Extract for Small Cell Lung Cancer                               | [Small Cell Lung Carcinoma](https://bioregistry.io/mesh:D055752) | [(-)-epigallocatechin 3-gallate](https://bioregistry.io/chebi:4806) | ![](https://bioregistry.io/chebi:4806?provider=chebi-img)   |
| Observational              | [NCT03418987](https://bioregistry.io/clinicaltrials:NCT03418987) | The Vertebral Vector in a Horizontal Plane. A Simple Way to See in 3D.          | [Scoliosis](https://bioregistry.io/mesh:D012600)                 |                                                                     |                                                             |
| Non-Randomized (Phase 0)   | [NCT01209533](https://bioregistry.io/clinicaltrials:NCT01209533) | Inhaled Iloprost in Mild Asthma                                                 | [Asthma](https://bioregistry.io/mesh:D001249)                    | [iloprost](https://bioregistry.io/chebi:63916)                      | ![](https://bioregistry.io/chebi:63916?provider=chebi-img)  |
| Non-Randomized (Phase 1)   | [NCT01682187](https://bioregistry.io/clinicaltrials:NCT01682187) | A Dose-Escalation Study in Participants With Recurrent Malignant Glioma         | [Glioma](https://bioregistry.io/mesh:D005910)                    | [lomustine](https://bioregistry.io/chebi:6520)                      | ![](https://bioregistry.io/chebi:6520?provider=chebi-img)   |
| Non-Randomized (Phase 1/2) | [NCT00379587](https://bioregistry.io/clinicaltrials:NCT00379587) | Rituximab for Prevention of Chronic GVHD                                        | [Hematologic Neoplasms](https://bioregistry.io/mesh:D019337)     | [rituximab](https://bioregistry.io/chebi:64357)                     | ![](https://bioregistry.io/chebi:64357?provider=chebi-img)  |
| Non-Randomized (Phase 2)   | [NCT00176787](https://bioregistry.io/clinicaltrials:NCT00176787) | Radiation Therapy With Capecitabine in Rectal Cancer                            | [Rectal Neoplasms](https://bioregistry.io/mesh:D012004)          | [capecitabine](https://bioregistry.io/chebi:31348)                  | ![](https://bioregistry.io/chebi:31348?provider=chebi-img)  |
| Non-Randomized (Phase 2/3) | [NCT04431453](https://bioregistry.io/clinicaltrials:NCT04431453) | Study of Remdesivir in Participants Below 18 Years Old With COVID-19            | [COVID-19](https://bioregistry.io/mesh:D000086382)               | [remdesivir](https://bioregistry.io/chebi:145994)                   | ![](https://bioregistry.io/chebi:145994?provider=chebi-img) |
| Non-Randomized (Phase 3)   | [NCT03184987](https://bioregistry.io/clinicaltrials:NCT03184987) | A Long-term Safety Study of Fixed Dose Combination Therapy Fluticasone [...]    | [Asthma](https://bioregistry.io/mesh:D001249)                    | [albuterol](https://bioregistry.io/chebi:2549)                      | ![](https://bioregistry.io/chebi:2549?provider=chebi-img)   |
| Non-Randomized (Phase 4)   | [NCT03282487](https://bioregistry.io/clinicaltrials:NCT03282487) | Optimising Steroid Replacement in Patients With Adrenal Insufficiency           | [Adrenal Insufficiency](https://bioregistry.io/mesh:D000309)     | [cortisol](https://bioregistry.io/chebi:17650)                      | ![](https://bioregistry.io/chebi:17650?provider=chebi-img)  |
| Randomized (Phase 0)       | [NCT04293887](https://bioregistry.io/clinicaltrials:NCT04293887) | Efficacy and Safety of IFN-α2β in the Treatment of Novel Coronavirus Patients   | [Coronavirus Infections](https://bioregistry.io/mesh:D018352)    | [interferon](https://bioregistry.io/chebi:52999)                    | ![](https://bioregistry.io/chebi:52999?provider=chebi-img)  |
| Randomized (Phase 1)       | [NCT01166087](https://bioregistry.io/clinicaltrials:NCT01166087) | Bioequivalence Study of Fluoxetine Hydrochloride Delayed-Release Capsules [...] | [Malnutrition](https://bioregistry.io/mesh:D044342)              | [fluoxetine](https://bioregistry.io/chebi:5118)                     | ![](https://bioregistry.io/chebi:5118?provider=chebi-img)   |
| Randomized (Phase 1/2)     | [NCT00106587](https://bioregistry.io/clinicaltrials:NCT00106587) | Treatment of In-Stent Restenosis by Paclitaxel Coated PTCA Balloons [...]       | [Coronary Restenosis](https://bioregistry.io/mesh:D023903)       | [paclitaxel](https://bioregistry.io/chebi:45863)                    | ![](https://bioregistry.io/chebi:45863?provider=chebi-img)  |
| Randomized (Phase 2)       | [NCT00094887](https://bioregistry.io/clinicaltrials:NCT00094887) | Nitric Oxide Inhalation to Treat Sickle Cell Pain Crises                        | [Anemia, Sickle Cell](https://bioregistry.io/mesh:D000755)       | [nitric oxide](https://bioregistry.io/chebi:16480)                  | ![](https://bioregistry.io/chebi:16480?provider=chebi-img)  |
| Randomized (Phase 2/3)     | [NCT00136487](https://bioregistry.io/clinicaltrials:NCT00136487) | Celecoxib (Celebrex) Versus Placebo in Men With Recurrent Prostate Cancer       | [Prostatic Neoplasms](https://bioregistry.io/mesh:D011471)       | [celecoxib](https://bioregistry.io/chebi:41423)                     | ![](https://bioregistry.io/chebi:41423?provider=chebi-img)  |
| Randomized (Phase 3)       | [NCT00843687](https://bioregistry.io/clinicaltrials:NCT00843687) | A Comparison of the Pharmacokinetics and Safety of Long-acting Injectable [...] | [Schizophrenia](https://bioregistry.io/mesh:D012559)             | [risperidone](https://bioregistry.io/chebi:8871)                    | ![](https://bioregistry.io/chebi:8871?provider=chebi-img)   |
| Randomized (Phase 4)       | [NCT03586687](https://bioregistry.io/clinicaltrials:NCT03586687) | Osteoarthritis Shoulder Injection Study                                         | [Osteoarthritis](https://bioregistry.io/mesh:D010003)            | [triamcinolone](https://bioregistry.io/chebi:9667)                  | ![](https://bioregistry.io/chebi:9667?provider=chebi-img)   |

## Proposing an Ontology Meta-model

Given my goal to create an ontology export of ClinicalTrials.gov, I had to start
by making some modeling decisions. The first was that each clinical study in the
resource is an _instance_. This meant that I had to start by finding the right
_class_ for each, corresponding to the study types and allocations that I
explored above.

### Searching for Existing Ontology Classes

The [Ontology for Biomedical Investigations (OBI)](https://obi-ontology.org) is
a high quality ontology that contains terms for assays, devices, objectives, and
other aspects of biomedical investigations. Therefore, I would ideally be able
to find terms corresponding to the study types and allocations that I explored
above already inside it.

I used the
[Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols4/ontologies) to search
for classes corresponding to the study types I explored above, but didn't find
anything specific enough in OBI. However, I did note that _if_ there would be
classes for clinical studies, then they would appear under its high-level class
for [investigation (OBI:0000066)](https://bioregistry.io/obi:0000066)

While searching in the OLS, I did find the following relevant classes, each with
their own issues:

1. The [Semantic Science Integrated Ontology (SIO)](https://bioregistry.io/sio)
   has a term for clinical trial
   ([SIO:001000](https://www.ebi.ac.uk/ols4/ontologies/sio/classes/http%253A%252F%252Fsemanticscience.org%252Fresource%252FSIO_001000)),
   but SIO doesn't follow best practices from
   [Open Biological and Biomedical Ontology (OBO) Foundry](https://obofoundry.org),
   meaning that it is difficult to reuse and less trustworthy.
2. The
   [Ontology of Precision Medicine and Investigation (OPMI)](https://bioregistry.io/opmi)
   has a term for clinical trial
   ([OPMI:0004507](https://www.ebi.ac.uk/ols4/ontologies/opmi/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FOPMI_0004507?lang=en)).
   I'm not comfortable reusing terms from this ontology for two main reasons:
   1. It's use-case specific, and curated based on project-based needs, which
      means that it's not a reliable resource.
   2. It's not curated using modern ontology infrastructure, so I'm not sure
      that I can trust it will be maintained.
3. The [Informed Consent Ontology (ICO)](https://bioregistry.io/ico) also has a
   term for clinical trial
   ([ICO:0000065](https://www.ebi.ac.uk/ols4/ontologies/ico/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FICO_0000065?lang=en))
   but I have the same reservations as for OPMI. There's an overlap of the same
   authors with OPMI, so I have reservations to invest in reusing terms they
   haven't been able to deduplicate themselves.
4. [Eagle-I Resource Ontology (ERO)](https://obofoundry.org/ontology/ero) is an
   OBO Foundry ontology that has a term
   [clinical trial (ERO:0000016)](https://purl.obolibrary.org/obo/ERO_0000016)
   which nicely subclasses OBI's investigation class, but ERO has been abandoned
   and marked as deprecated in the OBO Foundry.
5. The [Ontology for MicroRNA Target (OMIT)](https://bioregistry.io/omit)
   haphazardly imported all of MeSH at some point and has a term
   [Clinical Trial (OMIT:0016936)](https://www.ebi.ac.uk/ols4/ontologies/omit/classes/http%253A%252F%252Fpurl.obolibrary.org%252Fobo%252FOMIT_0016936).
6. The [Clinical Trials Ontology (CTO)](https://bioregistry.io/registry/cto) is
   an OBO Foundry ontology that nominally has the correct scope and has a term
   [clinical trial (CTO:0000220)](https://purl.obolibrary.org/obo/CTO_0000220),
   but there are potential issues with its design choices, and it was produced
   by a group that has historically had difficulty maintaining its resources and
   actively participating in the OBO community. Despite these issues making it
   less suitable for reuse, the associated workshop proceeding
   [CTO: a Community-Based Clinical Trial Ontology and its Applications in PubChemRDF and SCAIView](https://bioregistry.io/pmc:PMC9389640)
   contains some interesting ideas.

Honorable mentions from non-ontology resources, which are a not ideal from a
modeling perspective to use as a parent class in an ontology:

1. [BioLink model](https://bioregistry.io/biolink) has a term
   [clinical trial (biolink:ClinicalTrial)](https://w3id.org/biolink/vocab/ClinicalTrial).
2. SNOMED has a term
   [Clinical trial (procedure) (SNOMED:110465008)](http://snomed.info/id/110465008),
   but is not an ontology and is notorious for being a closed resource,
   hampering reuse.
3. NCIT has a term for
   [Clinical Trial (NCIT:C71104)](https://bioregistry.io/NCIT:C71104), but it is
   not curated an ontology (despite OBO Foundry having an OWL conversion of it).
4. MeSH has a term
   [Clinical Trials as Topic (mesh:D002986)](https://bioregistry.io/mesh:D002986).

Despite all of what I could find, none of these terms were part of an ontology
that I can trust. Further, most of them conflated interventional clinical
studies, i.e., clinical trials, with all other clinical studies.

Therefore, the next step was to get in touch with OBI and ask them to mint an
authoritative term, that also can capture the nuance in clinical studies that is
lost in the other resources. I did that in their issue tracker
[obi-ontology/obi#1831](https://github.com/obi-ontology/obi/issues/1831). They
were very receptive, we had a nice conversation that brought up several points,
and they challenged me to go even further than just proposing the parent terms
and begin to develop a standardized model.

### A draft proposal

The following diagram represents a draft proposal that includes several terms
that OBI could mint as well as the kinds of relations between them. This is not
a perfect proposal - its goal is to be a discussion piece for an upcoming OBI
community call. There are still several parts missing and open questions.

<a href="https://docs.google.com/drawings/d/19BuWZ-C2iZkxDScxDy9WsAtLsItvkqT9bFtFaFkpbyA/edit?usp=sharing">
<img src="https://docs.google.com/drawings/d/e/2PACX-1vSCMXiTg3EjROweTq4RKOnqRyW-RMs7QOOiC3mhbSHa1eJtfK5ROWVRX7wh63f3m5AkAjQQ7u4VAsM-/pub?w=2628&amp;h=1629">
</a>

Here are some missing parts to this model that could be added incrementally:

1. A more detailed categorization of expanded access studies based on the
   [expanded access types](https://clinicaltrials.gov/study-basics/glossary#expanded-access-type)
   and
   [expanded access status](https://clinicaltrials.gov/study-basics/glossary#expanded-access-status)
2. A more detailed categorization of observational studies based on the 1)
   assembly of groups and cohorts and 2)
   [observational study models](https://clinicaltrials.gov/study-basics/glossary#observational-study-model)
   such as case-control, case-only, case-cross-over, ecologic or community
   studies, and family-based.
3. A model for eligibility criteria and enrollment
4. A model for outcomes, linked to OBI's assay terms
5. A model for investigators, funder types, and sponsors to support bibliometric
   investigation
6. A model for geolocation data associated with clinical study sites
7. A model for capturing adverse events and reasons for trial cancellation/end.
   In downstream applications, this could be used in tandem with the
   [FDA's Adverse Event Reporting System (FAERS)](https://www.fda.gov/drugs/surveillance/fdas-adverse-event-reporting-system-faers)
   and the
   [Vaccine Adverse Event Reporting System (VAERS)](https://vaers.hhs.gov/).

There is high potential for applying natural language processing methods to
extract more detailed information from the unstructured parts of clinical study
records. I've been focusing on ClincialTrials.gov as an example in this post,
but other clinical trial registries comprise almost exclusively unstructured
text.

## Proof-of-concept Ontology Export of ClinicalTrials.gov

[PyOBO](https://github.com/biopragmatics/pyobo) is Python software package that
implements an in-memory data structure for OBO/OWL ontologies as well as I/O
operations. On top of this, it implements workflows for converting databases
like HGNC, MeSH, and ChEMBL into OBO/OWL ontolgies. These workflows are careful
to make good design decisions, reusing classes and relations from other OBO
ontologies when possible. This is crucial for them to be readily integratable
with other resources.

The [`obo-db-ingest`](https://github.com/biopragmatics/obo-db-ingest) repository
is responsible for automatically downloading new versions of the resources
covered by PyOBO, converting them to OBO/OWL, archiving them to Zenodo, and
assigning persistent URLs (PURLs) so the files can be accessed in a sustainable
way. It's also careful to include licensing information such that anyone can
download these resources in a ready-to-use format, whereas the underlying
resources are often less easy to use directly.

As a proof-of-concept, I implemented a converter for ClinicalTrials.gov in PyOBO
at
[https://github.com/biopragmatics/pyobo/blob/main/src/pyobo/sources/clinicaltrials.py](https://github.com/biopragmatics/pyobo/blob/main/src/pyobo/sources/clinicaltrials.py).
The draft converter uses temporary classes to represent the study types and
allocations I'm proposing to OBI. It also mints some of its own relationships,
which would ideally be encoded in either OBI or the Relation Ontology (RO) for
maximum reusability.

The initial export contains more than 500K clinical studies; nearly one million
literature references, and near two million relationships between trials,
interventions, and conditions (there are still several places for expansion and
improvement discussed below). The ClinicalTrials.gov data is licensed under an
[equivalent to a public domain dedication](https://clinicaltrials.gov/about-site/terms-conditions#availability),
so there are few restrictions on remixing and redistributing the data this way.

A summary page can be found in the `obo-db-ingest` repository
[here](https://github.com/biopragmatics/obo-db-ingest/tree/main/export/clinicaltrials)
and the exported artifacts are listed here:

| Artifact       | Download PURL                                                                  |
| -------------- | ------------------------------------------------------------------------------ |
| OBO            | https://w3id.org/biopragmatics/resources/clinicaltrials/clinicaltrials.obo.gz  |
| OFN            | https://w3id.org/biopragmatics/resources/clinicaltrials/clinicaltrials.ofn.gz  |
| OWL            | https://w3id.org/biopragmatics/resources/clinicaltrials/clinicaltrials.owl.gz  |
| OBO Graph JSON | https://w3id.org/biopragmatics/resources/clinicaltrials/clinicaltrials.json.gz |
| Nodes          | https://w3id.org/biopragmatics/resources/clinicaltrials/clinicaltrials.tsv     |

Here's what some OBO instances for clinical studies look like for each clinical
study type:

```
[Instance]
id: clinicaltrials:NCT00000102
name: Congenital Adrenal Hyperplasia\: Calcium Channels as Therapeutic Targets
property_value: clinicaltrials:has_intervention mesh:D009543 ! has intervention Nifedipine
property_value: clinicaltrials:investigates_condition mesh:D000308 ! investigates condition Adrenocortical Hyperfunction
property_value: clinicaltrials:investigates_condition mesh:D000312 ! investigates condition Adrenal Hyperplasia, Congenital
property_value: clinicaltrials:investigates_condition mesh:D006965 ! investigates condition Hyperplasia
property_value: clinicaltrials:investigates_condition mesh:D047808 ! investigates condition Adrenogenital Syndrome
instance_of: interventional-clinical-trial

[Instance]
id: clinicaltrials:NCT00000104
name: Does Lead Burden Alter Neuropsychological Development?
property_value: clinicaltrials:investigates_condition mesh:D007855 ! investigates condition Lead Poisoning
property_value: clinicaltrials:investigates_condition mesh:D011041 ! investigates condition Poisoning
instance_of: observational-clinical-trial

[Instance]
id: clinicaltrials:NCT00000106
name: 41.8 Degree Centigrade Whole Body Hyperthermia for the Treatment of Rheumatoid Diseases
property_value: clinicaltrials:investigates_condition mesh:D003095 ! investigates condition Collagen Diseases
property_value: clinicaltrials:investigates_condition mesh:D012216 ! investigates condition Rheumatic Diseases
instance_of: randomized-interventional-clinical-trial

[Instance]
id: clinicaltrials:NCT00000250
name: Cold Water Immersion Modulates Reinforcing Effects of Nitrous Oxide - 2
property_value: clinicaltrials:has_intervention mesh:D009609 ! has intervention Nitrous Oxide
property_value: clinicaltrials:investigates_condition mesh:D009293 ! investigates condition Opioid-Related Disorders
property_value: clinicaltrials:investigates_condition mesh:D019966 ! investigates condition Substance-Related Disorders
instance_of: non-randomized-interventional-clinical-trial

[Instance]
id: clinicaltrials:NCT00040625
name: ALIMTA \(Pemetrexed\) Alone or in Combination With Cisplatin for Patients With Malignant Mesothelioma.
property_value: clinicaltrials:has_intervention mesh:D000068437 ! has intervention Pemetrexed
property_value: clinicaltrials:investigates_condition mesh:D000086002 ! investigates condition Mesothelioma, Malignant
property_value: clinicaltrials:investigates_condition mesh:D008654 ! investigates condition Mesothelioma
instance_of: expanded-access-study
```

## Reflections, and, what's missing?

I first became familiar with ClinicalTrials.gov and other clinical study
registries while working on the
[RAPTER project](https://globalbiodefense.com/2023/05/10/rapter-expediting-medical-countermeasure-response/),
funded by the America Defense Threat Reduction Agency (DTRA) with the goal to
integrate vaccine information and build computational tools to quicken the
development of vaccines in response to future pandemics.

One of the key issues to overcome was the accuracy of the data within these
resources. For example, ClinicalTrials.gov contains both a free-text and
processed field for its conditions and interventions. In many cases,
re-processing was required to ensure complete and accurate information. In my
draft export of ClincalTrials.gov, I exclusively used the processed data fields,
but a more careful conversion would require additional data science techniques.

Similarly, for data from the World Health Organization and other clinical trial
registries, full NER and relation extraction is required to identify
interventions, conditions, and outcomes.

Even when processed data is available, it's using MeSH identifiers, which are
not readily integrable with other resources. That's why ontologies often curate
MeSH cross-references themselves. I created the
[Biomappings](https://github.com/biopragmatics/biomappings) project as a way to
quickly predict and curate MeSH mappings to other chemical and disease
vocabularies, such as
[Chemical Entities of Biological Interest (ChEBI)](https://bioregistry.io/chebi)
and the [Disease Ontology (DOID)](https://bioregistry.io/doid). I also built
[SeMRA](https://github.com/biopragmatics/semra), a workflow for assembling and
inferring mappings to best reuse existing mappings available from a wide variety
of sources. These two approaches are crucial for making clinical study and trial
information actionable in a data integration scenario.

There's a lot of work to do in this space, but this is a nice first step. For
me, exporting lots of resources in a standard ontology format makes it easy to
load up a complete set of nodes when building knowledge graphs. As a coda, I
will say a little bit about what I like to do with this kind of data once I have
got it structured and integrated with other sources.

## What's this all useful for, anyway?

TODO:

1. summarize knowledge graph integration, path queries, data integration

### Chemical Phase Assessment

```mermaid
   graph LR
     drug -- intervention in --> trial[Clinical Study] -- has phase --> phase
     drug -. has maximum phase (aggregated) .-> phase
```

You can find out what's the maximum phase each intervention has appeared in.
This is interesting because it's often the case that multiple trials use the
same interventions. This is especially true in drug repositioning, where a drug
might be useful for a similar disease. More generally, drugs of the same
chemical class might also be useful for the same disease

Think of the priviliged substructures:

- the beta hydroxy lactone appearing in statins that enables their HMG-CoA
  reductase inhibitor activity
- sulfonamides for antibacterial properties due to their competitive inhibition
  of dihydropteroate synthase

However, a clinical trial database isn't enough to help us understand this.

### Global Chemical Space Assessment

```mermaid
   graph LR
     scaffold -- substructure of --> drug -- intervention in --> trial[Clinical Study] -- has phase --> phase
     scaffold -. has maximum phase (aggregated) .-> phase
```

Checking what chemical space has been used. Substructure relations can be
imported from ChEBI

### Disease-specific Chemical Space Assessment

```mermaid
   graph LR
     scaffold -- substructure of --> drug -- intervention in --> trial[Clinical Study] -- has phase --> phase
     trial -- studies --> disease
     scaffold -. has maximum phase (aggregated) .-> phase
```

The graph diagram isn't great to show aggregation/filtering operations paired
with graph queries, but you can also aggregate by the disease, so you can get
information like "how far has each scaffold got in each/my disease area?"

### Disease Class

This gets even more wild if you do a second aggregation over disease class,
letting you aggregate to answer questions lie "how far has each scaffold got in
each high-level disease class?". Of course, the secret is in having a subclass
structure that reflects something meaningful, and having a good way of deciding
where to prune that hierarchy. Maybe, the question is something like aggregating
for all rare diseases, cancers, neurodegenerative dieases, etc.

```mermaid
   graph LR
     scaffold -- substructure of --> drug -- intervention in --> trial[Clinical Study] -- studies --> disease -- subclass of --> diseaseclass[disease class]
     trial -- has maximum phase --> phase
     scaffold -. has maximum phase .-> phase
```

### Vaccine Summaries

```mermaid
   graph LR
     vaccineplatform[vaccine platform] -- platform for --> vaccine -- intervention in --> trial[Clinical Study] -- studies --> disease -- subclass of --> diseaseclass[disease class]
     trial -- has phase --> phase
     vaccineplatform -. has maximum phase .-> phase
```

1. in RAPTER, it was used to get a quick overview of which vaccine platforms had
   progressed to what degree in clinical trials

Specifically, this can help summarize vaccine platforms like RNA vaccines, DNA
vaccines, viral vector vaccines, etc. and their ability to treat subclasses of
coronavirus diseases, ebola, and malaria.

### Target Identification

```mermaid
graph LR
  disease -- studied in --> trial[Clinical Study]
  trial -- uses intervention --> drug
  drug -- regulates --> protein
  disease -. has putative target .-> protein
```

Target identification typically covers identifying important proteins in a given
disease context whose modulation can result in a therapeutic effect.

When combining clinical trial information with chemical activity databases like
ChEMBL, it's possible to generate hypotheses of important proteins in a disease
area.

Databases like OpenTargets have several orthogonal resources for triaging target
candidates.

Knowledge driven approaches like DisGeNet use text mining approaches as a
stand-in. When applied tt scale, automated approaches are also useful (re,
INDRA)

Knockdown, knockout, or overexpression studies are typicall run to confirm
target hypotheses.

### Mechanism of Action Deconvolution

```mermaid
graph LR
  drug -- intervention in --> trial[Clinical Study]
  trial -- studies --> disease
  disease -- has target --> protein
  drug -. has putative mechanism of action .-> protein
```

The dual problem to target identification is mechanism of action deconvolution.
This is a scenario where you know a drug works against a disease, but not why.
It turns out that having a mechanistic hypothesis is not required for FDA
approval!

Clinical trial inforamtion, combine with existing disease-target databases like
DisGeNet can give a simple path-based method for hypothesis generation.

More sophistocated methods that take into account chemical similarity and
protein similarity also exist.

MoA hypotheses can be much more easily tested in biochemical assays.

Why do we need this? Phenotypic drug discovery hype comes in cycles, and this is
a nice way to bridge the gap to target-based drug discovery. It's particularly
effective when there exist good cellular or animal models for the disease.

## Further Reading

- [https://github.com/obi-ontology/obi/issues/1831]
- [https://clinicaltrials.gov/about-site/about-ctg]
- [https://clinicaltrials.gov/study-basics/learn-about-studies]
- [https://clinicaltrials.gov/study-basics/glossary]
