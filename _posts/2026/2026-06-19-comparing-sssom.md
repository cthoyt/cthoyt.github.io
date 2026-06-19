---
layout: post
title: Comparing manually curated semantic mappings in SSSOM
date: 2026-06-19 14:47:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - biocuration
  - curator agreement
---

I am currently supporting [Philip Strömert](https://github.com/StroemPhi) and
[Noura Rayya](https://github.com/NRayya) in the efforts to modernize and
revitalize the [Chemical Methods Ontology (CHMO)](https://semantic.farm/chmo) to
support annotation of instrumentation used to produce experimental data captured
in the [Chemotion](https://chemotion.net/) electronic laboratory notebook as
part of [NFDIChem](https://nfdi4chem.de). This post is about the adoption of
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
to support interoperability between CHMO and other resources, and the workflow I
developed to compare overlapping manual curations from different researchers.

Philip and Noura have already completed the important initial steps of assuming
maintainership from the Royal Society of Chemistry, porting the ontology to use
a standardized
[Ontology Development Kit (ODK)](https://github.com/INCATools/ontology-development-kit/)
layout, and
[revising the definitions](https://github.com/rsc-ontology/rsc-cmo/pull/70) of
many classes based on the [IUPAC GoldBook](https://goldbook.iupac.org).

## Landscape of Resources

There are several other NFDI consortia including NFDI4Cat (catalysis),
DAPHNE4NFDI (photon and neutron physics), and FAIRmat (materials science) that
have similar goals to annotate instrumentation. While each reuse CHMO to some
extent for this purpose, DAPHNE4NFDI additionally develops the
[Photon and Neutron Experimental Techniques (PANET) Ontology](https://semantic.farm/panet)
and FAIRmat develops the [NeXus format](https://www.nexusformat.org/) and
associated [NeXus Ontology](https://semantic.farm/nexus) as part of the
[NOMAD](https://nomad-lab.eu/nomad-lab/index.html) materials science data
management platform.

Further, there are several other resources with similar goals including the
[Allotrope Foundation Ontology (AFO)](https://www.allotrope.org/ontologieshttps://www.allotrope.org/ontologies),
the deprecated
[Physico-chemical Methods and Properties (FIX)](https://semantic.farm/fix)
ontology, the deprecated
[Physico-chemical process (REX)](https://semantic.farm/rex) ontology,
[IUPAC GoldBook](https://goldbook.iupac.org), and
[Wikidata](https://wikidata.org).

# Establishing Interoperability

In order to establish interoperability between these many resources, we are
using the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
to curate exact matches, narrow matches, and broad matches between CHMO terms
and external ones in PANET, NeXuS (sort of), AFO, FIX, REX, IUPAC GoldBook, and
Wikidata.

First, Philip had Ambika, a student research assistant (_Hiwi_, abbreviated in
German), work for several months to manually curate mappings from CHMO to REX,
FIX, AFO, and Wikidata (see
[this PR](https://github.com/rsc-ontology/rsc-cmo/pull/77)).

In parallel, I took the opportunity to spin up a new instance of a
[SSSOM Curator](https://github.com/cthoyt/sssom-curator/) repository within the
NFDI Section Metadata Working Group for Ontology Harmonization and Mappings
[GitHub repository](https://github.com/nfdi-de/section-metadata-wg-onto/tree/main/sssom),
run lexical prediction to generate candidate mappings from CHMO, and efficiently
manually curate the results in
[this PR](https://github.com/nfdi-de/section-metadata-wg-onto/pull/88). and
[this PR](https://github.com/nfdi-de/section-metadata-wg-onto/pull/89) over the
course of about an hour.

## Need for Comparison

The next challenge was to efficiently triage the similarities and differences
between my curations and Ambika's. Therefore, I implemented a workflow for
comparing the manually curated mappings in two SSSOM documents in
[cthoyt/sssom-pydantic#141](https://github.com/cthoyt/sssom-pydantic/pull/141).
This workflow creates a Markdown file describing similarities and differences.

I chained together the following two CLI commands with `sssom_pydantic` to get
the separate mapping files from Ambika's branch in the NFDI4Chem fork of CHMO,
merge them, then run the comparison against my own curations. Note that these
won't be reproducible after the branch is merged and deleted, and the actual
results will change as more curation is done.

```console
$ sssom_pydantic merge \
        --input https://github.com/NFDI4Chem/rsc-cmo/raw/refs/heads/Add-tsv-files/src/mappings/fix-mappings.sssom.tsv \
        --input https://github.com/NFDI4Chem/rsc-cmo/raw/refs/heads/Add-tsv-files/src/mappings/afo-mappings.sssom.tsv \
        --input https://github.com/NFDI4Chem/rsc-cmo/raw/refs/heads/Add-tsv-files/src/mappings/rex-mappings.sssom.tsv \
        --input https://github.com/NFDI4Chem/rsc-cmo/raw/refs/heads/Add-tsv-files/src/mappings/wikidata-mappings.sssom.tsv \
        --standardize \
        --output ambika.sssom.tsv
$ sssom_pydantic compare \
    ambika.sssom.tsv \
    https://github.com/nfdi-de/section-metadata-wg-onto/raw/refs/heads/main/sssom/data/positive.sssom.tsv \
    --standardize \
    --standardize-flip \
    --left-label Ambika \
    --right-label Charlie
```

Since the comparison workflow outputs Markdown, its results can easily be
embedded in GitHub issues or my blog, which is itself written in Markdown.

## Results

I am happy with the first version of the comparison workflow. Luckily, there
were only a small number of discrepancies which have obvious solutions. There
were also a few interesting discrepancies which were novel to either my or
Ambika's curations, which can be reviewed by a third curator (sorry Philip, more
work for you).

## Next Steps

I think that it can be extended to identify and report on one-to-many,
many-to-one, and many-to-many mappings which arise when jointly examining two
mapping sets. After Philip and others interact with the results, I'm sure we
will be able to extend it with other analyses.

More generally, the implementation of the comparison workflow is part of a
larger suite of workflows that I would like to describe in future posts
including:

1. [merging manually curated mappings](https://github.com/cthoyt/sssom-pydantic/pull/136)
2. [generating OWL ontology bridges](https://github.com/cthoyt/sssom-pydantic/pull/128)
3. incorporating SSSOM into ODK builds, which I will support
   [Damien Goutte-Gattat](https://github.com/gouttegd) to document in the ODK
   repository and the [OBOOK](https://oboacademy.github.io/obook).
4. unify this analysis with my other idea for doing
   [automated evaluation of predicted mappings](https://github.com/cthoyt/sssom-pydantic/pull/131),
   which I hope can be used to run future mapping challenges

Without further ado, here's the comparison, copied verbatim from the output of
the previous command:

# Comparison between Ambika and Charlie

1. [CHMO to FIX](#chmo-to-fix)
1. [CHMO to REX](#chmo-to-rex)

## CHMO to FIX

### Subject Comparison

- 288 entities appear as subjects only in Ambika
- 19 entities appear as subjects only in Charlie only
- 138 entities appear as subjects in both

The following 6 subjects (4.3%) appearing in both have conflicting objects:

| subject_id   | subject_label                                       | Ambika                                                            | both                                             | Charlie                                                  |
| ------------ | --------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| CHMO:0000141 | diffraction method                                  | FIX:0000004 (crystallography)                                     | FIX:0000217 (diffraction method)                 |                                                          |
| CHMO:0000164 | electron scattering                                 | FIX:0000666 (electron scattering spectroscopy)                    | FIX:0000401 (electron scattering)                |                                                          |
| CHMO:0000255 | flame atomic emission spectroscopy                  | FIX:0000935 (spark method)                                        | FIX:0000928 (flame atomic emission spectroscopy) |                                                          |
| CHMO:0000307 | X-ray emission spectroscopy                         | FIX:0000673 (X-ray fluorescence spectroscopy)                     | FIX:0000100 (X-ray emission spectroscopy)        |                                                          |
| CHMO:0000366 | electron energy loss spectroscopy                   | FIX:0000664 (electron impact spectroscopy)                        | FIX:0000663 (electron energy loss spectroscopy)  |                                                          |
| CHMO:0000570 | proton transfer reaction ion trap mass spectrometry | FIX:0000919 (proton transfer reaction ion trap mass spectrometry) |                                                  | FIX:0000918 (proton transfer reaction mass spectrometry) |

### Object Comparison

- 296 entities appear as objects only in Ambika
- 19 entities appear as objects only in Charlie
- 138 entities appear as objects in both

The following 2 objects (1.4%) appearing in both have conflicting subjects:

| object_id   | object_label                     | Ambika                                      | both                                    | Charlie                                         |
| ----------- | -------------------------------- | ------------------------------------------- | --------------------------------------- | ----------------------------------------------- |
| FIX:0000629 | pulsed field gel electrophoresis | CHMO:0002315 (pulsed-field electrophoresis) |                                         | CHMO:0002316 (pulsed-field gel electrophoresis) |
| FIX:0000816 | square-wave polarography         | CHMO:0000040 (square-wave voltammetry)      | CHMO:0000035 (square-wave polarography) |                                                 |

### Subject-Object Pair Comparison

- 301 subject-object pairs only appear in Ambika
- 20 subject-object pairs only appear in Charlie
- 137 subject-object pairs appear in both

The following 1 subject-object pairs (0.7%) appearing in have conflicting
predicates or predicate modifiers:

| subject_id   | subject_label       | object_id   | object_label        | warning             | Ambika           | Charlie         |
| ------------ | ------------------- | ----------- | ------------------- | ------------------- | ---------------- | --------------- |
| CHMO:0000164 | electron scattering | FIX:0000401 | electron scattering | different predicate | skos:narrowMatch | skos:exactMatch |

## CHMO to REX

### Subject Comparison

- 1 entities appear as subjects only in Ambika
- 18 entities appear as subjects only in Charlie only
- 0 entities appear as subjects in both

### Object Comparison

- 1 entities appear as objects only in Ambika
- 18 entities appear as objects only in Charlie
- 0 entities appear as objects in both

### Subject-Object Pair Comparison

- 1 subject-object pairs only appear in Ambika
- 18 subject-object pairs only appear in Charlie
- 0 subject-object pairs appear in both
