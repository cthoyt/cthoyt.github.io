---
layout: post
title: Discussions and Follow-ups from Biocuration 2024
date: 2024-03-11 14:52:00 +0100
author: Charles Tapley Hoyt
tags:
  - International Society of Biocuration
  - biocuration
---

I've just returned from the
<a href="https://ibdc.rcb.res.in/biocuration2024/">17<sup>th</sup> Annual
International Biocuration Conference</a> at the Indian Biological Data Centre
(IBDC) in Faridabad, India. I wanted to highlight some of the interesting
conversations I had while I was there, and ideas for follow-up. Most were
centered around the [Bioregistry](https://bioregistry.io) and the
[Semantic Mapping Assembler and Reasoner (SeMRA)](https://github.com/biopragmatics/semra),
which I gave an oral presentation on.

I talked to Guy Cochrane and Chuck Cook from the
[Global Biodata Coalition (GBC)](https://globalbiodata.org/). They chaired a
session on sustainability of biocurated resources, with specific focus on the
Global Biodata Coalition's
[Global Biodata Core Resources (GBCR)](https://globalbiodata.org/what-we-do/global-core-biodata-resources/)
initiative. I felt like my talk from last year's biocuration conference on the
Open Code, Open Data, Open Infrastructure (O3) roadmap
([preprint](https://doi.org/10.31219/osf.io/vuzt3)) would have fit right in
here. I am very keen to have their perspectives, as GBC has first worked on
evaluation of resources and is second working towards funding resources. Since
they have not worked on practical recommendations for supporting sustainability,
I eagerly volunteered to join their work in some capacity to help advise on
this.

GBC also published a workflow for evaluating the landscape of biological
databases
([press release](https://globalbiodata.org/what-we-do/global-inventory/) /
[publication](https://doi.org/10.1371/journal.pone.0294812) /
[code](https://github.com/globalbiodata/inventory_2022/)). When possible, this
workflow aligned on
[FAIRsharing](https://bioregistry.io/metaregistry/fairsharing), but given that
it is a limited resource and only has partial mappings to relevant related
resources like [re3code](https://bioregistry.io/metaregistry/re3data),
[BARTOC](https://bioregistry.io/metaregistry/bartoc), etc. I suggested using the
Bioregistry as a mapping hub to enrich the output of this workflow, which will
definitely be run again on a periodic basis.

Lynn Schriml presented recent updates on the Disease Ontology, which prompted a
relevant question from Harpreet Singh - Chief Data Officer at the Indian Council
of Medical Research (ICMR) who himself works with clinical data and has wondered
how to best annotate - using [MeSH](https://bioregistry.io/mesh),
[SNOMED](https://bioregistry.io/snomed), [ICD](https://bioregistry.io/icd11), or
other disease resources. I had an interesting discussion with him following the
talk which gave big motivation to the talk I was about to give on the
[large scale assembly and reasoning over semantic mappings](https://bit.ly/biocuration2024-cth).
I was very excited, since I love to add (last minute) shout-outs into my
conference talks that motivate parts of the work based on questions or
discussions from earlier parts of the conference.

There were a series of talks that motivated further discussions about mappings.
One of the most interesting was the talk from Shivani Sharma, a curator at the
[Indian Biological Data Centre (IBDC)](https://ibdc.rcb.res.in/) and one of the
local organizers. She works on the
[Indian Metabolome Data Archive](https://ibdc.rcb.res.in/imda/). Many of the
lines of work at the IBDC have practical applications towards agriculture and
integrate medium- and large-scale experimental work, biocuration, and downstream
analysis. Often, these applications are oriented towards improving crop yields
and avoiding disease. Shivani showed a slide where they considered a large
number of metabolomics nomenclature resources to use for annotating their data.
However, they were not familiar with methods for incorporating multiple
nomenclature resources, meaning that their curators were running into issues
where their chosen metabolomics database did not cover chemicals they needed to
annotate. This often lead to them having to create their own _ad hoc_
annotations, which also create issues for data integration. I am looking
forwards to catching up with them again, incorporating new metabolomics resource
into [PyOBO](https://github.com/biopragmatics/pyobo), ingesting mappings into
[SeMRA](https://github.com/biopragmatics/semra), and filling in the gaps using
Biomappings to support their curators.

Scott V. Nguyen from the
[American Type Culture Collection (ATCC)](https://bioregistry.io/atcc) also
approached me about this work, since he's currently trying to curate mappings
between cell lines in their resource and other public resources. It was lucky
that one of the examples from my talk was specifically about the cell lince
scenario, which I hope he can ingest and reduce his curation workload. Rachel
Lyne also presented on [COSMIC](https://bioregistry.io/cosmic.cell), a cancer
cell line resource that also creates its own accession numbers and could benefit
from this work, but I didn't get a chance to talk about it with her yet.

I also met Yasunori Yamamoto, who works on [TogoID](https://togoid.dbcls.jp/), a
secondary database of semantic mappings that covers select domains within
biomedicine. We discussed how they could make use of the
[Simple Standard for Sharing Ontology Mappings (SSSOM)](https://academic.oup.com/database/article/doi/10.1093/database/baac035/6591806)
to ingest more mappings from different resources, especially from Biomappings or
potentially from the outputs of SeMRA (which I presented on).

Matt Jeffreys presented on the annotations database in
[European PubMed Central](https://europepmc.org/) which allows for tagging
articles, sentences, or tokens in articles with annotations. They already showed
how this applies to named entity recognition (NER) and MeSH term annotations,
but we discussed how SeMRA and comprehensive semantic mapping databases could
help unify other annotations of overlapping vocabularies, e.g., if someone put
Disease Ontology (DO) NER annotations, which overlap with MeSH terms in the
disease (C) and psychiatric disorders (F) branches.

I discussed with Raja Mazumdar and Jeet Vora from George Washington University
who both work on [GlyGen](https://bioregistry.io/glygen) and are plugged into
the NIH's
[Common Fund Data Ecosystem (CFDE)](https://commonfund.nih.gov/dataecosystem)
about how they can continue to use the Bioregistry to standardize the
annotations in their resources. Jeet has got in touch earlier this year and
helped update the records in the Bioregistry related to GlyGen. Raja's talk also
motivated two new prefix additions to the Bioregistry for Biocompute Objects and
for OncoMX data objects. Further, Raja is very interested in improving his data
using the Bioregistry, since it already uses a Python script to validate its
JSON and TSV components, it will be easy to incorporate the Bioregistry Python
package's validation functions.

Earlier this winter, I presented to the American National Institutes of Health
(NIH) BISTI group about different avenues through which they could use the
Bioregistry to create more value for the NIH and its grantees. One of those
discussions was about improving GenBank's
[internal database catalog](https://www.ncbi.nlm.nih.gov/genbank/collab/db_xref/).
By chance, I talked with Ilene Karsch Mizrachi, a program head at the NIH about
this. She was attending the conference and made big contributions to the
discussions about the Indian relation to the International Nucleotide Sequence
Database Collaboration (INSDC). However, it turns out she was the one who
made/contributed to this GenBank table, many years ago. We will try and follow
up by enriching this table with information from the Bioregistry.

At last year's biocuration conference, Chris Hunter presented on
[GigaDB](http://gigadb.org/), and we had some initial discussions about using
the Bioregistry (or other related parts of the Biopragmatics Stack) to make
standardized annotations on data sets deposited in their database, such as cell
line annotations. We picked back up that conversation, and it seems that the
GigaDB developers are working with PHP - since we got CZI funding to make the
Bioregistry available in other languages, making a wrapper from Rust to PHP
(within the [curies.rs](https://github.com/biopragmatics/curies.rs) framework).

There was an entire session on the final day of the conference on structural
bioinformatics, which included several presentations from the American and
[European](https://www.ebi.ac.uk/pdbe) loci of the Protein Databank (PDB). The
first discussion was with Marcus Bage, who is currently trying to annotate
protein modifications. We discussed the implications of the vast number of
resources that partially cover this domain in different senses, including
[GO](https://bioregistry.io/go), [MOD](https://bioregistry.io/mod),
[SBO](https://bioregistry.io/sbo), [MOP / PSI-MI](https://bioregistry.io/mop),
and
[UniProt's internal vocabulary](https://bioregistry.io/registry/uniprot.ptm). A
long time ago, I mapped these together in
[PyBEL](https://github.com/pybel/pybel/blob/ed66f013a77f9cbc513892b0dad1025b8f68bb46/src/pybel/language.py#L346-L582),
but this was only a partial solution, too!

The second discussion was with Brinda Vallat about the upcoming change for PDB
accession numbers. It turns out that the 4 character code is estimated to fill
up in 2029, so it's time for PDB to make a change. Unfortunately, their solution
is to switch to local unique identifiers that look like `pdb_000002GC4`, which
is problematic for two main reasons. First, it's not backwards compatible with
existing IDs. Second, it introduces a banana (i.e., a redundant copy of the
name/acronym of the database in the local unique identifier). The reasoning
behind adding in the banana was to make it easier to find references in papers.
I can understand this, since we don't yet have general solutions for referencing
concepts across different publishers (though, we solved this in Manubot by
integrating the Bioregistry). However, this increases confusion for consumers. I
suggested they simply extend the existing IDs to be able to have more than 4
characters, and suggest people reference their entities with CURIEs like
`PDB:2GC4` within papers, which solves both issues simultaneously. Similarly, I
talked to Ibrahim Roshan Kunnakkattu about creating more careful identifier
recommendations for the PDB's
[Chemical Component Dictionary](https://bioregistry.io/registry/pdb-ccd) as well
as using some of the automated mapping tools I presented for filling out
references to ChEBI, ChEMBL, PubChem, and more.

I also had the unique pleasure to spend time in person with Tiago Lubiana, who
is highly aligned on many of my interests in data standardization, semantic web,
and open science. He has been a helpful contributor in the Bioregistry,
Wikidata, and the OBO Foundry. Writing up some of the things we discussed would
take a whole blog post, so instead, here's a nice picture we got together.

![Charlie Hoyt and Tiago Lubiana](/img/charlie_tiago_march_2024.jpg)

---

Overall, like every Biocuration conference, I was very happy to find people
interested in my work, and more importantly, interested in the idea of improving
their own data standardization! I also had lots of other interesting discussions
that don't require any follow-up. I am also planning on writing a post that
gives a more high-level summary of the different parts of the conference itself,
not just focusing on my work.
