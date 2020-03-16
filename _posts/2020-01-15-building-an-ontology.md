---
layout: post
title: Building an Ontology
date: 2020-01-22 00:00:00 -0800
---
Before I joined the Fraunhofer SCAI Department of Bioinformatics for my master's and PhD,
they had made first attempts at generating several narrow ontologies within the field
of neurodegenerative disease research [1-4].

## What they did wrong

- Problems with Protoge - messy organization, and most of the powers of ontology
  are overkill for biology (though there are some fantastic examples like HPO)
- Poor labels
- No xrefs - hugely redundant of other resources that already existed
- No way of importing new xrefs automatically as other dbs update

## How to

1. Pick a memorable, but short name.
2. Pick entity types (classes.tsv)
3. Make an author list using ORCID identifiers (authors.tsv)
4. Pick a memorable regular expression for identifiers. In CONSO, I used it as a prefix to 5 integers for good measure.
5. Start curating terms (terms.tsv). You'll need a few fields:
   - Author ORCID
   - Identifier (this is never allowed to change, and must always be increasing)
   - Entity Type
   - Label
   - Description
   - References in the literature
6. Curation of synonyms (synonyms.tsv). Each synonym needs its own metadata so this gets a separate file
7. Curation of xrefs (xrefs.tsv). Each xref needs its own metadata so it also gets a separate file
8. Curation of Relations. This needs a bit more thought, since


## References

1. Malhotra A, *et al*. (2013) [ADO: a disease ontology representing the domain knowledge specific to Alzheimer's disease](https://doi.org/10.1016/j.jalz.2013.02.009).
2. Younesi E, *et al*. (2015) [PDON: Parkinson's disease ontology for representation and modeling of the Parkinson's disease knowledge domain](https://doi.org/10.1186/s12976-015-0017-y)
3. Iyappan A, *et al.* (2017) [Neuroimaging Feature Terminology: A Controlled Terminology for the Annotation of Brain Imaging Features](https://doi.org/10.3233/jad-161148)
4. Malhotra A, *et al*. (2014) [Knowledge Retrieval from PubMed Abstracts and Electronic Medical Records with the Multiple Sclerosis Ontology]( https://doi.org/10.1371/journal.pone.0116718)
