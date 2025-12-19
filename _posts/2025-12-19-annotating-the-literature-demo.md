---
layout: post
title: Annotating the Literature with Named Entity Recognition
date: 2025-12-19 10:01:00 +0100
author: Charles Tapley Hoyt
tags:
  - named entity recognition
  - text mining
  - natural language processing
  - named entity normalization
  - medical subject headings
  - MeSH
  - PubMed
  - PyOBO
  - SSSLM
---

Annotating the literature with mentions of key concepts from a given domain is
often the first step towards extracting more substantial structured knowledge.
This can be challenging, as it typically encompasses acquiring and processing
the relevant literature and ontologies then installing and applying
difficult-to-use named entity recognition (NER) workflows. This post highlights
software components I've implemented to simplify this workflow. I demonstrate it
by annotating the biomedical literature available through
[PubMed](https://pubmed.ncbi.nlm.nih.gov/) with
[Medical Subject Headings (MeSH)](https://semantic.farm/mesh) terms, and also
comment on how this can be generalized to other natural sciences, engineering,
and humanities disciplines.

I've been building software for the last ten years that simplifies and
democratizes access to these resources. Here, I'm going to highlight three
components:

1. [**PubMed Downloader**](https://pubmed.ncbi.nlm.nih.gov/) provides a wrapper
   around PubMed's API and around bulk download and processing of the source
   data. While this resource only contains biomedical text, its place in the
   workflow can be replaced with any other text source.
2. [**SSSLM**](https://github.com/cthoyt/ssslm) provides a wrapper around NER
   methods such as [Gilda](https://github.com/gyorilab/gilda) and
   [spaCy](https://github.com/explosion/spaCy). SSSLM uses a pared-down version
   of Gilda as its default NER tool because Gilda is fast, interpretable, and
   easy to install (after removing some parts). SSSLM and the methods it wraps
   are fully domain-agnostic.
3. [**PyOBO**](https://github.com/biopragmatics/pyobo) provides a wrapper around
   fetching and processing ontologies, controlled vocabularies, databases, and
   other resources that can be used as a dictionary. It also has a high-level
   workflow,
   [`pyobo.get_grounder()`](https://pyobo.readthedocs.io/en/latest/api/pyobo.get_grounder.html)
   for getting content into `ssslm`. It's built on the
   [Semantic Farm](https://semantic.farm) (previously called the Bioregistry) to
   enable it to find and access ontologies across disciplines.

## Demonstration

The following is a demonstration on how to get the abstracts of 5 articles from
PubMed, perform named entity recognition (NER) using Medical Subject Headings
(MeSH), output the results (below). Note that the following code can be run as a
script using `uv run`, as it makes explicit its dependencies as
[PEP-723](https://peps.python.org/pep-0723/) inline metadata .

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click>=8.3.1",
#     "pubmed-downloader>=0.0.12",
#     "pyobo[gilda-slim]>=0.12.13",
#     "tabulate>=0.9.0",
# ]
# ///

import click
import pubmed_downloader
import pyobo
from tabulate import tabulate

# get a grounder loaded up with a specific version of MeSH.
# if you don't specify a version, the latest will be used.
grounder: ssslm.Grounder = pyobo.get_grounder("mesh", versions="2018")

# get 5 PubMed identifiers about diabetes. note that the
# PubMed API has been horrifically slow lately, so please be patient
pubmed_ids: list[str] = pubmed_downloader.search("diabetes", backend="api", retmax=5)
click.echo(f"got {len(pubmed_ids)} pubmed IDs")

for article in pubmed_downloader.get_articles(pubmed_ids, error_strategy="skip", progress=True):
    abstract: str = article.get_abstract()

    # get a list of annotations, which contain the offsets of the entity
    # and the grounding to a Bioregistry-standardized CURIE.
    # more generally, this can be applied to any string from any source
    annotations: list["ssslm.Annotation"] = grounder.annotate(abstract)

    rows = [
        (
            annotation.start,
            annotation.end,
            f"[{annotation.curie}](https://semantic.farm/{annotation.curie})",
            annotation.name,
            round(annotation.score, 3),
        )
        for annotation in annotations
    ]
    headers = ["Start", "End", "CURIE", "Name", "Score"]
    table = tabulate(rows, headers=headers, tablefmt="github")

    click.echo(
        f"**{article.title.rstrip().rstrip('.')}** "
        f"([pubmed:{article.pubmed}](https://semantic.farm/pubmed:{article.pubmed}))"
        f"\n\n> {abstract}\n\n{table}\n\n"
    )
```

## Parting Thoughts

Normally I post parting thoughts at the bottom of each post, but since the
results take up a lot of space, I'll put them here.

There are many directions to take these tools. The first might be to use a
subset of MeSH that's most appropriate for the annotation task. For example, if
we just wanted to see diseases, then it only makes sense to use the MeSH Disease
branch. Similarly, there are many other ontologies, controlled vocabularies, and
databases in the diseases space such as MONDO, DOID, SNOMED-CT, and many more.
These can be incorporated into the grounder with
`pyobo.get_grounder(["mesh", "mondo", "doid", "snomedct])`, but will lead to
redundancy issues. I've previously published
[SeMRA](https://github.com/biopragmatics/semra) where I addressed mapping
between equivalent entities, but am currently working on using these results to
assemble coherent and comprehensive lexica that can be easily reused by SSSLM in
the [Biolexica project](https://github.com/biopragmatics/biolexica) (which will
also get renamed to be domain-agnostic).

Other domains can be directly used. For example, in the energy domain, the
[Open Energy Ontology](https://semantic.farm/oeo) can be used with
`pyobo.get_grounder("oeo")`. In general, the
[Semantic Farm](https://semantic.farm) can be used to find ontologies from other
domains. Within the [NFDI](https://www.nfdi.de/?lang=en), there are
[collections](https://semantic.farm/collection/) for each NFDI consortia that
contain lists of relevant ontologies, controlled vocabularies, databases, and
other resources that mint identifiers.

I hope this was a helpful introduction! If you've got questions about these
workflows or want to see a demo on your favorite literature source/ontology/NER
method, post an issue to the relevant package's issue tracker.

## Results

**Investigation of intake pattern of SGLT2 inhibitors among shift workers with
diabetes: a crossover study**
([pubmed:41413602](https://semantic.farm/pubmed:41413602))

> Shift workers experience regular changes in their waking hours due to
> fluctuating work schedules. The timing of their medication intake differs
> depending on whether they are working a day or night shift. Sodium-glucose
> co-transporter 2 ( SGLT2) inhibitors are prescribed once a day and are often
> taken before or after breakfast. However, studies on the optimal dosing times
> for the effective treatment of shift workers are lacking. In this study, we
> investigated whether the effects were different by the pattern of SGLT2
> inhibitor intake for shift workers with diabetes. Seven shift workers with
> diabetes who were taking an SGLT2 inhibitor were analyzed. All participants
> took the medication upon waking for 14 days, followed by administration at a
> fixed time for another 14 days. Glucose levels were measured over 14 days when
> the drug was administered either upon waking or at a fixed time of day. The
> time in range (TIR), which indicates the percentage of time during which the
> glucose level is within the range of 70-180 mg/dL, was used as the main
> evaluation index. The mean HbA1c of the participants was 7.1%. The TIR was
> 88.5% in the administration upon waking group and 84.9% in the administration
> at a fixed time group. No significant difference in TIR values was observed
> between the two administration groups. A TIR of 70% or higher is recommended
> to prevent the onset of diabetic complications. Consistent intake of SGLT2
> inhibitors, regardless of whether it is during the day or night shift, may
> help stabilize blood glucose levels in shift workers throughout the day and
> night, thereby preventing the development of complications.

| Start | End  | CURIE                                                    | Name                                    | Score |
| ----- | ---- | -------------------------------------------------------- | --------------------------------------- | ----- |
| 6     | 13   | [mesh:D009274](https://semantic.farm/mesh:D009274)       | Occupational Groups                     | 0.54  |
| 82    | 96   | [mesh:D010561](https://semantic.farm/mesh:D010561)       | Personnel Staffing and Scheduling       | 0.54  |
| 219   | 233  | [mesh:D027981](https://semantic.farm/mesh:D027981)       | Symporters                              | 0.54  |
| 317   | 326  | [mesh:D062408](https://semantic.farm/mesh:D062408)       | Breakfast                               | 0.762 |
| 410   | 417  | [mesh:D009274](https://semantic.farm/mesh:D009274)       | Occupational Groups                     | 0.54  |
| 515   | 530  | [mesh:D000077203](https://semantic.farm/mesh:D000077203) | Sodium-Glucose Transporter 2 Inhibitors | 0.549 |
| 548   | 555  | [mesh:D009274](https://semantic.farm/mesh:D009274)       | Occupational Groups                     | 0.54  |
| 583   | 590  | [mesh:D009274](https://semantic.farm/mesh:D009274)       | Occupational Groups                     | 0.54  |
| 624   | 639  | [mesh:D000077203](https://semantic.farm/mesh:D000077203) | Sodium-Glucose Transporter 2 Inhibitors | 0.549 |
| 729   | 743  | [mesh:D009934](https://semantic.farm/mesh:D009934)       | Organization and Administration         | 0.54  |
| 781   | 788  | [mesh:D005947](https://semantic.farm/mesh:D005947)       | Glucose                                 | 0.778 |
| 832   | 836  | [mesh:D004364](https://semantic.farm/mesh:D004364)       | Pharmaceutical Preparations             | 0.54  |
| 981   | 988  | [mesh:D005947](https://semantic.farm/mesh:D005947)       | Glucose                                 | 0.762 |
| 1064  | 1069 | [mesh:D020481](https://semantic.farm/mesh:D020481)       | Index                                   | 0.762 |
| 1141  | 1155 | [mesh:D009934](https://semantic.farm/mesh:D009934)       | Organization and Administration         | 0.54  |
| 1191  | 1205 | [mesh:D009934](https://semantic.farm/mesh:D009934)       | Organization and Administration         | 0.54  |
| 1298  | 1312 | [mesh:D009934](https://semantic.farm/mesh:D009934)       | Organization and Administration         | 0.54  |
| 1383  | 1405 | [mesh:D048909](https://semantic.farm/mesh:D048909)       | Diabetes Complications                  | 0.54  |
| 1428  | 1444 | [mesh:D000077203](https://semantic.farm/mesh:D000077203) | Sodium-Glucose Transporter 2 Inhibitors | 0.549 |
| 1524  | 1537 | [mesh:D001786](https://semantic.farm/mesh:D001786)       | Blood Glucose                           | 0.762 |
| 1554  | 1561 | [mesh:D009274](https://semantic.farm/mesh:D009274)       | Occupational Groups                     | 0.54  |

**Men's health needs assessment in the Toledo District of Southern Belize**
([pubmed:41413521](https://semantic.farm/pubmed:41413521))

> Belize is a small country in Central America with a growing burden of
> non-communicable disease (NCD), including hypertension and diabetes. Toledo
> District is the southernmost and poorest district in the country. Reliable
> national level health data for Belize is readily available, but the data is
> rarely disaggregated by sex or district. Reducing the burden of NCDs is a high
> priority for the Ministry of Health and Wellness. Belize's progress to date on
> Sustainable Development Goal (SDG) 3 (Good Health and Wellbeing) has been
> modest with many indicators stagnating or progress increasing at less than 50%
> of the required rate. SDG 3 describes the need to reduce the risks of NCDs and
> to strengthen the capacities of the healthcare workforce. The objective was to
> perform a men's health needs assessment to identify and prioritize men's
> health needs in the Toledo District. This was a mixed methods study.
> Qualitative data were collected from semi-structured interviews. Interviews
> were recorded, transcribed, and analyzed using Thematic Analysis. Quantitative
> data included epidemiological data from national vital statistics or disease
> registries and other public sources. Data were collected between January and
> June 2017. Belizean men have among the highest risk for cardiac or diabetes
> related illness or death in the Americas. Diabetes and hypertension are
> responsible for 4.49% and 1.23% of Disability Adjusted Life Years in men
> respectively and are increasing by 2.51% annually. Fifty-seven interviews (55
> individuals and two groups) from nine villages were carried out. Four themes
> emerged from the qualitative data. Men in Toledo: • have poor health literacy;
> • have reasonable access to health resources, but do not use them; • inability
> to clearly articulate health priorities; • do not process risk well. Men in
> Toledo suffer from a high prevalence of NCDs including hypertension and
> diabetes and understand health and risks poorly. This may contribute to
> Belize's struggle to achieve the goals of SDG 3.4.1. Strengthening the
> healthcare workforce by improved training of community health workers (CHWs)
> and providing health education to men in Toledo is required to address these
> concerns.

| Start | End  | CURIE                                                    | Name                             | Score |
| ----- | ---- | -------------------------------------------------------- | -------------------------------- | ----- |
| 0     | 6    | [mesh:D001531](https://semantic.farm/mesh:D001531)       | Belize                           | 0.778 |
| 29    | 44   | [mesh:D002489](https://semantic.farm/mesh:D002489)       | Central America                  | 0.778 |
| 70    | 94   | [mesh:D000073296](https://semantic.farm/mesh:D000073296) | Noncommunicable Diseases         | 0.549 |
| 112   | 124  | [mesh:D006973](https://semantic.farm/mesh:D006973)       | Hypertension                     | 0.762 |
| 236   | 242  | [mesh:D006262](https://semantic.farm/mesh:D006262)       | Health                           | 0.762 |
| 252   | 258  | [mesh:D001531](https://semantic.farm/mesh:D001531)       | Belize                           | 0.778 |
| 321   | 324  | [mesh:D012723](https://semantic.farm/mesh:D012723)       | Sex                              | 0.762 |
| 405   | 411  | [mesh:D006262](https://semantic.farm/mesh:D006262)       | Health                           | 0.778 |
| 426   | 432  | [mesh:D001531](https://semantic.farm/mesh:D001531)       | Belize                           | 0.778 |
| 455   | 483  | [mesh:D000076502](https://semantic.farm/mesh:D000076502) | Sustainable Development          | 0.556 |
| 498   | 504  | [mesh:D006262](https://semantic.farm/mesh:D006262)       | Health                           | 0.778 |
| 546   | 556  | [mesh:D007202](https://semantic.farm/mesh:D007202)       | Indicators and Reagents          | 0.54  |
| 669   | 674  | [mesh:D012306](https://semantic.farm/mesh:D012306)       | Risk                             | 0.762 |
| 723   | 733  | [mesh:D003695](https://semantic.farm/mesh:D003695)       | Delivery of Health Care          | 0.54  |
| 734   | 743  | [mesh:D000078329](https://semantic.farm/mesh:D000078329) | Workforce                        | 0.762 |
| 776   | 788  | [mesh:D054526](https://semantic.farm/mesh:D054526)       | Men's Health                     | 0.725 |
| 789   | 805  | [mesh:D020380](https://semantic.farm/mesh:D020380)       | Needs Assessment                 | 0.762 |
| 833   | 845  | [mesh:D054526](https://semantic.farm/mesh:D054526)       | Men's Health                     | 0.725 |
| 846   | 851  | [mesh:D006301](https://semantic.farm/mesh:D006301)       | Health Services Needs and Demand | 0.54  |
| 893   | 900  | [mesh:D008722](https://semantic.farm/mesh:D008722)       | Methods                          | 0.762 |
| 1112  | 1128 | [mesh:D014798](https://semantic.farm/mesh:D014798)       | Vital Statistics                 | 0.762 |
| 1132  | 1139 | [mesh:D004194](https://semantic.farm/mesh:D004194)       | Disease                          | 0.762 |
| 1140  | 1150 | [mesh:D012042](https://semantic.farm/mesh:D012042)       | Registries                       | 0.762 |
| 1237  | 1240 | [mesh:D008571](https://semantic.farm/mesh:D008571)       | Men                              | 0.762 |
| 1264  | 1268 | [mesh:D012306](https://semantic.farm/mesh:D012306)       | Risk                             | 0.762 |
| 1312  | 1317 | [mesh:D003643](https://semantic.farm/mesh:D003643)       | Death                            | 0.762 |
| 1325  | 1333 | [mesh:D000569](https://semantic.farm/mesh:D000569)       | Americas                         | 0.778 |
| 1348  | 1360 | [mesh:D006973](https://semantic.farm/mesh:D006973)       | Hypertension                     | 0.762 |
| 1400  | 1430 | [mesh:D000087509](https://semantic.farm/mesh:D000087509) | Disability-Adjusted Life Years   | 0.556 |
| 1434  | 1437 | [mesh:D008571](https://semantic.farm/mesh:D008571)       | Men                              | 0.762 |
| 1628  | 1631 | [mesh:D008571](https://semantic.farm/mesh:D008571)       | Men                              | 0.778 |
| 1655  | 1670 | [mesh:D057220](https://semantic.farm/mesh:D057220)       | Health Literacy                  | 0.762 |
| 1700  | 1716 | [mesh:D006295](https://semantic.farm/mesh:D006295)       | Health Resources                 | 0.762 |
| 1773  | 1790 | [mesh:D006292](https://semantic.farm/mesh:D006292)       | Health Priorities                | 0.762 |
| 1809  | 1813 | [mesh:D012306](https://semantic.farm/mesh:D012306)       | Risk                             | 0.762 |
| 1820  | 1823 | [mesh:D008571](https://semantic.farm/mesh:D008571)       | Men                              | 0.778 |
| 1853  | 1863 | [mesh:D015995](https://semantic.farm/mesh:D015995)       | Prevalence                       | 0.762 |
| 1882  | 1894 | [mesh:D006973](https://semantic.farm/mesh:D006973)       | Hypertension                     | 0.762 |
| 1923  | 1929 | [mesh:D006262](https://semantic.farm/mesh:D006262)       | Health                           | 0.762 |
| 1934  | 1939 | [mesh:D012306](https://semantic.farm/mesh:D012306)       | Risk                             | 0.762 |
| 1971  | 1977 | [mesh:D001531](https://semantic.farm/mesh:D001531)       | Belize                           | 0.778 |
| 2004  | 2009 | [mesh:D006040](https://semantic.farm/mesh:D006040)       | Goals                            | 0.762 |
| 2042  | 2052 | [mesh:D003695](https://semantic.farm/mesh:D003695)       | Delivery of Health Care          | 0.54  |
| 2053  | 2062 | [mesh:D000078329](https://semantic.farm/mesh:D000078329) | Workforce                        | 0.762 |
| 2087  | 2111 | [mesh:D003150](https://semantic.farm/mesh:D003150)       | Community Health Workers         | 0.762 |
| 2133  | 2149 | [mesh:D006266](https://semantic.farm/mesh:D006266)       | Health Education                 | 0.762 |
| 2153  | 2156 | [mesh:D008571](https://semantic.farm/mesh:D008571)       | Men                              | 0.762 |
| 2182  | 2189 | [mesh:D019484](https://semantic.farm/mesh:D019484)       | Address                          | 0.762 |

**Risk factors of ventilator-associated pneumonia in patients with acute
exacerbation of chronic obstructive pulmonary disease: a meta-analysis and
systematic review** ([pubmed:41413500](https://semantic.farm/pubmed:41413500))

> This meta-analysis aimed to identify risk factors for ventilator-associated
> pneumonia (VAP) in patients with Acute exacerbations of Chronic obstructive
> pulmonary disease (AECOPD). We systematically searched PubMed, Web of Science,
> CINAHL, Cochrane Library, Embase, CNKI, and other databases for studies
> investigating risk factors for VAP in patients experiencing AECOPD. The search
> encompassed records from database inception up to July 2, 2025. The quality of
> the studies was assessed using the Newcastle-Ottawa Scale. Meta-analysis was
> performed using Stata 18.0. A total of 16 articles were included, encompassing
> 3,664 subjects and 16 risk factors. Meta-analysis results showed that, Age
> (OR: 2.49, 95%CI : 1.49, 4.17; P<0.001), Smoking history (OR: 2.70, 95%CI :
> 1.65, 4.44; P<0.001), Acute physiology and chronic health evaluation composite
> score (APACHE Ⅱ) score (OR: 3.03, 95%CI : 1.98, 4.65; P<0.001), Sequential
> organ failure assessment (SOFA) score (OR: 2.75, 95%CI : 1.90, 3.99; P<0.001),
> Diabetes (OR: 2.11, 95%CI : 1.38, 3.24; P = 0.001), Underlying Diseases (OR:
> 3.42, 95%CI : 1.85, 6.32; P<0.001), Duration of mechanical ventilation (OR:
> 4.53, 95%CI : 2.68, 7.65; P<0.001), Tracheal intubation (OR: 4.21, 95%CI :
> 1.85, 9.57; P = 0.001), Indwelling gastric tube ( OR: 3.31, 95%CI : 1.38,
> 7.95; P = 0.008), Total parenteral nutrition (OR: 1.86, 95%CI : 1.29, 2.70; P
> = 0.001), Combined antibiotics (OR: 2.79, 95%CI : 1.32, 5.93; P = 0.007),
> Tracheotomy (OR: 2.92, 95%CI : 2.04, 4.17; P<0.001), History of mechanical
> ventilation within one year (OR: 2.92, 95%CI : 2.04, 4.17; P = 0.005), Use
> acid suppressants (OR: 2.10, 95%CI : 1.49, 2.97; P<0.001) were associated with
> the development of VAP in AECOPD patients. This study identified 14 risk
> factors associated with the risk of VAP in AECOPD patients. This finding is
> helpful for early identification of high-risk patients, which is of great
> value for reducing mortality and improving the clinical prognosis of patients
> with mechanical ventilation.

| Start | End  | CURIE                                              | Name                                   | Score |
| ----- | ---- | -------------------------------------------------- | -------------------------------------- | ----- |
| 5     | 18   | [mesh:D017418](https://semantic.farm/mesh:D017418) | Meta-Analysis                          | 0.762 |
| 37    | 49   | [mesh:D012307](https://semantic.farm/mesh:D012307) | Risk Factors                           | 0.762 |
| 54    | 85   | [mesh:D053717](https://semantic.farm/mesh:D053717) | Pneumonia, Ventilator-Associated       | 0.54  |
| 132   | 169  | [mesh:D029424](https://semantic.farm/mesh:D029424) | Pulmonary Disease, Chronic Obstructive | 0.549 |
| 207   | 213  | [mesh:D039781](https://semantic.farm/mesh:D039781) | PubMed                                 | 0.778 |
| 222   | 229  | [mesh:D012586](https://semantic.farm/mesh:D012586) | Science                                | 0.778 |
| 248   | 255  | [mesh:D007990](https://semantic.farm/mesh:D007990) | Libraries                              | 0.556 |
| 317   | 329  | [mesh:D012307](https://semantic.farm/mesh:D012307) | Risk Factors                           | 0.762 |
| 394   | 401  | [mesh:D011996](https://semantic.farm/mesh:D011996) | Records                                | 0.762 |
| 407   | 415  | [mesh:D019991](https://semantic.farm/mesh:D019991) | Database                               | 0.762 |
| 520   | 533  | [mesh:D017418](https://semantic.farm/mesh:D017418) | Meta-Analysis                          | 0.772 |
| 639   | 651  | [mesh:D012307](https://semantic.farm/mesh:D012307) | Risk Factors                           | 0.762 |
| 653   | 666  | [mesh:D017418](https://semantic.farm/mesh:D017418) | Meta-Analysis                          | 0.772 |
| 735   | 742  | [mesh:D012907](https://semantic.farm/mesh:D012907) | Smoking                                | 0.778 |
| 743   | 750  | [mesh:D006664](https://semantic.farm/mesh:D006664) | History                                | 0.762 |
| 794   | 840  | [mesh:D018806](https://semantic.farm/mesh:D018806) | APACHE                                 | 0.549 |
| 858   | 866  | [mesh:D018806](https://semantic.farm/mesh:D018806) | APACHE                                 | 0.53  |
| 1072  | 1080 | [mesh:D004194](https://semantic.farm/mesh:D004194) | Disease                                | 0.778 |
| 1072  | 1080 | [obo:mesh#C](https://semantic.farm/obo:mesh#C)     | Diseases                               | 0.778 |
| 1136  | 1158 | [mesh:D012121](https://semantic.farm/mesh:D012121) | Respiration, Artificial                | 0.54  |
| 1211  | 1221 | [mesh:D007440](https://semantic.farm/mesh:D007440) | Intubation                             | 0.762 |
| 1332  | 1358 | [mesh:D010289](https://semantic.farm/mesh:D010289) | Parenteral Nutrition, Total            | 0.549 |
| 1411  | 1422 | [mesh:D000900](https://semantic.farm/mesh:D000900) | Anti-Bacterial Agents                  | 0.54  |
| 1466  | 1477 | [mesh:D014140](https://semantic.farm/mesh:D014140) | Tracheotomy                            | 0.778 |
| 1521  | 1528 | [mesh:D006664](https://semantic.farm/mesh:D006664) | History                                | 0.778 |
| 1532  | 1554 | [mesh:D012121](https://semantic.farm/mesh:D012121) | Respiration, Artificial                | 0.54  |
| 1767  | 1779 | [mesh:D012307](https://semantic.farm/mesh:D012307) | Risk Factors                           | 0.762 |
| 1800  | 1804 | [mesh:D012306](https://semantic.farm/mesh:D012306) | Risk                                   | 0.762 |
| 1941  | 1950 | [mesh:D009026](https://semantic.farm/mesh:D009026) | Mortality                              | 0.762 |
| 1978  | 1987 | [mesh:D011379](https://semantic.farm/mesh:D011379) | Prognosis                              | 0.762 |
| 2005  | 2027 | [mesh:D012121](https://semantic.farm/mesh:D012121) | Respiration, Artificial                | 0.54  |

**Randomized trial assessing transverse supraumbilical incisions for cesarean
sections in morbid obese women with pannus**
([pubmed:41413498](https://semantic.farm/pubmed:41413498))

> BACKGROUND AND OBJECTIVE: The high prevalence of Morbidly obese Egyptian
> patients presents surgical problems for cesarean sections (CS), including a
> higher risk of wound infections. This study examines the impact of a
> transverse supraumbilical (TSU) incision in these patients. We conducted a
> randomized controlled trial on 72 morbidly obese patients (BMI >40 kg/m²)
> scheduled for cesarean section at Ain Shams University Hospital from March
> 2016 to August 2018. Participants were divided into Group A (36 patients) with
> a transverse supraumbilical (TSU) incision and Group B (36 patients) with a
> conventional Pfannenstiel incision. The primary outcome measured was the
> incidence of wound infection, while secondary outcomes included operative
> time, postoperative pain, hospital stay, blood loss, postoperative mobility,
> and intestinal motility. The results indicated no significant differences
> between the groups regarding age, BMI, parity, diabetes mellitus, and history
> of previous cesarean sections. The incidence of surgical site infection was
> significantly lower in the transverse supraumbilical group (11.1%, 4/36)
> compared to the Pfannenstiel group (58.3%, 21/36), with an absolute risk
> reduction of 47.2% (95% CI: 27.8% to 66.6%). Other parameters like operative
> time, hematocrit drop, pain score, hospital stay, and intestinal motility
> showed no significant differences between the groups (P>0.05). Supraumbilical
> transverse incisions are a safe, effective alternative to Pfannenstiel
> incisions in morbidly obese women, with better wound infection rates and
> easier access. Further research is needed to confirm the benefits and to
> assess patient satisfaction. This study was registered prospectively in
> clinicaltrials.gov (NCT02692729) on 1.3.2016.

| Start | End  | CURIE                                              | Name                        | Score |
| ----- | ---- | -------------------------------------------------- | --------------------------- | ----- |
| 35    | 45   | [mesh:D015995](https://semantic.farm/mesh:D015995) | Prevalence                  | 0.762 |
| 113   | 130  | [mesh:D002585](https://semantic.farm/mesh:D002585) | Cesarean Section            | 0.762 |
| 156   | 160  | [mesh:D012306](https://semantic.farm/mesh:D012306) | Risk                        | 0.762 |
| 164   | 180  | [mesh:D014946](https://semantic.farm/mesh:D014946) | Wound Infection             | 0.762 |
| 293   | 320  | [mesh:D016449](https://semantic.farm/mesh:D016449) | Randomized Controlled Trial | 0.762 |
| 381   | 397  | [mesh:D002585](https://semantic.farm/mesh:D002585) | Cesarean Section            | 0.762 |
| 411   | 421  | [mesh:D014495](https://semantic.farm/mesh:D014495) | Universities                | 0.556 |
| 422   | 430  | [mesh:D006761](https://semantic.farm/mesh:D006761) | Hospitals                   | 0.556 |
| 670   | 679  | [mesh:D015994](https://semantic.farm/mesh:D015994) | Incidence                   | 0.762 |
| 683   | 698  | [mesh:D014946](https://semantic.farm/mesh:D014946) | Wound Infection             | 0.762 |
| 734   | 748  | [mesh:D061646](https://semantic.farm/mesh:D061646) | Operative Time              | 0.762 |
| 750   | 768  | [mesh:D010149](https://semantic.farm/mesh:D010149) | Pain, Postoperative         | 0.549 |
| 770   | 783  | [mesh:D007902](https://semantic.farm/mesh:D007902) | Length of Stay              | 0.54  |
| 785   | 810  | [mesh:D019106](https://semantic.farm/mesh:D019106) | Postoperative Hemorrhage    | 0.502 |
| 825   | 844  | [mesh:D005769](https://semantic.farm/mesh:D005769) | Gastrointestinal Motility   | 0.54  |
| 934   | 940  | [mesh:D010298](https://semantic.farm/mesh:D010298) | Parity                      | 0.762 |
| 942   | 959  | [mesh:D003920](https://semantic.farm/mesh:D003920) | Diabetes Mellitus           | 0.762 |
| 965   | 972  | [mesh:D006664](https://semantic.farm/mesh:D006664) | History                     | 0.762 |
| 985   | 1002 | [mesh:D002585](https://semantic.farm/mesh:D002585) | Cesarean Section            | 0.762 |
| 1008  | 1017 | [mesh:D015994](https://semantic.farm/mesh:D015994) | Incidence                   | 0.762 |
| 1021  | 1044 | [mesh:D013530](https://semantic.farm/mesh:D013530) | Surgical Wound Infection    | 0.54  |
| 1181  | 1204 | [mesh:D061366](https://semantic.farm/mesh:D061366) | Numbers Needed To Treat     | 0.54  |
| 1262  | 1276 | [mesh:D061646](https://semantic.farm/mesh:D061646) | Operative Time              | 0.762 |
| 1278  | 1288 | [mesh:D006400](https://semantic.farm/mesh:D006400) | Hematocrit                  | 0.762 |
| 1295  | 1299 | [mesh:D010146](https://semantic.farm/mesh:D010146) | Pain                        | 0.762 |
| 1307  | 1320 | [mesh:D007902](https://semantic.farm/mesh:D007902) | Length of Stay              | 0.54  |
| 1326  | 1345 | [mesh:D005769](https://semantic.farm/mesh:D005769) | Gastrointestinal Motility   | 0.54  |
| 1523  | 1528 | [mesh:D014930](https://semantic.farm/mesh:D014930) | Women                       | 0.762 |
| 1542  | 1557 | [mesh:D014946](https://semantic.farm/mesh:D014946) | Wound Infection             | 0.762 |
| 1591  | 1599 | [mesh:D012106](https://semantic.farm/mesh:D012106) | Research                    | 0.762 |
| 1648  | 1668 | [mesh:D017060](https://semantic.farm/mesh:D017060) | Patient Satisfaction        | 0.762 |

**Associations of Perfluoroalkyl and Polyfluoroalkyl Substances With
Cardiovascular Disease Incidence in Adults With Prediabetes: Findings From the
Diabetes Prevention Program**
([pubmed:41413398](https://semantic.farm/pubmed:41413398))

> Perfluoroalkyl and polyfluoroalkyl substances (PFAS) are persistent,
> widespread environmental contaminants linked to cardiometabolic outcomes
> including obesity, hyperlipidemia, and diabetes. We examined whether baseline
> plasma PFAS concentrations are associated with incident cardiovascular disease
> (CVD) in adults with prediabetes, leveraging data from DPPOS (Diabetes
> Prevention Program Outcomes Study). Among 1382 participants, we quantified
> baseline plasma concentrations of 6 PFAS. We used Cox proportional hazards
> models to estimate the risks of developing CVD outcomes during a median of 21
> years of follow-up for each PFAS and used quantile g-computation to evaluate
> the joint effect of all 6 PFAS. Effect modification by age, sex, menopausal
> status, diet, and physical activity was explored. The incidence of major
> adverse cardiovascular events was 9.6%; 3.9% had CVD-related death. Each
> increase in interquartile range (1.1 ng/mL) in 2-( In adults with prediabetes,
> higher plasma concentrations of select PFAS, but not their mixture, were
> prospectively associated with increased CVD risk. These findings underscore
> PFAS as a potential environmental risk factor for CVD in high-risk
> populations.

| Start | End  | CURIE                                              | Name                        | Score |
| ----- | ---- | -------------------------------------------------- | --------------------------- | ----- |
| 152   | 159  | [mesh:D009765](https://semantic.farm/mesh:D009765) | Obesity                     | 0.762 |
| 161   | 175  | [mesh:D006949](https://semantic.farm/mesh:D006949) | Hyperlipidemias             | 0.54  |
| 220   | 226  | [mesh:D010949](https://semantic.farm/mesh:D010949) | Plasma                      | 0.762 |
| 276   | 298  | [mesh:D002318](https://semantic.farm/mesh:D002318) | Cardiovascular Diseases     | 0.54  |
| 308   | 314  | [mesh:D000328](https://semantic.farm/mesh:D000328) | Adult                       | 0.762 |
| 320   | 331  | [mesh:D011236](https://semantic.farm/mesh:D011236) | Prediabetic State           | 0.54  |
| 381   | 388  | [mesh:D019542](https://semantic.farm/mesh:D019542) | Program                     | 0.778 |
| 454   | 460  | [mesh:D010949](https://semantic.farm/mesh:D010949) | Plasma                      | 0.762 |
| 495   | 526  | [mesh:D016016](https://semantic.farm/mesh:D016016) | Proportional Hazards Models | 0.549 |
| 543   | 548  | [mesh:D012306](https://semantic.farm/mesh:D012306) | Risk                        | 0.762 |
| 679   | 684  | [mesh:D007596](https://semantic.farm/mesh:D007596) | Joints                      | 0.54  |
| 735   | 738  | [mesh:D012723](https://semantic.farm/mesh:D012723) | Sex                         | 0.762 |
| 759   | 763  | [mesh:D004032](https://semantic.farm/mesh:D004032) | Diet                        | 0.762 |
| 769   | 786  | [mesh:D015444](https://semantic.farm/mesh:D015444) | Exercise                    | 0.54  |
| 805   | 814  | [mesh:D015994](https://semantic.farm/mesh:D015994) | Incidence                   | 0.762 |
| 885   | 890  | [mesh:D003643](https://semantic.farm/mesh:D003643) | Death                       | 0.762 |
| 951   | 957  | [mesh:D000328](https://semantic.farm/mesh:D000328) | Adult                       | 0.762 |
| 963   | 974  | [mesh:D011236](https://semantic.farm/mesh:D011236) | Prediabetic State           | 0.54  |
| 983   | 989  | [mesh:D010949](https://semantic.farm/mesh:D010949) | Plasma                      | 0.762 |
| 1093  | 1097 | [mesh:D012306](https://semantic.farm/mesh:D012306) | Risk                        | 0.762 |
| 1159  | 1170 | [mesh:D012307](https://semantic.farm/mesh:D012307) | Risk Factors                | 0.54  |
| 1192  | 1203 | [mesh:D011153](https://semantic.farm/mesh:D011153) | Population                  | 0.762 |
