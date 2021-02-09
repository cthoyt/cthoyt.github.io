---
layout: page
title: Research
permalink: /research/
---
My research is focused on the generation and application of biological
knowledge graphs in drug discovery and precision medicine. Recently, I've
had a specific focus on knowledge graph embedding methodologies and downstream
application of link prediction.

<img src="/img/research_workflow.png" alt="Research Workflow"/>

## Biocuration

While there are several useful public terminologies useful for curation of
biomedical relations, there is often the need to develop new controlled
vocabularies, thesauri, taxonomies, and ontologies to support new biological
phenomena. I lead the team that created the [Curation of Neurodegeneration
Supporting Ontology (CONSO)](https://github.com/pharmacome/conso).

After identifying named entities within scholarly articles, their relations can
be extracted and encoded in a knowledge graph. I lead the team that created the
knowledge graph [Curation of Neurodegeneration in BEL (CONIB)](https://github.com/pharmacome/conib)
and later the knowledge graph [TauBase](https://github.com/pharmacome/taubase).

I also lead the same team to re-curate the knowledge graphs curated and
published during the [AETIONOMY](https://www.aetionomy.eu/) project and developed
a novel [rational enrichment workflow](https://github.com/bel-enrichment/bel-enrichment).
Because of the time and cost of curation, prioritization of articles is crucial.
I've developed [semi-automated curation workflows](https://doi.org/10.1093/database/baz068)
based on a new metric for information density in regions of knowledge graphs.

I also serve on the [Biological Expression Language Committee](https://bep.bel.bio) that
facilitates the improvement of the language as a modeling paradigm in systems and networks
biology.

## Data Integration and Harmonization

In order to check the syntax and semantics of these knowledge graphs, I developed
[PyBEL](https://github.com/pybel). To interactively explore these graphs in a
web-based environment and identify biological contractions, I developed
[BEL Commons](https://github.com/bel-commons).

Finally, to integrate all of the rich biological data sources available to the
public, I developed [Bio2BEL](https://github.com/bio2bel). During the process,
I was able to support the [ComPath](https://github.com/compath) project, which
used the Bio2BEL framework to support the curation of equivalencies and hierarchical
relations between entries in several major pathway databases (e.g., KEGG, WikiPathways, Reactome)
and then later in the [PathMe](https://github.com/pathme) project where they were
harmonized in BEL as a common schema.

## Knowledge Graph Embeddings

Knowledge graph embedding methods learn latent representations for the nodes
and edges in a graph to support clustering, link prediction, entity
disambiguation, and other downstream machine learning tasks.

I've worked on [PyKEEN](https://github.com/pykeen/pykeen), a
PyTorch reimplementation of several recent knowledge graph embedding models
with a focus on reproducibility. I've also developed [BioKEEN](https://github.com/smartdataanalytics/biokeen),
which connects biological knowledge graphs in BEL (notably from Bio2BEL)
directly to the PyKEEN pipeline.

## Predictions

The link prediction task in knowledge graphs is isomorphic to several tasks in
drug discovery and precision medicine.

Predicting links between genes/proteins and diseases accomplishes target
identification/prioritization. I've worked on [GuiltyTargets](https://github.com/guiltytargets), 
which embedded proteins from protein-protein interaction networks annotated
with disease-specific differential gene expression patterns. These embeddings
were used for positive-unlabeled learning using disease-specific gene lists.
While this method works well, it was only single-task (only working
on one disease at a time).

Predicting links between chemicals and diseases accomplishes drug repositioning
(in the case when the chemical is a known drug) or otherwise novel drug
discovery. I've worked on [DrugReLink](https://github.com/drugrelink),
which uses [Hetionet](https://het.io) to make these predictions for a given
chemical or disease.

Because many compounds fail in the clinic due to undesirable side effects,
predicting them during early-stage drug discovery could drastically improve
the efficiency. I've worked on [SEffNet](https://github.com/seffnet), which
uses a network composed of drug-disease, drug-side effect, drug-target, and
drug-drug links to predict compounds' side effects and give insight into
the targets mediating those side effects.

Some of my [ongoing work](https://github.com/clepp) is to apply these methods
in precision medicine. I'm doing it by annotating patients as nodes in
networks, and creating edges to biological entities based on clinical
measurements (e.g., gene expression) then embedding those nodes for downstream
machine learning tasks such as subgroup identification and survival analysis.

## Presentations

<ul>
{% for entry in site.data.presentations %}
    <li>
    <a href="{{ entry.url }}">{{ entry.name }}</a>
    at {{ entry.venue }} {% if entry.online %}(online) {% else %}in {{ entry.location.city }}, {{ entry.location.country }}{% endif %} on {{ entry.date.month }} 
    {{ entry.date.day }}, {{ entry.date.year }}
    </li>
{% endfor %}
</ul>

## Publications

My publications are listed in many places, so there's not much good in writing it all again on this site.
Check one of the following:

- [Scholia](https://tools.wmflabs.org/scholia/author/Q47475003)
- [Google Scholar](https://scholar.google.com/citations?user=PjrpzUIAAAAJ)
- [Loop](https://loop.frontiersin.org/people/827476/overview)
- [DBLP](https://dblp.org/pid/199/2168)
