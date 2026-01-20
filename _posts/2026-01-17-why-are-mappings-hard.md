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

This post is a mega dump on what makes semantic mappings hard, both on a
technical, philosophical, and practical level.

[starting on slide 7](https://docs.google.com/presentation/d/1stuJbkSbvphYs8fYyj6JJX1JzYvxS4_lernmRovIWTU/edit?slide=id.g2bf67b64f65_0_764#slide=id.g2bf67b64f65_0_764)

### Proliferation of Formats

The first major challenge with semantic mappings is the variety of forms they
can take. This both includes different data models and serializations of those
models. Let's start with a lightning review (please let me know if I missed
something):

<img src="https://forge.extranet.logilab.fr/uploads/-/system/project/avatar/107/external-content.duckduckgo.com.jpeg" align="left" style="max-height: 3em;" alt="SKOS logo"/>
[Simple Knowledge Organization System (SKOS)](https://www.w3.org/TR/skos-reference)
is a data model for RDF to represent controlled vocabularies, taxonomies,
dictionaries, thesauri, and other semantic artifacts. It defines several
semantic mapping predicates including for broad matches, narrow matches, close
matches, related matches, and exact matches.

[JSKOS (JSON for Knowledge Organization Systems)](https://gbv.github.io/jskos/#mapping),
a JSON-based extension of the SKOS data model. I recently wrote a post about
converting between [SSSOM and JSKOS]({% post_url 2026-01-15-sssom-to-jskos %}).

<img src="https://www.jean-delahousse.net/wp-content/uploads/2020/09/Owl_logo-258x300.png"  align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OWL logo">
[Web Ontology Language (OWL)](https://www.w3.org/TR/owl2-syntax/) is primarily
used for ontologies. It has first-class language support for encoding
equivalences between classes, properties, or individuals. Other semantic
mappings can be encoded as annotation properties on classes, properties, or
individuals, e.g., using SKOS predicates.

<img src="https://obofoundry.org/images/foundrylogo.png"  align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OBO logo">
The
[OBO Flat File Format](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html)
is a simplified version of OWL with macros most useful for curating biomedical
ontologies. It has the same abilities as OWL, but also the `xref` macro which
corresponds to `oboInOwl:hasDbXref` relations, which are by nature imprecise and
therefore used in a variety of ways.

<img src="https://avatars.githubusercontent.com/u/77892844?v=4" align="left" style="max-height: 3em; margin-right: 0.5em;" alt="SSSOM logo">
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

<img src="https://ontoportal.org/images/logo.png" align="left" style="max-height: 3em; margin-right: 0.5em;" alt="OntoPortal logo"/>
[OntoPortal](https://ontoportal.org/) has its own data model for semantic
mappings that has low metadata precision. I recently wrote a post on converting
[OntoPortal to SSSOM]({% post_url 2025-11-23-sssom-from-bioportal %}). OntoPortal would also like
to invest more in SSSOM infrastructure if it can organize funding and human resources.

<img src="https://upload.wikimedia.org/wikipedia/commons/6/66/Wikidata-logo-en.svg" align="left" style="max-height: 3em" alt="Wikidata logo">
[Wikidata](https://www.wikidata.org) has its own data model for semantic
mappings that include higher precision metadata. I recently wrote a post on
mapping between the data models from [SSSOM and
Wikidata]({% post_url 2026-01-07-sssom-to-wikidata %}).

Finally, there's a long tail of mappings that live in poorly annotated CSV, TSV,
Excel, and other formats. Similarly, mappings can live in plain RDF files, e.g.,
encoded with SKOS predicates, but without high precision metadata.

### Scattered, Partially Overlapping, and Incomplete

Semantic mappings are not centralized, meaning that multiple sources of semantic
mappings often need to be integrated to map between two semantic spaces. Even
then, these integrated mappings are often incomplete. Using
[Medical Subject Headings (MeSH)](https://semantic.farm/mesh) and the
[Human Phenotype Ontology (HPO)](https://semantic.farm/hpo) as an example, we
can see the following:

1. MeSH doesn't maintain any mappings to HPO.
2. HPO maintains some mappings as primary mappings.
3. The [Unified Medical Language System (UMLS)](https://semantic.farm/umls)
   maintains some mappings as secondary mappings. HPO suggests using UMLS as a
   supplementary mapping resource.
4. [Biomappings](https://github.com/biopragmatics/biomappings) maintains some
   community-curated mappings as secondary mappings.

[![](/img/mappings-are-hard/scattered.png)](https://github.com/biopragmatics/semra/blob/main/notebooks/umls-inference-analysis.ipynb)

This actually might not be the best example - it would have been better to show
a pair of resources that both partially map to the other. When I first made this
chart, I had to engineer the UMLS inference by hand. Eventually, the need to
generalize this workflow led to the development of the
[Semantic Mapping Reasoner and Assembler (SeMRA)](https://github.com/biopragmatics/semra)
Python package which does this automatically and at scale. The fact that there
were missing mappings that even UMLS inference couldn't retrieve led to
establishing the [Biomappings](https://github.com/biopragmatics/biomappings)
project for prediction and semi-automated curation of semantic mappings. The
underlying technology stack from Biomappings eventually got spun out to
[SSSOM Curator](https://github.com/cthoyt/sssom-curator) and is now fully
domain-agnostic.

### Different Precision or Conflicts

Another challenge with semantic mappings is when different resources have
different level of precision. In the example below, OrphaNet uses low-precision
mapping predicates (i.e., `oboInOwl:hasDbXref`) while MONDO uses high-precision
mapping predicates (i.e., `skos:exactMatch`). It makes sense to take the highest
quality mapping in this situation, but having a coherent software stack to do
this at scale was the big challenge (solved by SeMRA).

[![](/img/mappings-are-hard/precision.svg)](https://docs.google.com/drawings/d/1jBK1-FxzfsBFd6Ro0YjQSvwJCZs1rqlLQq9FdtcEU-w/edit?usp=sharing)

This can get a bit dicier when there might be conflicting information, for
example, if one resource says exact match and another says broader match. In
SeMRA, I devised a confidence assessment scheme (which should get its own post
later).

### Common Conflations

There are three flavors of conflations that make curating and reviewing mappings
difficult that I want to highlight.

#### Different Ontology Encodings

Classes, instances, and properties are mutually exclusive by design. This means
that any semantic mappings between them are nonsense, but there are many
situations where these mappings might get produced by an automated system or by
a curator who is less knowledgable about the ontology aspect of semantic
mappings. There's also a much more subtle discussion about classes, instances,
and metaclasses ( see
[this discussion](https://github.com/OBOFoundry/OBOFoundry.github.io/issues/2454))
that I would set aside.

As a concrete example, the
[Information Artifact Ontology (IAO)](https://semantic.farm/registry/iao) has a
class that represents the section of a document that contains its abstract:
[abstract (IAO:0000315)](http://purl.obolibrary.org/obo/IAO_0000315). Schema.org
has an annotation property whose range is a creative work and whose domain is
the text of the abstract itself: [schema:abstract](http://schema.org/abstract).
These both have the same label `abstract`, which means that it's possible to
conflate (i.e., accidentally map them).

#### Different Entity Types

The second kind of conflation is even more subtle, when two classes, instances,
or properties come from similar but distinct hierarchies.

For example, there's a subtle difference between what is a phenotype and what is
a disease. Ontologies are highly apt at encoding this subtlety with _axioms_
that can then be used by reasoners. This can become a problem for curating and
reviewing semantic mappings because some diseases are named after the phenotype
that it presents or that causes it. Using MeSH's disease hierarchy and HPO's
phenotype hierarchy as an example, we can see that
[Staghorn Calculi (mesh:D000069856)](https://semantic.farm/mesh:D000069856) and
[Staghorn calculus (HP:0033591)](https://semantic.farm/hp:0033591) should not
get mapped.

Many more examples can be produced (which also show there are even more
subtleties here) using SSSOM Curator with the command:
`sssom_curator predict lexical doid hp`. See the
[SSSOM Curator documentation](https://sssom-curator.readthedocs.io/en/latest/projects.html#making-predictions)
for more information on the lexical matching workflow.

#### Different Senses

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

Schultz _et al._ (2011) proposed a way to formalize the connections between the
various senses for diseases in
[Scalable representations of diseases in biomedical ontologies](https://link.springer.com/article/10.1186/2041-1480-2-S2-S6).
However, the OBO community has yet to resolve the
[long and taxing discussion](https://github.com/OBOFoundry/COB/pull/226) on how
to standardize disease modeling practices.

For semantic mappings, this becomes a problem because a reasoner will explode if
diseases under two different BFO branches get marked as equivalent, because the
BFO upper level terms are marked as disjoint - this is a feature, not a bug.
However, while useful for creating carefully constructed, logically
(self-)consistent descriptions of diseases, these modeling choices can be
confusing when curating or reviewing mappings. These modeling choices might not
be so important in downstream applications, such as assembling a knowledge graph
to support graph machine learning, where many different knowledge sources with
lower levels of accuracy and precision must be merged. In practice, I have
merged triples using conflicting senses for diseases in a useful way, without
issue.


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

### Evidence

A key challenged that motivated the development of SSSOM as a standard was to
associate high-quality metadata with semantic mappings, such as the reason the
mapping was produced (e.g., manual curation, lexical matching, structural
matching), who produced it (e.g., a person, algorithm, agent), when, how, and
more.

[![](/img/mappings-are-hard/evidence.svg)](https://docs.google.com/drawings/d/1rBofcaQxBFuYX0OzhCvBkigSNFWLclAbQ_X7zG7PRKA/edit?usp=sharing)

We developed the
[Semantic Mapping Vocabulary (semapv)](https://semantic.farm/registry/semapv) to
encode different kinds of evidence such as for manual curation of mappings,
lexical matching, structural matching, and others. SSSOM is well-suited towards
capturing simple evidences (blue).

#### Provenance for Inferences

But, the purple one requires a more detailed metadata model that simply doesn't
fit in the SSSOM paradigm (and it shouldn't be hacked in, either). I proposed a
more detailed data model for capturing how inference is done in
[Assembly and reasoning over semantic mappings at scale for biomedical data integration](https://doi.org/10.1093/bioinformatics/btaf542)
and provided a reference implementation in the
[Semantic Reasoning Mapper and Reasoner (SeMRA)](https://github.com/biopragmatics/semra)
Python software package. Here's what that data model looks like, which also has
a Neo4j counterpart:

[![](/img/mappings-are-hard/semra-data-model.svg)](https://docs.google.com/drawings/d/1C5l1UmwKohMsgprSXRK6Lo2egLsRWhXPIfoVo09tJ9I/edit?usp=sharing)

### Negative Semantic Mappings

SSSOM also has first-class support for encoding _negative_ relationships,
meaning that the following can be represented:

[![](/img/mappings-are-hard/negatives.svg)](https://docs.google.com/drawings/d/1AfCR35ra3FyQMulaTlynVZKswLbj8gp5MA4N2ipFe1I/edit?usp=sharing)

This means that SSSOM curators can keep track of non-trivial negative mappings,
e.g., when curating the results of semantic mapping prediction or automated
inference. In a semi-automated curation loop, this allows us to avoid
re-reviewing [zombie mappings](https://doi.org/10.32388/DYZ5J3) over and over
again.

High quality, non-trivial negative mappings also enable more accurate machine
learning, as opposed to using negative sampling. For example, we have been
working on developing graph machine learning-based ontology matching and merging
using [PyKEEN](https://github.com/pykeen/pykeen/) (a graph machine learning
package I helped develop and maintain).

An open challenge is that we neither have support from data modeling formalisms
(e.g., ontologies in OWL, knowledge graphs in RDF or Neo4j) to encode negative
knowledge (in this case negative mappings) nor tooling support. This means that
when we output SSSOM to RDF, we use our own formalism, which won't be
correctly recognized by any other tooling that wasn't developed with SSSOM in
mind. I'm keeping notes about this in a separate [post about negative
knowledge]({% post_url 2025-10-09-negative-rdf %}) that I update periodically.
