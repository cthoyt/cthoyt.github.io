---
layout: post
title:
  Mapping between Open Educational Resource Data Models and Related Ontologies
date: 2025-11-07 10:14:00 +0200
author: Charles Tapley Hoyt
tags:
  - open educational resources
  - learning materials
  - OERs
  - SSSOM
  - SSSOM Curator
  - Biomappings
---

Interest in (open) educational resources (OERs) in the last twenty years has
lead to a highly fragmented landscape of modeling efforts. This post is about
establishing mappings and crosswalks between these disparate efforts using the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
and [SSSOM Curator](https://github.com/cthoyt/sssom-curator).

More concretely, most modeling efforts for (open) educational resources and
learning materials involves developing a metadata model that captures key
information such as the title, description, authors, language, disciple, and
keywords as well as pedagogical metadata like the target audience, required
proficiency level, and learning objectives. Notably, the Dublin Core Metadata
Initiative's
[Learning Resource Metadata Innovation (LMRI)](https://www.dublincore.org/specifications/lrmi)
and
[Educational Resource Discovery Index (ERuDIte)](https://www.pagestudy.org/erudite-training-resource-standard/)
each produced their own OER metadata models, then later consolidated efforts
with a third OER metadata model in Schema.org. The World Wide Web Consortium
(W3C) established the
[Open Educational Resources Schema Community Group](https://www.w3.org/community/oerschema/)
which developed [OERSchema](https://github.com/open-curriculum/oerschema), but
this metadata model did not see critical adoption, the working group shut down
in 2023, and the repository is effectively inactive. There's also numerous
partially overlapping isolated efforts (surprisingly, many in Germany) with
heterogeneous reusability (e.g., many are published by not downloadable, many
are poorly constructed).

Here's a non-exhaustive list of metadata models that follow semantic web
standards (see bioregistry record https://semantic.farm/collection/0000018):

| Prefix                                         | Name                                                    | Homepage                                                             |
| ---------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------- |
| [`educor`](https://semantic.farm/educor)       | Educational and Career-Oriented Recommendation Ontology | https://github.com/tibonto/educor                                    |
| [`lrmi`](https://semantic.farm/lrmi)           | DCMI Learning Resource Metadata Innovation Terms        | https://www.dublincore.org/specifications/lrmi/lrmi_terms/2022-06-14 |
| [`modalia`](https://semantic.farm/modalia)     | MoDALIA Ontology                                        | https://git.rwth-aachen.de/dalia/dalia-ontology                      |
| [`oerschema`](https://semantic.farm/oerschema) | OER Schema                                              | https://github.com/open-curriculum/oerschema                         |
| [`schema`](https://semantic.farm/schema)       | Schema.org                                              | https://schema.org                                                   |
| [`vivo`](https://semantic.farm/vivo)           | VIVO Ontology                                           | https://github.com/vivo-ontologies/vivo-ontology                     |

## TL;DR

This post is about creating a semantic mapping repository using SSSOM Curator,
filling it with predicted mappings between ontologies, data models, and other
semantic spaces relevant for open educational resources (OERs), then opening the
curation interface.

```console
$ uv tool install sssom-curator[predict-lexical,exports,web]
$ sssom-curator init
$ sssom-curator predict lexical --all-by-all --force kim.hcrt schema vivo
$ sssom-curator web
```

1. Surveying the semantic landscape
2. Ingesting resources
3. using lexical prediction workflow
4. curation
5. future: assess the amount of uncurated stuff (i.e., islands in the mapping
   graph)

## Survey Semantic Landscape

## Education Levels

| Prefix                                                           | Name                                                             | Homepage                                                                                                                      |
| ---------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| [`ans.educationlevel`](https://semantic.farm/ans.educationlevel) | U.S. Education Level Vocabulary                                  | http://purl.org/ASN/scheme/ASNEducationLevel/                                                                                 |
| [`isced1997`](https://semantic.farm/isced1997)                   | International Standard Classification of Education, 1997 Edition | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=International_Standard_Classification_of_Education_(ISCED) |
| [`isced2011`](https://semantic.farm/isced2011)                   | International Standard Classification of Education, 2011 Edition | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=International_Standard_Classification_of_Education_(ISCED) |
| [`isced2013`](https://semantic.farm/isced2013)                   | International Standard Classification of Education, 2013 Edition | https://ec.europa.eu/eurostat/statistics-explained/index.php?title=International_Standard_Classification_of_Education_(ISCED) |
| [`kim.educationlevel`](https://semantic.farm/kim.educationlevel) | KIM Education Level                                              | https://github.com/dini-ag-kim/educationalLevel                                                                               |
| [`kim.esv`](https://semantic.farm/kim.esv)                       | Educational Sectors Vocabulary                                   | https://github.com/dini-ag-kim/vocabs-edu                                                                                     |
| [`kim.hcrt`](https://semantic.farm/kim.hcrt)                     | Higher Education Resource Types                                  | https://github.com/dini-ag-kim/hcrt                                                                                           |
| [`oeh.educationlevel`](https://semantic.farm/oeh.educationlevel) | OpenEduHub Education Level                                       | https://github.com/openeduhub/oeh-metadata-vocabs                                                                             |

## Subjects and Disciplines

| Prefix                                                                                   | Name                                             | Homepage                                                  |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------ | --------------------------------------------------------- |
| [`ccso`](https://semantic.farm/ccso)                                                     | Curriculum Course Syllabus Ontology              | https://github.com/Vkreations/CCSO                        |
| [`kim.schulfaecher`](https://semantic.farm/kim.schulfaecher)                             | KIM School Subjects                              | https://github.com/dini-ag-kim/schulfaecher               |
| [`kim.hochschulfaechersystematik`](https://semantic.farm/kim.hochschulfaechersystematik) | German University Subject Classification System  | https://github.com/dini-ag-kim/hochschulfaechersystematik |
| [`adcad`](https://semantic.farm/adcad)                                                   | Arctic Data Center Academic Disciplines Ontology | https://github.com/NCEAS/adc-disciplines                  |
| [`edam`](https://semantic.farm/edam)                                                     | EDAM Ontology                                    | https://github.com/edamontology/edamontology              |
