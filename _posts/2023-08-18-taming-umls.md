---
layout: post
title: Unlocking UMLS
date: 2023-08-18 00:00:00 -0800
author: Charles Tapley Hoyt
tags:
  - umls
  - reproducibility
---

The [Unified Medical Language System (UMLS)](https://www.nlm.nih.gov/research/umls)
is a widely used biomedical and clinical vocabulary maintained by the United States
National Library of Medicine. However, it is notoriously difficult to access and work
with its source data due to licensing restrictions and a complicated download system.
In the same vein as previous posts about [DrugBank]({% post_url 2020-12-14-taming-drugbank %}) and
[ChEMBL]({% post_url 2021-08-05-taming-chembl-sql %}), this post
describes [software](https://github.com/cthoyt/umls_downloader) and a workflow
I've developed for getting and working with this data. It also works
for [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html),
[SemMedDB](https://lhncbc.nlm.nih.gov/ii/tools/SemRep_SemMedDB_SKR/SemMedDB_download.html), [SNOMED-CT](https://www.nlm.nih.gov/healthit/snomedct/international.html),
and any other data accessible through
the [UMLS Terminology Services (UTS) ticket granting system](https://documentation.uts.nlm.nih.gov/automating-downloads.html).

The first big issue with the UMLS is its licensing. Here's an excerpt from the
[How to License and Access the Unified Medical Language System® (UMLS®) Data](https://www.nlm.nih.gov/databases/umls.html)
page accessed on August 28<sup>th</sup>, 2023:

> 1. Please sign up for a new UMLS Terminology Services (UTS) account with your preferred identity provider at the UTS
     homepage.
> 2. Complete and submit the license request form. NLM will send the license approval e-mail within 5 business days
     after reviewing your authenticated license request.
> 3. You will sign in using identity provider credentials to download files or access web interfaces that require UTS
     authentication such as the UTS, VSAC, SNOMED CT, or RxNorm.

These are three big hurdles. We typically expect scientific data to be available to download without login. Second,
we expect it to be available under a well-defined, standard licenses like ones
from [Creative Commons](https://creativecommons.org/)
such as [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
or [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Third, we expect downloading to be simple, such
as clicking a single link. UMLS subverts all of these expectations. Even more bizarre (iirc), part of the terms and
conditions says that you have to fill out a user survey each year to keep your account and access. This is all a big
bummer, even worse compounded by the fact that this is created with taxpayer money at a government organization.

## How To Break Free



Don't worry about [UMLS Terminology Services (UTS)](https://uts.nlm.nih.gov/uts/)
licensing and distribution rules - just use
`umls_downloader` to write code that knows how to download content and use it
automatically from the following (non-exhaustive) list of resources:

- [UMLS](https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html)
- [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html)
- [SemMedDB](https://lhncbc.nlm.nih.gov/ii/tools/SemRep_SemMedDB_SKR/SemMedDB_download.html)
- [SNOMED-CT](https://www.nlm.nih.gov/healthit/snomedct/international.html)
- potentially more in the future

or any content that can be downloaded through
the [UTS ticket granting](https://documentation.uts.nlm.nih.gov/automating-downloads.html)
system. There's no centralized list of content available through the UTS so
suggestions for additional resources are welcome through
the [issue tracker](https://github.com/cthoyt/umls_downloader/issues).

Full documentation are available at [umls-downloader.readthedocs.io](https://umls-downloader.readthedocs.io).

## Installation

```bash
$ pip install umls_downloader
```

## Download A Specific Version of UMLS

```python
import os
from umls_downloader import download_umls

# Get this from https://uts.nlm.nih.gov/uts/edit-profile
api_key = ...

path = download_umls(version="2021AB", api_key=api_key)

# This is where it gets downloaded: ~/.data/bio/umls/2021AB/umls-2021AB-mrconso.zip
expected_path = os.path.join(
    os.path.expanduser("~"), ".data", "umls", "2021AB",
    "umls-2021AB-mrconso.zip",
)
assert expected_path == path.as_posix()
```

After it's been downloaded once, it's smart and doesn't need to download again.
It gets stored using [`pystow`](https://github.com/cthoyt/pystow) automatically
in the `~/.data/bio/umls` directory.

A full list of functions is available in the
[documentation](https://umls-downloader.readthedocs.io).

## Automating Configuration of UTS Credentials

There are two ways to automatically set the username and password so you don't
have to worry about getting it and passing it around in your python code:

1. Set `UMLS_API_KEY` in the environment
2. Create `~/.config/umls.ini` and set in the `[umls]` section a `api_key` key.

```python
from umls_downloader import download_umls

# Same path as before
path = download_umls(version="2021AB")
```

## Download the Latest Version

First, you'll have to
install [`bioversions`](https://github.com/cthoyt/bioversions)
with `pip install bioversions`, whose job it is to look up the latest version of
many databases. Then, you can modify the previous code slightly by omitting
the `version` keyword argument:

```python
from umls_downloader import download_umls

# Same path as before (as of November 21st, 2021)
path = download_umls()
```

## Download and open the file

The UMLS file is zipped, so it's usually accompanied with the following
boilerplate code:

```python
import zipfile
from umls_downloader import download_umls

path = download_umls()
with zipfile.ZipFile(path) as zip_file:
    with zip_file.open("MRCONSO.RRF", mode="r") as file:
        for line in file:
            ...
```

This exact code is wrapped with the `open_umls()` using Python's context manager
so it can more simply be written as:

```python
from umls_downloader import open_umls

with open_umls() as file:
    for line in file:
        ...
```

The `version` and `api_key` arguments also apply here.

## Why not an API?

The UMLS provides an [API](https://documentation.uts.nlm.nih.gov/rest/home.html)
for access to tiny bits of data at a time. There are even two recent (last 5
years) packages [`umls-api`](https://pypi.org/project/umls-api)
[`connect-umls`](https://pypi.org/project/connect-umls) that provide a wrapper
around them. However, API access is generally rate limited, difficult to use in
bulk, and slow. For working with UMLS (or any other database, for that matter)in
bulk, it's necessary to download full database dumps.

## UMLS Mappings

One of the nice qualities of UMLS is it is a mapping hub. It provides mostly complete mappings
between many vocabularies including MeSH, NCIT, SNOMED-CT, HPO, LOINC, and more.

Because I've spent a lot of time automating the ingestion of UMLS in a generic way, I have also
used the PyOBO package to write a more fit-for-purpose wrapper in processing its content to generate
ontologies (as OBO, OWL, or OBO Graph JSON) and mappings files (as SSSOM).
https://github.com/pyobo/pyobo/commit/be67eadf77afa270cf224cad71d5b1905ae78b53


```python
import pyobo

df = pyobo.get_sssom_df("umls")
df.to_csv("umls.sssom.tsv", sep="\t", index=False)
```

SSSOM is ...

For example, if you want to get UMLS as an SSSOM dataframe, you can do

```python
import pyobo

df = pyobo.get_sssom_df("umls")
df.to_csv("umls.sssom.tsv", sep="\t", index=False)
```

If you don't want to get all of the many resources required to add
names, you can pass ``names=False``

```python
import pyobo

df = pyobo.get_sssom_df("umls", names=False)
df.to_csv("umls.sssom.tsv", sep="\t", index=False)
```
