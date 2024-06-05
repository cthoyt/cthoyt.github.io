---
layout: post
title: Easier ORCID
date: 2024-06-04 14:52:00 +0100
author: Charles Tapley Hoyt
tags:
  - ORCID
  - bibliometrics
---

Open Researcher and Contributor Identifier (ORCID) is an invaluable resource that supports the unambiguous
identification of researchers. However, its first party data dump is too complex, verbose, and unstandardized for many
use cases. This post describes open source software I
wrote ([`orcid_downloader`](https://github.com/cthoyt/orcid_downloader)) that automates downloading, processing, and
exporting ORCID into a more usable form, which I put on [Zenodo](https://zenodo.org/doi/10.5281/zenodo.10137939) under
the CC0 license.

Criticisms of ORCID

1. ORCID is in XML, which makes it highly verbose and hard to understand. There exists some kind of JSON converter, but
   it's in Java and I don't understand why ORCID doesn't also just make the export and put it on their FigShare along
   with the XML products
2. Main data product contains provenance information for all fields, which in theory is nice but not always necessary
3. The "summary" file is 32 gigabytes compressed with tar gz! this makes it effectively impossible to get into the data
   without processing it in full.

This Zenodo record

contains a derived version that is much more straightforwards, accessible, and smaller. So far, this includes employers,
education, external identifiers, and publications linked to PubMed. It adds additional processing to ground employers
and educational instutitions using the Research Organization Registry (ROR). It also does some minor string processing,
such as standardization of education types (e.g., Bachelor of Science, Master of Science) and standardization of PubMed
references.

The records.jsonl.gz file is a JSON Lines file where each row represents a single ORCID record in a simple, well-defined
schema (see schema.json). The records_hq.jsonl.gz file is a subset of the full records file that only contains records
that have at least one ROR-grounded employer, at least one ROR-grounded education, or at least one publication indexed
in PubMed. The point of this subset is to remove ORCID records that are generally not possible to match up to any
external information.

## External Identifiers

An ORCID record has two places that make cross-references to external
nomenclature authorities:

1. The "Websites & Social Links" section which allows a researcher to give a link with a name.
   This is a trove of links to LinkedIn, Google Scholar, GitHub, and other external identifiers.
   ORCID itself doesn't standardize them, but using a combination of the Bioregistry and custom parsing,
   many can be standardized.
2. The "Other IDs" section is generated based on applications that connect to ORCID and send structured links. This
   includes Scopus, Web of Science (formerly ResearcherID), Loop, and some others. This also needs quite a bit
   of standardization, probably due to a combination of bugs in ORCID, bugs in external services, legacy data, and other
   things.

### Reflections

I found several interesting things while parsing these sections:

1. I discovered several new nomenclature authorities that weren't already registered in
   the [Bioregistry](https://github.com/biopragmatics/bioregistry). This includes Loop, Digital Author ID (Dutch),
   Authenticus (Portuguese), Dialnet (Spanish), SciProfiles, Ciência (Portuguese), and KAKEN (Japanese). I still have to
   send [new prefix requests](https://www.youtube.com/watch?v=e-I6rcV2_BE) for these.
2. I found several fields that were totally junk or didn't make sense. For example, there is sometimes a reference to
   the ORCID record itself. There are also references to external IDs that aren't really IDs, or at least don't follow
   enough of the guidelines
   from [Identifiers in the 21<sup>st</sup> Century](https://doi.org/10.1371/journal.pbio.2001414)
   to be useful.
3. Both the "Websites & Social Links" and "Other IDs" needed standardization. In some places, this was as easy as
   using the Bioregistry prefix standardization, but in other places required more custom URL parsing. This is
   especially true for Google Scholar, which can appear with a number of domain names (e.g., https://scholar.google.com
   or https://scholar.google.es). The local unique identifier appears here inside the URL parameters, which can be in
   any order along with the language tag, so this needs URL parsing instead of more simple URI prefix handling *a la*
   the [`curies`](https://github.com/biopragmatics/curies) Python Package.

### Summary

Here's a breakdown of the top external cross-references, standardized with the Bioregistry (where possible). Note that
this was prioritized by the most common
cross-references, and is not complete. To capture _all_ would be a lot of work and require many more corner cases
to less common services. I also threw away links to non-professional social networks like Facebook/Instagram.
I also made the value judgement to throw away links to Twitter since it doesn't reflect open and inclusive scientific
community values anymore.

| Resource                                                  |     Count |
|-----------------------------------------------------------|----------:|
| [`scopus`](https://bioregistry.io/scopus)                 | 1,400,735 |
| [`wos.researcher`](https://bioregistry.io/wos.researcher) |   608,543 |
| `sciprofiles`                                             |   259,654 |
| `loop`                                                    |   229,224 |
| [`linkedin`](https://bioregistry.io/linkedin)             |   191,321 |
| `researchgate`                                            |   125,242 |
| [`google.scholar`](https://bioregistry.io/google.scholar) |    52,131 |
| [`github`](https://bioregistry.io/github)                 |    13,397 |
| [`gnd`](https://bioregistry.io/gnd)                       |     7,621 |
| [`isni`](https://bioregistry.io/isni)                     |     4,105 |
| `dai`                                                     |     1,982 |
| `authenticus`                                             |     1,422 |
| `dialnet`                                                 |     1,210 |
| [`wikidata`](https://bioregistry.io/wikidata)             |       147 |

The results of this process are first available as part of the records file(s). Second, they are available through
a dedicated file ([sssom.tsv.gz](https://zenodo.org/records/11474470/files/sssom.tsv.gz?download=1)) in
the [Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
that solely focuses on the cross-references. Here's what the first few lines of that file look like:

| subject_id                                                                    | subject_label       | predicate_id    | object_id                                                                       | mapping_justification        |
|-------------------------------------------------------------------------------|---------------------|-----------------|---------------------------------------------------------------------------------|------------------------------|
| [orcid:0000-0001-5099-6000](https://bioregistry.io/orcid:0000-0001-5099-6000) | Debashis Bhowmick   | skos:exactMatch | [scopus:57214299968](https://bioregistry.io/scopus:57214299968)                 | semapv:ManualMappingCuration |
| [orcid:0000-0001-5009-9000](https://bioregistry.io/orcid:0000-0001-5009-9000) | Ali Gargouri        | skos:exactMatch | loop:470724                                                                     | semapv:ManualMappingCuration |
| [orcid:0000-0001-5084-9000](https://bioregistry.io/orcid:0000-0001-5009-9000) | Luana Licata        | skos:exactMatch | loop:1172627                                                                    | semapv:ManualMappingCuration |
| [orcid:0000-0001-5084-9000](https://bioregistry.io/orcid:0000-0001-5009-9000) | Luana Licata        | skos:exactMatch | [scopus:6603618518](https://bioregistry.io/scopus:6603618518)                   | semapv:ManualMappingCuration |
| [orcid:0000-0001-5124-3000](https://bioregistry.io/orcid:0000-0001-5124-3000) | Wojciech Nawrocki   | skos:exactMatch | loop:661557                                                                     | semapv:ManualMappingCuration |
| [orcid:0000-0001-5075-0000](https://bioregistry.io/orcid:0000-0001-5075-0000) | Xueyong Pang        | skos:exactMatch | [wos.researcher:K-6721-2018](https://bioregistry.io/wos.researcher:K-6721-2018) | semapv:ManualMappingCuration |
| [orcid:0000-0001-5103-2000](https://bioregistry.io/orcid:0000-0001-5103-2000) | Bartlomiej Dec      | skos:exactMatch | [scopus:57194469902](https://bioregistry.io/scopus:57194469902)                 | semapv:ManualMappingCuration |
| [orcid:0000-0001-5020-8000](https://bioregistry.io/orcid:0000-0001-5020-8000) | Sapna Gambhir       | skos:exactMatch | [scopus:35811915000](https://bioregistry.io/scopus:35811915000)                 | semapv:ManualMappingCuration |
| [orcid:0000-0001-5074-2000](https://bioregistry.io/orcid:0000-0001-5074-2000) | Martin Perez-Santos | skos:exactMatch | [scopus:56082352000](https://bioregistry.io/scopus:56082352000)                 | semapv:ManualMappingCuration |

### What are Cross-References Useful For?

There are many different nomenclature authorities because each have different goals and data models associated with
records. Different communities also value different nomenclature authorities differently. For example, life scientists
are more often using ORCID when publishing, but including persistent identifiers in publications is not yet common
in computer science papers. Further, computer scientists more often link to
their [DBLP](https://bioregistry.io/registry/dblp.author),
arXiv, OpenReview, or other computer-science focused pages.

When assembling data and knowledge from more than a single resource, it's important to resolve the identifiers
used for researchers to a single identifier - it's not good if different knowledge is connected to an ORCID and a
DBLP for a single researcher. This can be resolved using a combination of semantic mappings (i.e., cross-references)
and software for the large-scale automated assembly of mappings such as the
[Semantic Mapping Reasoning Assembler (SeMRA)](https://github.com/biopragmatics/semra).
It allows for specifying a priority list of nomenclature authorities to assemble coherent knowledge from ORCID
and other sources simultaneously.

This is also a much more valuable process when combining other mapping resources. Wikidata has put a lot of effort
into capturing bibliographic metadata, especially to support the [Scholia project](https://scholia.toolforge.org/).
The following SPARQL query against Wikidata shows that there are 1,811,573 (about 10% of all ORCID records) links from
Wikidata entries to ORCID as of June 2024. [Run it yourself](https://w.wiki/AHew).

```sparql
SELECT (count(DISTINCT ?orcid) as ?total)
WHERE { ?item wdt:P496 ?orcid }
```

[OpenCheck](https://opencheck.is/) tried to create mappings between Twitter, GitHub, and ORCID using their APIs, but
became defunct when Twitter shut off their public APIs.
Other mapping resources probably exist, please let me know if you're aware of other ones!

## Affiliations

| Resource                                                  |     Count |
|-----------------------------------------------------------|----------:|
| [`ror`](https://bioregistry.io/ror)                       | 8,725,215 |
| [`ringgold`](https://bioregistry.io/ringgold)             | 6,614,519 |
| [`grid`](https://bioregistry.io/grid)                     | 1,404,183 |
| [`funderregistry`](https://bioregistry.io/funderregistry) |   698,384 | 
| `lei`                                                     |     1,206 |

## Education Roles

| Education Role                            |     Count |
|-------------------------------------------|----------:|
| Doctor of Philosophy                      | 1,231,845 |
| Master                                    |   426,625 |
| Bachelor                                  |   402,297 |
| Master of Science                         |   360,052 |
| Bachelor of Science                       |   322,853 |
| Doctor of Medicine                        |   202,884 |
| Bachelor of Arts                          |   108,778 |
| Master of Arts                            |    78,601 |
| Postdoctoral Researcher                   |    37,548 |
| Bachelor of Medicine, Bachelor of Surgery |    27,722 |
| Master of Technology                      |    22,473 |
| Bachelor of Technology                    |    21,465 |
| Bachelor of Engineering                   |    21,345 |
| Diploma                                   |    20,695 |
| Master of Business Administration         |    19,660 |
| Master of Philosophy                      |    18,069 |
| Master of Education                       |    18,055 |
| Master of Public Health                   |    17,760 |
| Bachelor of Education                     |    17,376 |
| Master of Engineering                     |    14,260 |

1. https://degree.studentnews.eu lists degrees conferred in the EU/Europe
2. https://github.com/vivo-ontologies/academic-degree-ontology is an incomplete/abandoned
   effort from 2020 to ontologize degree names
3. Wikidata has a class for academic degree https://www.wikidata.org/wiki/Q189533. Its
   `SPARQL query service <https://query.wikidata.org>`_ can be queried with the following,
   though note that the Wikidata class hierarchy is broken in several places.

   ```sparql
      SELECT ?item ?itemLabel WHERE {
         ?item wdt:P279* wd:Q189533 .
         SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
       }
   ```

It's tricky to decide what's a different degree vs. just a degree in a certain discipline, for example,
a bachelor of engineering is sometimes awarded for studying engineering but otherwise a bachelor of science might be
awarded.

Also, for education, people often put the discipline (e.g., just "Chemistry") instead of saying what degree level it
was.

There's a similar situation for employment.

## Authorship

Authorships are extracted and standardized in the pubmeds.tsv.gz file, which contains an ORCID column and PubMed column
that has been pre-sanitized to only contain local unique identifiers. This information is also available through the
main records file.

Some things to deal with:

1. The field that is labeled to contain a PubMed identifier contains a mix of local unique identifiers, valid Compact
   URIs (CURIEs), invalid CURIEs, URIs, free text that's totally irrelevant. Needs custom processing.

2023 statistics:

- correct: 3,175,196 (99.85%)
- needs processing: 2,832 (0.09%)
- junk: 2,080 (0.07%)

what was in here? a mashup of:

- DOIs
- PMC identifiers,
- a few stray strings that contain a combination of pubmed, PMC,
- a lot with random text (keywords)
- some `with full text citations

## Lexical Indexing

It includes two pre-built Gilda indexes for named entity recognition (NER) and named entity normalization (NEN). One
contains all records, and the second is filtered to high-quality records. The following Python code snipped can be used
for grounding:

```python
from gilda import Grounder

url = "..."
grounder = Grounder(url)
results = grounder.ground("Charles Tapley Hoyt")
```

It is automatically generated with code in https://github.com/cthoyt/orcid_downloader.