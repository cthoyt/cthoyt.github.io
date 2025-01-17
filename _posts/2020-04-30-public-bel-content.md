---
layout: post
title:
  A Listing of Publicly Available Content in the Biological Expression Language
  (BEL)
date: 2020-04-30 17:50:00 +0100
author: Charles Tapley Hoyt
tags: bel pybel
---

While many researchers have a pathway or pathology of interest, their first time
curating content in the Biological Expression Language (BEL) may seem
intimidating. This post lists several disease maps and BEL content sources that
are directly available for re-use.

## Manually Curated BEL

The [bel-repository](https://github.com/pybel/bel-repository) Python package has
the job of taking BEL content that lives in a GitHub repository and making it
easy to share with other people. It leverages `pybel` and `tox` to pre-compile
BEL content and provide summaries that are auto-hosted by GitHub (when
configured properly). The following is a short but growing list of some
resources that are available through GitHub.

### Selventa Large + Small Corpora [![DOI](https://zenodo.org/badge/199500332.svg)](https://zenodo.org/badge/latestdoi/199500332)

Along with their release of the OpenBEL Framework in 2012, Selventa published
two files
[to GitHub](https://github.com/OpenBEL/openbel-framework-resources/tree/latest/knowledge)
that showcased the range of biological phenomena that could be expressed in BEL
with a slight focus on atherosclerosis. They were excitingly named the "Selventa
Small Corpus" and "Selventa Large Corpus".

Because Selventa dissolved in 2016 and the belframework.org domain expired in
mid-2019, the files have been updated and redistributed on GitHub at
[cthoyt/selventa-knowledge](https://github.com/cthoyt/selventa-knowledge) under
the Creative Commons Attribution-Non-Commercial-ShareAlike 3.0 Unported License,
same as the original. It can be installed in Python directly with:

```bash
pip install git+https://github.com/cthoyt/selventa-knowledge.git
selventa-knowledge summarize
```

It can be used in Python as a PyBEL
[BEL graph](https://pybel.readthedocs.io/en/latest/reference/struct/datamodel.html#pybel.BELGraph)
with:

```python
import selventa_knowledge
selventa_graph = selventa_knowledge.get_graph()
selventa_graph.summarize()
```

### EpiCom [![DOI](https://zenodo.org/badge/189166127.svg)](https://zenodo.org/badge/latestdoi/189166127)

This knowledge graph describes putative mechanisms involved in the pathogenesis
of Epilepsy. It was published by Hoyt and Domingo-Fernández _et al._ (2018) in
[A systematic approach for identifying shared mechanisms in epilepsy and its comorbidities](https://doi.org/10.1093/database/bay050).

It is available on GitHub under
[neurommsig-epilepsy/neurommsig-epilepsy](https://github.com/neurommsig-epilepsy/neurommsig-epilepsy)
or can be installed directly with Python using:

```bash
pip install neurommsig-epilepsy
neurommsig-epilepsy summarize
```

After installation, it can be directly used with PyBEL like:

```python
import neurommsig_epilepsy
epilepsy_graph = neurommsig_epilepsy.get_graph()
epilepsy_graph.summarize()
```

### CONIB [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3385895.svg)](https://doi.org/10.5281/zenodo.3385895)

The Curation of Neurodegeneration in BEL (CONIB) encodes biological phenomena
related to tauopathies in the context of neurodegeneration.

It is available on GitHub under
[pharmacome/conib](https://github.com/pharmacome/conib) or can be installed
directly with Python using:

```bash
pip install git+https://github.com/pharmacome/conib.git
conib summarize
```

After installation, it can be directly used with PyBEL like:

```python
import conib
conib_graph = conib.get_graph()
conib_graph.summarize()
```

### HemeKG [![DOI](https://zenodo.org/badge/202482655.svg)](https://zenodo.org/badge/latestdoi/202482655)

The Heme Knowledge Graph (HemeKG) encodes heme pathogenicity and pathway
dysregulation in the context of hemolytic disorders. It was published by Humayun
_et al._ in
[A computational approach for mapping heme biology in the context of hemolytic disorders](https://doi.org/10.3389/fbioe.2020.00074).

It is available on GitHub under
[hemekg/hemekg](https://github.com/hemekg/hemekg) or can be installed directly
with Python using:

```bash
pip install hemekg
hemekg summarize
```

After installation, it can be directly used with PyBEL like:

```python
import hemekg
heme_graph = hemekg.get_graph()
heme_graph.summarize()
```

### COVID-19 Knowledge Graph [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3748950.svg)](https://doi.org/10.5281/zenodo.3748950)

The COVID-19 Knowledge graph encodes biology surrounding the infection of the
novel coronavirus. It was published by Domingo-Fernández _et al._ in
[ COVID-19 Knowledge Graph: a computable, multi-modal, cause-and-effect knowledge model of COVID-19 pathophysiology](https://doi.org/10.1101/2020.04.14.040667).

It is available on GitHub under
[covid19kg/covid19kg](https://github.com/covid19kg/covid19kg) or can be
installed directly with Python using:

```bash
pip install git+https://github.com/covid19kg/covid19kg.git
covid19kg summarize
```

After installation, it can be directly used with PyBEL like:

```python
import covid19kg
covid19_graph = covid19kg.get_graph()
covid19_graph.summarize()
```

## Bio2BEL

The [Bio2BEL](https://github.com/bio2bel/bio2bel) ecosystem is built on top of
PyBEL to convert as many reasonable structured data sources as possible into
BEL, automatically. A
[list of most of the available repositories](https://bio2bel.readthedocs.io/en/latest/repositories.html)
is available in the documentation. A few notable examples are included here.
Notably, metadatabases like Pathway Commons will not be supported by Bio2BEL,
because it's almost always better to get the source data which is much higher
granular. A
[pre-print](https://www.biorxiv.org/content/biorxiv/early/2019/05/08/631812.full.pdf)
describing the Bio2BEL philosophy and summarizing the content in it is available
on _bioRxiv_.

### Causal Biological Networks Database

The [Causal Biological Networks database](http://causalbionet.com/) provides a
swath of ground-truth biology. It has human, rat, and mouse networks that can be
downloaded from the main page in a bespoke (and undocumented) JGF variant.
Luckily, an importer can be found in the
[PyBEL documentation](https://pybel.readthedocs.io/en/latest/reference/io.html?highlight=CBN#pybel.from_cbn_jgif_file)
with instructions for unzipping the downloads and loading them into PyBEL with
`pybel.from_cbn_jgif_file()`.

The content has also been pre-processed and is available at
[https://github.com/pybel/cbn-bel](https://github.com/pybel/cbn-bel)

### Hetionet

Hetionet is a large biomedical knowledge graphs created for drug repositioning.

> [Systematic integration of biomedical knowledge prioritizes drugs for repurposing](https://doi.org/10.7554/eLife.26726)
> Daniel S Himmelstein, Antoine Lizee, Christine Hessler, Leo Brueggeman,
> Sabrina L Chen, Dexter Hadley, Ari Green, Pouya Khankhanian, Sergio E
> Baranzini _eLife_ (2017-09-22) DOI: `10.7554/eLife.26726`

An export of Hetionet as BEL can be found at
[https://github.com/pybel/hetionet-bel](https://github.com/pybel/hetionet-bel).

### OpenBioLink [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3834052.svg)](https://doi.org/10.5281/zenodo.3834052)

OpenBioLink is a framework that produces biomedical knowledge graphs for link
prediction.

> [OpenBioLink: A benchmarking framework for large-scale biomedical link prediction](https://doi.org/10.1093/bioinformatics/btaa274)
> Breit, A., Ott, S., Agibetov, A., & Samwald, M. _Bioinformatics_ (2020) DOI:
> `10.1093/bioinformatics/btaa274`

### KEGG, WikiPathways, and Reactome

The [PathMe](https://github.com/PathwayMerger) package converts KEGG, Reactome,
and WikiPathways to BEL. Results may vary, because the variety of XML, BioPAX,
and GPML/RDF used by the source databases changes all of the time, but this is a
trove of content from other manual curation efforts. It was published by
Domingo-Fernández _et al_ in
[_BMC Bioinformatics_](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-019-2863-9).

## Leaving the PyBEL Ecosystem

While each repository distributes the source BEL scripts along with pre-compiled
BEL JSON for easy use with PyBEL, some users may want to convert the content for
other purposes. For example, you may want to upload it to one of many services
that PyBEL interacts with.

### Upload to BEL Commons

BEL Commons is a free, open-source platform for hosting BEL content. It includes
the ability to interactively explore nodes, edges, and networks along with their
associated metadata as well as enrich them with content from Bio2BEL.

> **Warning** BEL Commons was originally developed and published in an academic
> capacity at Fraunhofer. While they hosted a
> [public instance](https://bel-commons-dev.scai.fraunhofer.de) to support its
> original publication, it was permanently shut down in 2020.

```python
import covid19kg
graph = covid19kg.get_graph()

import pybel
pybel.to_bel_commons(graph, host='...', user='...', password='...')
```

If you would like to host your own instance of BEL Commons, it can be downloaded
from GitHub
([bel-commons/bel-commons](https://github.com/bel-commons/bel-commons)) and
hosted easily with Docker. If you are hosting your own instance, all you have to
do is use the `host` keyword. See the
[pybel.to_bel_commons()](https://pybel.readthedocs.io/en/latest/reference/io.html#module-pybel.io.bel_commons_client)
documentation.

### Upload to BioDati Studio

> **Warning** After a relatively short stint, BioDati was shut down some time in
> 2021, likely coinciding with the departure of William Hayes to go to Sage
> Therapeutics. Therefore, this section corresponds to infrastructure that no
> longer exists, but it will remain in this post for posterity.

BioDati is a paid, closed-source platform for hosting BEL content. However, they
do have a demo instance running at https://studio.demo.biodati.com with which
the examples in this module will be described.

```python
import covid19kg
graph = covid19kg.get_graph()

import pybel
pybel.to_biodati(graph, host='https://nanopubstore.demo.biodati.com', user='...', password='...')
```

More information on uploading to BioDati can be found in the documentation of
[pybel.to_biodati()](https://pybel.readthedocs.io/en/latest/reference/io.html#module-pybel.io.biodati_client).

### Conversion to INDRA

INDRA is an excellent suite for automated model assembly developed in the
Laboratory of Systems Pharmacology at Harvard Medical School. PyBEL can convert
content to INDRA with the following code:

```python
import covid19kg
graph = covid19kg.get_graph()

import pybel
statements = pybel.to_indra_statements(graph)
```

---

PyBEL has tons of other I/O formats, especially for analytical tools like
[HiPathia](http://hipathia.babelomics.org),
[SPIA](https://bioconductor.org/packages/release/bioc/html/SPIA.html),
[PyKEEN](https://github.com/pykeen/pykeen), and others that aren't mentioned
here, but can be found in its documentation
[here](https://pybel.readthedocs.io/en/latest/reference/io.html).

I hope you're able to find some of this content useful! If you know about any
other publicly available BEL content, please let me know, so I can update this
post. All of my contact info is below. Or make a
[pull request against this page](https://github.com/cthoyt/cthoyt.github.io/edit/master/_posts/2020-04-30-public-bel-content.md)
directly.
