---
layout: post
title: Reproducibly Loading the ChEMBL Relational Database
date: 2021-08-04 13:46:00 +0100
author: Charles Tapley Hoyt
tags: cheminformatics chembl sql
---
In his blog post, [Some Thoughts on Comparing Classification Models](https://practicalcheminformatics.blogspot.com/2020/05/some-thoughts-on-comparing.html),
Pat Walters illustrated enlightened ways to convey the results of training and evaluating machine learning models
on [hERG](https://en.wikipedia.org/wiki/HERG) activity data from ChEMBL (spoiler, it's
[box plots](https://en.wikipedia.org/wiki/Box_plot)). It started by querying the ChEMBL relational database, but featured
a common issue that hampers reproducibility: hard-coded configuration to a local database based on a specific RDBMS (
MySQL). This blog post is about how to address this
[`chembl_downloader`](https://github.com/cthoyt/chembl-downloader) and make code using ChEMBL's SQL dump more reusable
and reproducible.

The original blog post pointed to code [here](https://github.com/PatWalters/comparing_classifier). It was slightly
modified [here](https://github.com/PatWalters/jcamd_model_comparison) to include the code that queries
ChEMBL (among other things).
The [original notebook](https://nbviewer.jupyter.org/github/PatWalters/jcamd_model_comparison/blob/92cc912f24dcac5cad0c52143b67b8c2c124c11e/jcamd_model_comparison.ipynb)
began like this (edited for clarity):

```python
import mysql.connector as sql
import pandas as pd

sql = """
select
    canonical_smiles,
    cs.molregno,
    md.chembl_id as mol_chembl_id,
    standard_relation, standard_value, standard_type, standard_units, description,
    td.organism, assay_type, confidence_score,
    td.pref_name, td.chembl_id as tgt_chembl_id
from activities act
    join assays ass on act.assay_id = ass.assay_id
    join target_dictionary td on td.tid = ass.tid
    join compound_structures cs on cs.molregno = act.molregno
    join molecule_dictionary md on md.molregno = cs.molregno
where ass.tid = 165
    and assay_type in ('B','F')
    and standard_value is not null
    and standard_units = 'nM'
    and act.standard_relation is not null
    and standard_type = 'IC50'
    and standard_relation = '='
"""

with sql.connect(
    host='localhost',
    database='chembl_26',
    user='pwalters',
    password='itsasecret',
) as con:
    df = pd.read_sql(sql, con=con)
```

There are two main issues with this code:

1. It uses a specific database (MySQL) and user-specific connection configuration which means:
    - Nobody else can run this code without editing it.
    - There's no information about how to get, preprocess, or load the database before running the script.
2. It relies on a specific version of ChEMBL, which means that we can't benefit from new compounds and assays in new
   releases without editing it.

To be fair, this is a blog post that's not necessarily supposed to be reused. But what if were so easy to fix this
anti-pattern that there's no excuse not to? Here's how using
the [`chembl_downloader`](https://github.com/cthoyt/chembl-downloader) Python package:

```python
import chembl_downloader
import pandas as pd

sql = ...  # omitted for brevity

version = "26"
with chembl_downloader.connect(version=version) as con:
    df = pd.read_sql(sql, con=con)
```

With only a single (logical) line changed, this code now knows how to download the ChEMBL 26 SQLite dump from the
source, store it in a deterministic location, extract it, and load with SQLite.

This means that anyone can run it
without knowing how to download ChEMBL themselves, which version to get, how to name the file, or where to put it on
their machine. It also relies on SQLite, which is effectively available on all devices that run Python and has
exactly the same programmatic API, but without the need to run or connect to extra software.
While a RDBMS like MySQL might be more powerful for kinds of queries, the difference
is negligible when querying single assays.
It also implicitly solves the problem that the user doesn't know if there was any pre-processing done to the file.

Under the hood, it's using the
[`pystow`](https://github.com/cthoyt/pystow) package to deterministically pick a folder (`~/.data/chembl/26/`) into which
the file `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_29/chembl_29_sqlite.tar.gz`
is download (`~/.data/chembl/26/chembl_29_sqlite.tar.gz`).

Since the pattern of connecting to the database then running a SQL query with pandas is so common, the
`chembl_downloader` has a `query()` function that wraps the two lines from the previous example:

```python
import chembl_downloader

sql = ...  # omitted for brevity

version = "26"
df = chembl_downloader.query(sql, version=version)
```

## Getting the Newest Version

What about making this code automatically updating to the newest version of ChEMBL? Just use the
`chembl_downloader.latest()` to the latest version up for you. Under the hood, it's using the
[`bioversions`](https://github.com/cthoyt/bioversions) package to do this.

```python
import chembl_downloader

sql = ...  # omitted for brevity

version = chembl_downloader.latest()                       # <-- This line changed for this example
df = chembl_downloader.query(sql, version=version)
```

Doing this is so common, that you can actually just omit the `version` argument
and it will look up the latest for you.

## Meaningful Improvement

I made a [pull request](https://github.com/PatWalters/jcamd_model_comparison/pull/1) to update the notebook
based on these suggestions. The new notebook is [here](https://nbviewer.jupyter.org/github/PatWalters/jcamd_model_comparison/blob/60f1ac2c62a6be957d78c6cf3a570946d714397a/jcamd_model_comparison.ipynb)
and features the most recent version of ChEMBL at the time of writing (ChEMBL 29) instead of ChEMBL 26.
