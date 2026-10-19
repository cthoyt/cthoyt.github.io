---
layout: post
title: Annotating Custom URI Prefixes for OBO Foundry Ontologies
date: 2026-10-19 12:44:00 +0200
author: Charles Tapley Hoyt
tags:
  - OBO Foundry
  - Semantic Farm
  - Bioregisrry
  - CHEMINF
  - FMA
  - MAMO
  - SWO
  - ontologies
  - SHACL
  - JSON-LD
  - VANN
  - URI prefix
  - PURL
---

This post describes a recent improvement to the
[Semantic Farm](https://semantic.farm) alignment workflow with the
[Open Biological and Biomedical Ontology (OBO) Foundry](https://obofoundry.org)
enabled by contributing upstream data and code improvements to the OBO Foundry
itself.

While the OBO Foundry
[Principle 3 (URI/Identifier Space)](https://obofoundry.org/principles/fp-003-uris.html)
states

> Each ontology MUST have a unique IRI in the form of an OBO Foundry persistent
> URL (PURL) that includes the ontology’s short namespace.

there are four ontologies for which this isn't the case:

| Prefix                                   | Name                                   | URI Prefix                                     |
|------------------------------------------|----------------------------------------|------------------------------------------------|
| [CHEMINF](https://semantic.farm/cheminf) | Chemical Information Ontology          | `http://semanticscience.org/resource/CHEMINF_` |
| [FMA](https://semantic.farm/fma)         | Foundational Model of Anatomy Ontology | `http://purl.org/sig/ont/fma/`                 |
| [MAMO](https://semantic.farm/mamo)       | Mathematical Modeling Ontology         | `http://identifiers.org/mamo/MAMO_`            |
| [SWO](https://semantic.farm/swo)         | Software Ontology                      | `http://www.ebi.ac.uk/swo/SWO_`                |

## Updating the OBO Foundry

Because the OBO Foundry previously assumed that all OBO Foundry ontologies
followed principle four, it had a hard-coded rule for generating JSON-LD and
SHACL contexts that incorrectly created incorrect URI prefixes like
`http://purl.obolibrary.org/obo/CHEMINF_` for the Chemical Information Ontology
following the rule for well-behaved ontologies like the
[Gene Ontology (GO)](https://semantic.farm/go), whose URI prefix is
`http://purl.obolibrary.org/obo/GO_`.

Therefore, I made a pull request to the OBO Foundry in
<https://github.com/OBOFoundry/OBOFoundry.github.io/pull/2951> that extended its
data model to include a `uri_prefix` field and add the explicit override for
each of the four ontologies above. It also updated the context-generating
scripts to take into account these annotations.

Further, I added into the JSON-LD context a mapping from `uri_prefix` to the
predicate from the
[vocabulary for annotating vocabulary descriptions (VANN)](https://semantic.farm)
for describing the URI prefix for a given resource
([`vann:preferredNamespaceUri`](https://semantic.farm/vann:preferredNamespaceUri)).
This gets explicitly reflected in the
[Turtle version](https://github.com/OBOFoundry/OBOFoundry.github.io/blob/master/registry/ontologies.ttl)
of the JSON-LD export of the registry. The specific usage of the new predicate
can be seen
[here](https://github.com/OBOFoundry/OBOFoundry.github.io/blob/2e6d1f43e5ca74100c64920ec11cb9fb7680fc59/registry/ontologies.ttl#L822-L836).

## Updating VANN

During the process, I actually realized that there was a misconfiguration on the
purl.org redirects for the VANN PURLs. Specifically, PURLs like
<http://purl.org/vocab/vann/usageNote> were redirecting to
<https://vocab.org/vann/usageNote> when they should have been redirecting to
<https://vocab.org/vann/#usageNote>.

Luckily, I was able to reach out to VANN's maintainer via its GitHub repository
and suggest a fix on <https://github.com/iand/vocabdotorg/issues/4>. Ian was
able to fix the configuration the same day, once again demonstrating that open
science is awesome.

## Updating the Semantic Farm / Bioregistry

The gap in the OBO Foundry's curated data about its ontologies wasn't new. I had
actually already written custom overrides in the Semantic Farm / Bioregistry's
alignment script to override one (but not all four) of these during ingestion of
the OBO Foundry.

After the OBO Foundry pull request was accepted, I was able to remove the custom
overrides in a pull request to the Semantic Farm / Bioregistry
(<https://github.com/biopragmatics/bioregistry/pull/2130>).

---

Like [my previous post]({% post_url 2026/2026-10-02-world-avatar %}) describing
contributions I made to the World Avatar project, this post is yet another
demonstration of the goodness of openness, shared technical infrastructure, and
learning to love the [drive-by curation](https://doi.org/10.32388/KBX9VO).
