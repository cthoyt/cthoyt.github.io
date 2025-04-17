---
layout: post
title:
  The `EFO_ID` column in ChEMBL's drug indications table isn't what you think
date: 2025-04-17 18:42:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEBI
  - ChEMBL
  - UBERON
  - Experimental Factor Ontology
  - EFO
  - GO
  - Gene Ontology
  - clinical trials
---

ChEMBL periodically curates clinical trial information into its
`DRUG_INDICATION` table. However, there's some weird inconsistencies in the way
it references disease concepts in external vocabularies. This blog post is an
exploration of that table.

As of ChEMBL v35, the `DRUG_INDICATION` table contains the following columns:

1. `DRUGIND_ID` - a unique identifier for the chemical-indication pair
2. `MOLREGNO` - a foreign key to the molecules table
3. `MAX_PHASE_FOR_IND` - the maximum phase achieved by clinical trials of the
   chemical-indication pair
4. `MESH_ID` - the local unique identifier from
   [Medical Subject Headings (MeSH)](https://bioregistry.io/mesh) for the
   indication
5. `MESH_HEADING` - the label in MeSH for the given MeSH ID
6. `EFO_ID` - A compact URI (CURIE) for a term in the
   [Experimental Factor Ontology (EFO)](https://bioregistry.io/efo) ( in theory)
7. `EFO_TERM` - a label for the CURIE in the `EFO_ID` column

This is already strange, considering that for cell lines, tissues, and targets,
ChEMBL has created its own table which contains the cross-references to external
vocabularies. Here, they're baked into the pivot table.

The funny business is about the `EFO_ID` column:

1. It's strange that the `MESH_ID` column uses local unique identifiers but the
   `EFO_ID` column uses compact URIs (CURIEs). CURIEs are a syntax for
   referencing an entity in an ontology or database that takes the form of
   `<prefix>:<local unique identifier>`. The `prefix` is usually the acronym for
   the resource and the local unique identifier is the ID inside the resource
   (usually a number). More on this in [my previous
   post]({% post_url 2021-09-14-curies %}).
2. The CURIEs in the `EFO_ID` column aren't all using `EFO` as the prefix!

Let's have a look at what's actually in the `EFO_ID` column by using the
[`chembl_downloader`](https://github.com/cthoyt/chembl-downloader) Python
package to automatically download the latest version of ChEMBL and run SQL
queries over it.

```python
import chembl_downloader

chembl_downloader.query("""\
   SELECT DISTINCT efo_id, efo_term
   FROM DRUG_INDICATION
   WHERE efo_id NOT LIKE 'EFO:%'
""")
```

| efo_id          | efo_term                     |
| --------------- | ---------------------------- |
| HP:0001945      | Fever                        |
| Orphanet:309005 | Disorder of lipid metabolism |
| HP:0003124      | Hypercholesterolemia         |
| Orphanet:79211  | Combined hyperlipidemia      |
| HP:0000023      | Inguinal hernia              |
| ...             | ...                          |

Using a bit of SQL string processing to identify the prefixes and the
[Bioregistry](https://bioregistry.io) to retrieve the name and homepage gives a
bit more context about what the prefixes in CURIEs in the `EFO_ID` column
represent.

```python
import bioregistry
import chembl_downloader

sql = """\
SELECT prefix, count(prefix) as count
FROM (
    SELECT substr(efo_id, 0, instr(efo_id, ":")) as prefix
    FROM DRUG_INDICATION
)
GROUP BY prefix
HAVING count(prefix) > 0
ORDER BY count(prefix) DESC
"""

df = chembl_downloader.query(sql)
df["name"] = df["prefix"].map(bioregistry.get_name)
df["homepage"] = df["prefix"].map(bioregistry.get_homepage)
```

| prefix   |  count | name                                     | homepage                                           |
| -------- | -----: | ---------------------------------------- | -------------------------------------------------- |
| EFO      | 37,603 | Experimental Factor Ontology             | http://www.ebi.ac.uk/efo                           |
| MONDO    | 13,532 | Mondo Disease Ontology                   | https://monarch-initiative.github.io/mondo         |
| HP       |  3,381 | Human Phenotype Ontology                 | http://www.human-phenotype-ontology.org/           |
| Orphanet |    359 | Orphanet                                 | http://www.orpha.net/consor/                       |
| MP       |    281 | Mammalian Phenotype Ontology             | https://www.informatics.jax.org/vocab/mp_ontology/ |
| GO       |     50 | Gene Ontology                            | http://geneontology.org/                           |
| DOID     |     45 | Human Disease Ontology                   | http://www.disease-ontology.org                    |
| CHEBI    |     19 | Chemical Entities of Biological Interest | http://www.ebi.ac.uk/chebi                         |
| UBERON   |      1 | Uber Anatomy Ontology                    | http://uberon.org                                  |

The ones that stand out to me are `CHEBI`, `UBERON`, and `GO`, since these
resources are respectively for chemicals, anatomical entities, and biological
processes/cellular components/molecular functions.

I wrote the following function to do a bit of exploring, based on the prefix.

```python
import chembl_downloader

def print_indications_with_prefix(prefix: str) -> "pd.DataFrame":
    sql = f"""\
        SELECT DISTINCT
            MOLECULE_DICTIONARY.chembl_id,
            MOLECULE_DICTIONARY.pref_name,
            DRUG_INDICATION.efo_id,
            DRUG_INDICATION.efo_term
        FROM MOLECULE_DICTIONARY
            JOIN DRUG_INDICATION ON MOLECULE_DICTIONARY.molregno == DRUG_INDICATION.molregno
        WHERE DRUG_INDICATION.efo_id LIKE '{prefix}:%'
        ORDER BY MOLECULE_DICTIONARY.pref_name
        """
    df = chembl_downloader.query(sql)
    df["chembl_id"] = df["chembl_id"].map(lambda s: f"[{s}](https://bioregistry.io/chembl.compound:{s})")
    df["efo_id"] = df["efo_id"].map(lambda s: f"[{s}](https://bioregistry.io/{s})")
    print(df.to_markdown(tablefmt="github", index=False))
```

Using `UBERON` returns a single result, which appears to be a mistake / an abuse
of the database schema.

| chembl_id                                                             | pref_name      | efo_id                                                  | efo_term   |
| --------------------------------------------------------------------- | -------------- | ------------------------------------------------------- | ---------- |
| [CHEMBL4650497](https://bioregistry.io/chembl.compound:CHEMBL4650497) | PEGSITACIANINE | [UBERON:0000029](https://bioregistry.io/UBERON:0000029) | lymph node |

Using `CHEBI` returns a large number of diagnostic agents. This is part of the
"role" hierarchy within ChEBI, and also what I would consider an abuse of the
database schema.

| chembl_id                                                             | pref_name                        | efo_id                                            | efo_term             |
| --------------------------------------------------------------------- | -------------------------------- | ------------------------------------------------- | -------------------- |
| [CHEMBL1234270](https://bioregistry.io/chembl.compound:CHEMBL1234270) | ARFOLITIXORIN                    | [CHEBI:44185](https://bioregistry.io/CHEBI:44185) | methotrexate         |
| [CHEMBL5314823](https://bioregistry.io/chembl.compound:CHEMBL5314823) | DIGADOGLUCITOL                   | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4650354](https://bioregistry.io/chembl.compound:CHEMBL4650354) | FLORBENGUANE F18                 | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5095045](https://bioregistry.io/chembl.compound:CHEMBL5095045) | FLORZOLOTAU (18F)                | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314559](https://bioregistry.io/chembl.compound:CHEMBL5314559) | FLOTUFOLASTAT F 18 GALLIUM       | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4298157](https://bioregistry.io/chembl.compound:CHEMBL4298157) | FLUBROBENGUANE F18               | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314633](https://bioregistry.io/chembl.compound:CHEMBL5314633) | IODINE I124 EVUZAMITIDE          | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4298185](https://bioregistry.io/chembl.compound:CHEMBL4298185) | LONAPEGSOMATROPIN                | [CHEBI:37845](https://bioregistry.io/CHEBI:37845) | growth hormone       |
| [CHEMBL5314761](https://bioregistry.io/chembl.compound:CHEMBL5314761) | PEGFOSIMER MANGANESE             | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4650497](https://bioregistry.io/chembl.compound:CHEMBL4650497) | PEGSITACIANINE                   | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4297334](https://bioregistry.io/chembl.compound:CHEMBL4297334) | PIFLUFOLASTAT F18                | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314483](https://bioregistry.io/chembl.compound:CHEMBL5314483) | RIZEDISBEN                       | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314650](https://bioregistry.io/chembl.compound:CHEMBL5314650) | TECHNETIUM TC-99M LABELED CARBON | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4298067](https://bioregistry.io/chembl.compound:CHEMBL4298067) | TOMARALIMAB                      | [CHEBI:35610](https://bioregistry.io/CHEBI:35610) | antineoplastic agent |
| [CHEMBL5314445](https://bioregistry.io/chembl.compound:CHEMBL5314445) | VIDOFLUFOLASTAT(18F)             | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4594280](https://bioregistry.io/chembl.compound:CHEMBL4594280) | VIPIVOTIDE TETRAXETAN            | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL4594411](https://bioregistry.io/chembl.compound:CHEMBL4594411) | XENON XE-129, HYPERPOLARIZED     | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314610](https://bioregistry.io/chembl.compound:CHEMBL5314610) | ZOPOCIANINE                      | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |
| [CHEMBL5314611](https://bioregistry.io/chembl.compound:CHEMBL5314611) | ZOPOCIANINE SODIUM               | [CHEBI:33295](https://bioregistry.io/CHEBI:33295) | diagnostic agent     |

Using `GO` returns aging, regulation of ovulation (both positive and negative),
and wound healing as the four unique biological processes. This is a little less
controversial than UBERON and CHEBI, but it still has a bit of a mismatch for
the idea of an "indication".

| chembl_id                                                             | pref_name                | efo_id                                          | efo_term                         |
| --------------------------------------------------------------------- | ------------------------ | ----------------------------------------------- | -------------------------------- |
| [CHEMBL1566](https://bioregistry.io/chembl.compound:CHEMBL1566)       | ACARBOSE                 | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL600](https://bioregistry.io/chembl.compound:CHEMBL600)         | ACETYLCYSTEINE           | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1399](https://bioregistry.io/chembl.compound:CHEMBL1399)       | ANASTROZOLE              | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL25](https://bioregistry.io/chembl.compound:CHEMBL25)           | ASPIRIN                  | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1201556](https://bioregistry.io/chembl.compound:CHEMBL1201556) | BECAPLERMIN              | [GO:0042060](https://bioregistry.io/GO:0042060) | wound healing                    |
| [CHEMBL5315086](https://bioregistry.io/chembl.compound:CHEMBL5315086) | BETULA PUBESCENS BARK    | [GO:0042060](https://bioregistry.io/GO:0042060) | wound healing                    |
| [CHEMBL1200800](https://bioregistry.io/chembl.compound:CHEMBL1200800) | CALCIUM ACETATE          | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1200539](https://bioregistry.io/chembl.compound:CHEMBL1200539) | CALCIUM CARBONATE        | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL113313](https://bioregistry.io/chembl.compound:CHEMBL113313)   | CAPROMORELIN             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1042](https://bioregistry.io/chembl.compound:CHEMBL1042)       | CHOLECALCIFEROL          | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL2108185](https://bioregistry.io/chembl.compound:CHEMBL2108185) | CORIFOLLITROPIN ALFA     | [GO:0060279](https://bioregistry.io/GO:0060279) | positive regulation of ovulation |
| [CHEMBL429910](https://bioregistry.io/chembl.compound:CHEMBL429910)   | DAPAGLIFLOZIN            | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1421](https://bioregistry.io/chembl.compound:CHEMBL1421)       | DASATINIB                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL139](https://bioregistry.io/chembl.compound:CHEMBL139)         | DICLOFENAC               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL367149](https://bioregistry.io/chembl.compound:CHEMBL367149)   | DOCONEXENT               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1200969](https://bioregistry.io/chembl.compound:CHEMBL1200969) | DUTASTERIDE              | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL135](https://bioregistry.io/chembl.compound:CHEMBL135)         | ESTRADIOL                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL2108390](https://bioregistry.io/chembl.compound:CHEMBL2108390) | FIBRIN                   | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL500468](https://bioregistry.io/chembl.compound:CHEMBL500468)   | GHRELIN                  | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL389621](https://bioregistry.io/chembl.compound:CHEMBL389621)   | HYDROCORTISONE           | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL13817](https://bioregistry.io/chembl.compound:CHEMBL13817)     | IBUTAMOREN               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL460026](https://bioregistry.io/chembl.compound:CHEMBL460026)   | ICOSAPENT                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL2109042](https://bioregistry.io/chembl.compound:CHEMBL2109042) | INFLUENZA VIRUS VACCINE  | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL471737](https://bioregistry.io/chembl.compound:CHEMBL471737)   | IVABRADINE               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL444814](https://bioregistry.io/chembl.compound:CHEMBL444814)   | L-CITRULLINE             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL191](https://bioregistry.io/chembl.compound:CHEMBL191)         | LOSARTAN                 | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1201419](https://bioregistry.io/chembl.compound:CHEMBL1201419) | LUTROPIN ALFA            | [GO:0060279](https://bioregistry.io/GO:0060279) | positive regulation of ovulation |
| [CHEMBL2107951](https://bioregistry.io/chembl.compound:CHEMBL2107951) | MALTODEXTRIN             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL267936](https://bioregistry.io/chembl.compound:CHEMBL267936)   | MECAMYLAMINE             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1201716](https://bioregistry.io/chembl.compound:CHEMBL1201716) | MECASERMIN               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1431](https://bioregistry.io/chembl.compound:CHEMBL1431)       | METFORMIN                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL650](https://bioregistry.io/chembl.compound:CHEMBL650)         | METHYLPREDNISOLONE       | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL4074884](https://bioregistry.io/chembl.compound:CHEMBL4074884) | MITOQUINONE MESYLATE     | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL438497](https://bioregistry.io/chembl.compound:CHEMBL438497)   | NICOTINAMIDE RIBOSIDE    | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL3](https://bioregistry.io/chembl.compound:CHEMBL3)             | NICOTINE                 | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1201574](https://bioregistry.io/chembl.compound:CHEMBL1201574) | ONABOTULINUMTOXINA       | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1234886](https://bioregistry.io/chembl.compound:CHEMBL1234886) | OXYGEN                   | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL395429](https://bioregistry.io/chembl.compound:CHEMBL395429)   | OXYTOCIN                 | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL90593](https://bioregistry.io/chembl.compound:CHEMBL90593)     | PRASTERONE               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL50](https://bioregistry.io/chembl.compound:CHEMBL50)           | QUERCETIN                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL165](https://bioregistry.io/chembl.compound:CHEMBL165)         | RESVERATROL              | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL413](https://bioregistry.io/chembl.compound:CHEMBL413)         | SIROLIMUS                | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1200574](https://bioregistry.io/chembl.compound:CHEMBL1200574) | SODIUM CHLORIDE          | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL93268](https://bioregistry.io/chembl.compound:CHEMBL93268)     | SODIUM NITRITE           | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL136478](https://bioregistry.io/chembl.compound:CHEMBL136478)   | SODIUM NITROPRUSSIDE     | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL1201621](https://bioregistry.io/chembl.compound:CHEMBL1201621) | SOMATROPIN               | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL48802](https://bioregistry.io/chembl.compound:CHEMBL48802)     | SULFORAPHANE             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL386630](https://bioregistry.io/chembl.compound:CHEMBL386630)   | TESTOSTERONE             | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL2107067](https://bioregistry.io/chembl.compound:CHEMBL2107067) | TESTOSTERONE UNDECANOATE | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |
| [CHEMBL3545347](https://bioregistry.io/chembl.compound:CHEMBL3545347) | TXA127                   | [GO:0007568](https://bioregistry.io/GO:0007568) | aging                            |

---

There wasn't really a point to this post other than to show off a quirk I found
in ChEMBL. This is useful to be aware of when automatically processing the
database in bulk, e.g., for building a knowledge graph.

There are two other follow-up questions I would have about this table:

1. Are there any EFO terms that are outside the disease hierarchy (i.e., not a
   child of [EFO:0000408](http://www.ebi.ac.uk/efo/EFO_0000408))?
2. Why are there DOID terms? The combination of EFO and MONDO _should_ cover
   everything. Answering this question actually isn't so difficult given my
   recent work on assembling mappings with
   [SeMRA](https://github.com/biopragmatics/semra), specifically for the
   [disease landscape](https://github.com/biopragmatics/semra/tree/main/notebooks/landscape#example).
   I'll try to come back to this in a future post.

If you made it this far: what did you think about my clickbait title?
