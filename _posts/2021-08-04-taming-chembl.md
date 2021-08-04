---
layout: post
title: How to use ChEMBL Reproducibly
date: 2021-08-04 13:46:00 +0100
author: Charles Tapley Hoyt
tags: cheminformatics, chembl
---
[ChEMBL](https://www.ebi.ac.uk/chembl) is easily the most useful database in a cheminformatician's toolbox, containing
structural and activity information for millions of diverse compounds.

## Getting files reproducibly

In his recent post entitled [Generalized Substructure Search](https://greglandrum.github.io/rdkit-blog/tutorial/substructure/2021/08/03/generalized-substructure-search.html),
Greg Landrum highlighted some new features in RDKit that enable more advanced substructure queries. He began by
loading up ChEMBL like this (edited for clarity):

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

There are two main issues with this code:

1. It relies on a local file path to the ChEMBL data, which means:
    - Nobody else can run this code without editing it.
    - There's no information on how to get or preprocess this file before running the script.
2. It relies on a specific version of ChEMBL, which means that we can't benefit from new compounds in new releases
   without editing it.

To be fair, this is a blog post that's not necessarily supposed to be reused. But what if were so easy to fix this
anti-pattern that there's no excuse not to? Here's how using
the [`chembl_downloader`](https://github.com/cthoyt/chembl_downloader) Python package:

```python
import chembl_downloader

in_path = chembl_downloader.download_sdf(version="29")

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

out_path = "../data/chembl29_sssdata.pkl"
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

With only a single line changed, this code now knows how to download the ChEBML 29 from the source and store it
in a deterministic location on your hard drive. This means that anyone can run it without knowing how to download
ChEMBL themselves, which version to get, how to name the file, or where to put it on their machine. It also implicitly
solves the problem that the user doesn't know if there was any pre-processing done to the file at
`"/home/glandrum/Downloads/chembl_29.sdf.gz"`. Under the hood, it's using the
[`pystow`](https://github.com/cthoyt/pystow) package to pick a deterministic location (`~/.data/chembl/29/`) into
which the file `https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_29/chembl_29.sdf.gz`
is download.

What about making this code automatically updating to the newest version of ChEBML? Just drop `version="29"` and
`chembl_downloader` will look the latest version up for you. Under the hood, it's using the
[`bioversions`](https://github.com/cthoyt/bioversions) package to do this.

```python
import chembl_downloader

in_path = chembl_downloader.download_sdf()

with gzip.open(in_path) as file:
    data = []
    for i, mol in enumerate(rdkit.Chem.ForwardSDMolSupplier(file)):
        ...
        data.append(...)

out_path = "../data/chembl29_sssdata.pkl"
with open(out_path, 'wb') as file:
    pickle.dump(data, file)
```

Now this code is ready to stand the test of time! Just to make sure we save the right artifacts in the right places, I
would also suggest generating file paths in a deterministic way that includes the version number. You can get the latest
version number using `chembl_downloader.latest()`. You can use [`pystow`](https://github.com/cthoyt/pystow)
to pick a deterministic data location

```python
output_path = '../data/chembl29_sssdata.pkl'
pickle.dump(data, open(','
wb + '))

```

## Querying reproducibly

See also: taming drugbank post