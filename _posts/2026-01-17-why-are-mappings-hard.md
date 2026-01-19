---
layout: post
title: Challenges with Semantic Mappings
date: 2026-01-16 11:42:00 +0100
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - knowledge graphs
---

Semantic mappings are hard.

[starting on slide 7](https://docs.google.com/presentation/d/1stuJbkSbvphYs8fYyj6JJX1JzYvxS4_lernmRovIWTU/edit?slide=id.g2bf67b64f65_0_764#slide=id.g2bf67b64f65_0_764)

### Proliferation of Formats

The first major challenge with semantic mappings is the variety of forms they
can take. This both includes different data models and serializations of those
models. Let's start with a lightning review (please let me know if I missed
something):

[Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference)
is a data model for RDF to represent controlled vocabularies, taxonomies,
dictionaries, thesauri, and other semantic artifacts. It defines several
semantic mapping predicates including for broad matches, narrow matches, close
matches, related matches, and exact matches.

[JSKOS (JSON for Knowledge Organization Systems)](https://gbv.github.io/jskos/#mapping),
a JSON-based extension of the SKOS data model. I recently wrote a post about
converting between [SSSOM and JSKOS]({% post_url 2026-01-15-sssom-to-jskos %}).

The [Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-syntax/) is
primarily used for ontologies. It has first-class language support for encoding
equivalences between classes, properties, or individuals. Other semantic
mappings can be encoded as annotation properties on classes, properties, or
individuals, e.g., using SKOS predicates.

The
[OBO Flat File Format](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html)
is a simplified version of OWL with macros most useful for curating biomedical
ontologies. It has the same abilities as OWL, but also the `xref` macro which
corresponds to `oboInOwl:hasDbXref` relations, which are by nature imprecise and
therefore used in a variety of ways.

The
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
is a fit-for-purpose format for semantic mappings between classes, properties,
or individuals. SSSOM guides curators towards inputting key metadata that are
typically missing from other formalisms and is gaining wider community adoption.
Importantly, SSSOM integrates into ontology curation workflows, especially for
[Ontology Development Kit (ODK)](https://incatools.github.io/ontology-development-kit)
users.

The
[Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
lives in a similar space to SSSOM, but IMO was much less approachable (c.f.
XML + Java), and has not seen a lot of traction in the biomedical space.

[OntoPortal](https://ontoportal.org/) has its own data model for semantic
mappings that has low metadata precision. I recently wrote a post on converting
[OntoPortal to SSSOM]({% post_url 2025-11-23-sssom-from-bioportal %})

[Wikidata](https://www.wikidata.org) has its own data model for semantic
mappings that include higher precision metadata. I recently wrote a post on
converting between own thing going on, see [SSSOM and
Wikidata]({% post_url 2026-01-07-sssom-to-wikidata %})

Finally, there's a long tail of mappings that live in poorly annotated CSV, TSV,
Excel, and other formats. Similarly, mappings can live in plain RDF files, e.g.,
encoded with SKOS predicates, but without high precision metadata.

### Scattered and Partially Overlapping

Semantic mappings are not centralized, meaning that multiple sources of semantic
mappings often need to be integrated to fully map between two vocabularies.
Using [Medical Subject Headings (MeSH)](https://semantic.farm/mesh) and the
[Human Phenotype Ontology (HPO)](https://semantic.farm/hpo) as an example, we
can see the following:

1. MeSH doesn't maintain any mappings to HPO
2. HPO maintains some mappings as primary mappings
3. UMLS maintains some mappings as secondary mappings (suggested by HPO)
4. [Biomappings](https://github.com/biopragmatics/biomappings) maintains some
   community-curated mappings as secondary mappings

[![](/img/mappings-are-hard/scattered.png)](https://github.com/biopragmatics/semra/blob/main/notebooks/umls-inference-analysis.ipynb)

This actually might not be the best example - it would have been better to show
a pair of resources that both partially map to the other. When I first made this
chart, I had to engineer the UMLS inference by hand. This led to the development
of the
[Semantic Mapping Reasoner and Assembler (SeMRA)](https://github.com/biopragmatics/semra)
Python package which does this in general and at scale. The fact that there were
missing mappings that even UMLS inference couldn't retrieve led to establishing
the [Biomappings](https://github.com/biopragmatics/biomappings) project for
prediction and semi-automated curation of semantic mappings. The underlying
technology stack from Biomappings eventually got spun out to
[SSSOM Curator](https://github.com/cthoyt/sssom-curator) and is now fully
domain-agnostic.

### Different Precision

[![](/img/mappings-are-hard/precision.svg)](https://docs.google.com/drawings/d/1jBK1-FxzfsBFd6Ro0YjQSvwJCZs1rqlLQq9FdtcEU-w/edit?usp=sharing)

### Different Entity Types

mapping between disease ontologies and phenotype ontologies is questionable

mesh keeps this in its disease hierarchy while HP is a phenotype hierarchy.
there should be a different relationship that isn't a semantic mapping, but more
like "disease presents as" for disease that were historically named after the
phenotype they cause. this can also be just something as simple as incorrect
modeling choices (which I think the MeSH case covers)

mesh:D000069856 Staghorn Calculi skos:exactMatch hp:0033591 Staghorn calculus
semapv:ManualMappingCuration orcid: 0000-0001-9439-5346
generate_hp_mesh_mappings.py

`sssom_curator predict lexical doid hp`

### Different Ontology Philosophy

mapping between different disease ontologies is hard because of arguments about
what kind of BFO thing a disease is (disposition, quality, etc.)

### Different Kinds of Evidence

[![](/img/mappings-are-hard/evidence.svg)](https://docs.google.com/drawings/d/1rBofcaQxBFuYX0OzhCvBkigSNFWLclAbQ_X7zG7PRKA/edit?usp=sharing)

We developed the
[Semantic Mapping Vocabulary (semapv)](https://semantic.farm/registry/semapv) to
encode different kinds of evidence such as for manual curation of mappings,
lexical matching, structural matching, and others. The
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom/)
is well-suited towards capturing simple evidences (blue), but the purple one
requires a more detailed metadata model that I proposed in
[Assembly and reasoning over semantic mappings at scale for biomedical data integration](https://doi.org/10.1093/bioinformatics/btaf542)
and implemented in the
[Semantic Reasoning Mapper and Reasoner (SeMRA)](https://github.com/biopragmatics/semra)
Python software package.

### Inexact or Negative

TODO link to negative RDF post

[![](/img/mappings-are-hard/negatives.svg)](https://docs.google.com/drawings/d/1AfCR35ra3FyQMulaTlynVZKswLbj8gp5MA4N2ipFe1I/edit?usp=sharing)

[previous post on negative RDF]({% post_url 2025-10-09-negative-rdf %})

negative mappings are crucial during inference and curation to avoid duplicated
work [zombie mappings](https://doi.org/10.32388/DYZ5J3).

though we didn't get good results in the first applications of graph machine
learning for semantic mapping prediction, negative mappings are key for training
machine learning models and making more realistic/useful evaluations.

### The Need for Inference

linguists get really tripped up here. mapping of logical definition -> use OWL
exact match mapping of meaning -> use SKOS, even if definitions/labels don't
really match, this can be chalked up to imprecision of language.

Here are three different vocabularies' terms for _protein_ and their
definitions. Even though we know that the intent was to represent the same
thing, the definitions are not exactly compatible. This means as a semantic
mapping curator, we have two options: we can either use our prior knowledge that
we know what a protein is, and this is the way they decided to represent it, or
we can take the definition very, very seriously and say that these are mutually
incompatible. I think that the latter is really unconstructive, since this
effectively means you won't ever be able to map anything. If you want to go down
the second route to decide if things are then same, rather than relying on human
language, ontologies provide the ability to make logical definitions. For
example, the cell ontology (CL) does this really well. However, this also has a
caveat, that to make mappings based on logical definitions, then the different
modelers have to agree on the same modeling paradigm. As far as I know, there
aren't any groups out there that use the same modeling paradigm that haven't
just combine forces to work on the same resource. So we're stuck back at option
1 either way.

| Entity                                                       | Description                                                                                                                                             |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [wikidata:Q8054](https://www.wikidata.org/wiki/Q8054)        | biomolecule or biomolecule complex largely consisting of chains of amino acid residues                                                                  |
| [SIO:010043](http://semanticscience.org/resource/SIO_010043) | A protein is an organic polymer that is composed of one or more linear polymers of amino acids.                                                         |
| [PR:000000001](http://purl.obolibrary.org/obo/PR_000000001)  | An amino acid chain that is canonically produced _de novo_ by ribosome-mediated translation of a genetically-encoded mRNA, and any derivatives thereof. |

### Upper Level Hierarchy Issues

The [basic formal ontology (BFO)](https://basic-formal-ontology.org) is an
upper-level ontology that is used by many ontologies, including almost the
entire [Open Biomedical Ontologies (OBO) Foundry](https://obofoundry.org).
However, as Chris Mungall described in his blog post,
[Shadow Concepts Considered Harmful](https://douroucouli.wordpress.com/2022/08/10/shadow-concepts-considered-harmful/),
there are many different senses in which an entity can be described, each
falling under a different, mutually exclusive branch of BFO. The figure below,
from Chris's post, represents different senses in which a human heart can be
described:

[![](/img/mappings-are-hard/mungalls-ontology-design-guidelines-12.png)](https://douroucouli.wordpress.com/2022/08/10/shadow-concepts-considered-harmful/)

This problem is particularly bad in disease modeling. Here are only a few
examples (of many more) that illustrate this:

- the [Ontology for General Medical Science [OGMS]](https://semantic.farm/ogms)
  term for
  [disease (OGMS:0000031)](http://purl.obolibrary.org/obo/OGMS_0000031), the
  [Experimental Factor Ontology (EFO)](https://semantic.farm/efo) term for
  [disease (EFO:0000408)](http://www.ebi.ac.uk/efo/EFO_0000408),
  [Monarch Disease Ontology (MONDO)](https://semantic.farm/mondo) term for
  [disease (MONDO:0000001)](http://purl.obolibrary.org/obo/MONDO_0000001) is a
  [disposition (BFO:0000016)](http://purl.obolibrary.org/obo/BFO_0000016)
- the
  [Gender, Sex, and Sexual Orientation Ontology (GSSO)](https://semantic.farm/gsso)
  term for [disease (GSSO:000486)](http://purl.obolibrary.org/obo/GSSO_000486)
  is a [process (BFO:0000015)](http://purl.obolibrary.org/obo/BFO_0000015)
- the [Human Disease Ontology (DOID)](https://semantic.farm/doid) informally
  mentions that a disease is a disposition, but doesn't make an ontological
  commitment to BFO
- many more controlled vocabularies including NCIT, SNOMED-CT, and MI have their
  own terms for diseases but don't use BFO as an upper-level ontology nor are
  constructed in a way conducive towards integration with other ontologies

[Scalable representations of diseases in biomedical ontologies](https://link.springer.com/article/10.1186/2041-1480-2-S2-S6)
by Schultz _et al._ (2011)

https://github.com/OBOFoundry/COB/pull/226

because the different parts of the BFO upper level are marked as disjoint, a
reasoner will explode if you try and use terms that are in different parts of
the hierarchy interchangably. However. This modeling choice is not
useful/important in many downstream applications, like assembling a knowledge
graph, where mapping and consolidating informtation that might have MONDO

### Context-dependent interpretation

A gene is a region of a chromosome that encodes a transcript.

[SO:0000704](http://purl.obolibrary.org/obo/SO_0000704) A protein is a chain of
amino acids

[PR:000000001](http://purl.obolibrary.org/obo/PR_000000001)

Genes represent a combination of the physical region on a chromosome and the
information contained within

When assembling mechanistic biological knowledge into pathways.

Some mappings may be context-dependent. For example, many knowledge graphs
simplify the complexities of the central dogma of biology and consider genes and
gene products (such as proteins) to be equivalent. However,

![](/img/mappings-are-hard/context-dependent.svg)
