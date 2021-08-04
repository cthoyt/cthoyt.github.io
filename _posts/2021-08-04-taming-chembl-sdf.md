---
layout: post
title: Loading ChEMBL SDF Data Reproducibly
date: 2021-08-04 13:46:00 +0100
author: Charles Tapley Hoyt
tags: cheminformatics chembl
---
[ChEMBL](https://www.ebi.ac.uk/chembl) is easily the most useful database in a cheminformatician's toolbox, containing
structural and activity information for millions of diverse compounds.
In his recent blog post, [Generalized Substructure Search](https://greglandrum.github.io/rdkit-blog/tutorial/substructure/2021/08/03/generalized-substructure-search.html),
Greg Landrum highlighted some new RDKit features that enable more advanced substructure queries. It
started by loading molecules from the ChEMBL 29 SDF dump, but it featured a common issue that hampers reproducibility:
a hard-coded local file path to the ChEMBL data. This blog post is how to address this using
[`chembl_downloader`](https://github.com/cthoyt/chembl-downloader) and make code using ChEMBL's
SDF dump more reusable and reproducible.

## Getting Data Reproducibly

The code in the blog post began by loading up ChEMBL 29 like this (edited for clarity and imports omitted for brevity):

```python
in_path = "/home/glandrum/Downloads/chembl_29.sdf.gz"

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

out_path = "../data/chembl29_sssdata.pkl"
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

There are three main issues with this code:

1. It relies on a local file path to the ChEMBL data, which means:
    - Nobody else can run this code without editing it.
    - There's no information on how to get or preprocess this file before running the script.
2. It relies on a specific version of ChEMBL, which means that we can't benefit from new compounds in new releases
   without editing it.
3. It outputs data to a relative file path, which might not work based on the way the script is run or the directory
   structure on your drive

To be fair, this is a blog post that's not necessarily supposed to be reused. But what if were so easy to fix this
anti-pattern that there's no excuse not to? Here's how using
the [`chembl_downloader`](https://github.com/cthoyt/chembl-downloader) Python package:

```python
import chembl_downloader

version = "29"                                             # <-- This line changed for this example
in_path = chembl_downloader.download_sdf(version=version)  # <-- This line changed for this example

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

out_path = "../data/chembl29_sssdata.pkl"
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

With only a single line changed, this code now knows how to download the ChEMBL 29 from the source and store it in a
deterministic location on your hard drive. This means that anyone can run it without knowing how to download ChEMBL
themselves, which version to get, how to name the file, or where to put it on their machine. It also implicitly solves
the problem that the user doesn't know if there was any pre-processing done to the file at
`"/home/glandrum/Downloads/chembl_29.sdf.gz"`. Under the hood, it's using the
[`pystow`](https://github.com/cthoyt/pystow) package to determinisically pick a folder (`~/.data/chembl/29/`) into which
the file `ftp://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_29/chembl_29.sdf.gz`
is download (`~/.data/chembl/29/chembl_29.sdf.gz`).

## Getting the Newest Version

What about making this code automatically updating to the newest version of ChEMBL? Just use the
`chembl_downloader.latest()` to the latest version up for you. Under the hood, it's using the
[`bioversions`](https://github.com/cthoyt/bioversions) package to do this.

```python
import chembl_downloader

version = chembl_downloader.latest()                       # <-- This line changed for this example
in_path = chembl_downloader.download_sdf(version=version)

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

out_path = "../data/chembl29_sssdata.pkl"
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

Note, if you omit the `version` argument completely, it automatically looks up the version as well. However, there's one
more thing to update before we've addressed our third point: where the file is output. There are two goals in fixing the
output:

1. Make the path deterministic
2. Make the path based on the version of ChEMBL that's being used, so if a newer version gets used, it doesn't delete
   the old file

The solution comes by using `pystow` to pick a deterministic path, which the `download_sdf()` function is actually
using under the hood, too:

```python
import chembl_downloader

version = chembl_downloader.latest()
in_path = chembl_downloader.download_sdf(version=version)

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

import pystow                                                  # <-- This line changed for this example
out_path = pystow.join("chembl", version, name="sssdata.pkl")  # <-- This line changed for this example
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

The `pystow.join` method creates a path to `~/.data/chembl/<version>/sssdata.pkl`.
Now this code is ready to stand the test of time and a variety of different uses!

## Coda

Because the pattern of getting the SDF from ChEMBL then opening it with a `ForwardSDMolSupplier` is so common,
it's actually included in its own function `supplier()`. The code could be compressed one more time like:

```python
import chembl_downloader

version = chembl_downloader.latest()

with chembl_downloader.supplier(version=version) as suppl:
    data = []
    for i, mol in enumerate(suppl):
        ...
        data.append(...)

import pystow

out_path = pystow.join("chembl", version, name="sssdata.pkl")
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```
