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

Getting semantic mappings is hard because there are a lot of competing data
models and serialization formats. For example:

1. OWL as a data model can encode semantic mappings in a variety of ways, such
   as using the equivalence (built in) or by using arbitary annotation
   properties (e.g., for skos or OIO)
2. OBO ontology has an `xref` field, a way to add arbitrary anntoation
   properties (e.g., for skos exact match)
3. SSSOM is the best
4. JSKOS, see [previous post]({% post_url 2026-01-15-sssom-to-jskos %})
5. arbitrary RDF that encodes triples, e.g., using skos predicates
6. [Expressive and Declarative Ontology Alignment Language (EDOAL)](https://moex.gitlabpages.inria.fr/alignapi/edoal.html)
7. OntoPortal has its own data model , see [previous
   post]({% post_url 2025-11-23-sssom-from-bioportal %})
8. Wikidata has its own thing going on, see [previous
   post]({% post_url 2026-01-07-sssom-to-wikidata %})
9. a long tail of informal standards in TSV, Excel, etc.

![](/img/mappings-are-hard/formats.png)

### Scattered and partially overlapping

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
