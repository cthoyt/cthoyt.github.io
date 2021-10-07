---
layout: post
title: A Glossary for the Bioregistry
date: 2021-09-14 09:47:00 +0100
author: Charles Tapley Hoyt
tags: semantics
---
There are a lot of terms that I've been throwing around when talking about the
Bioregistry, so this blog post is a first draft of a gloassary of all of them.

Later, I will revise this further and put it either on the Bioregistry website,
or make a totally new repo on the [Biopragmatics](https://github.com/biopragmatics)
GitHub organization.

## Semantic spaces

A [controlled vocabulary](https://en.wikipedia.org/wiki/Controlled_vocabulary)
enumerates a set of named entities. For example, the
[Chemical Entities of Biological Interest (ChEBI)](https://www.ebi.ac.uk/chebi)
is a well-known controlled vocabulary in the biomedical domain that lives in
an ontology.

### Local identifiers

A useful (but not required) property of a controlled vocabulary is to
additionally assign each named entity a stable **local identifier**. Throughout
this document, it is assumed that all controlled vocabularies have this
property. Any resource that assigns stable local identifiers to entities,
even if it is not itself a controlled vocabulary, is a **semantic space**.

The term _local identifier_ is synonymous with _identifier_ and _accession_,
but has the added qualifier _local_ as a reminder that two controlled
vocabularies may use the same one. For example, the [Chemical Entities of Biological Interest (ChEBI)](https://www.ebi.ac.uk/chebi)
entry for [6-methoxy-2-octaprenyl-1,4-benzoquinone](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:1234)
and the [Human Disease Ontology (DOID)](https://bioregistry.io/doid) entry for
[gender identity disorder](https://www.ebi.ac.uk/ols/ontologies/doid/terms?obo_id=DOID:1234)
share the local identifier of `1234`.

It's often useful to have a [regular expression](https://en.wikipedia.org/wiki/Regular_expression)
that describes local identifiers of a given semantic space. For example,
both ChEBI and DOID use local identifiers that look like numbers, which match
the regular expression `^\d+$`. The `^` and `$` denote the beginning and end
of the regular expression and appear exactly the same in all regular expressions
for local identifiers. The `\d` will match a number and the `+` means that the
preceding token (`\d`) can be matched one or more times in a row.

It's important to remember that identifiers might look like numbers, but they
should _never_ be treated as such. For example, the [Gene Ontology (GO)](https://bioregistry.io/go)
uses identifiers that are left-padded with zeros like in `0032571`
for [response to vitamin K](https://bioregistry.io/go:0032571). The regular
expression pattern for GO entries is `^\d{7}$`, since there are always exactly
seven numbers. Regular expressions don't have a straightforward way to describe
numbers that are left padded with zero, so keep in mind that this is
approximation is a good balance between precision and simplicity.

There are a variety of patterns used for identifiers, including integers (`^\d+$`;
e.g., PubMed), zero padded integers (`^\d{7}$`; e.g., GO and other OBO
Ontologies), universally unique identifiers (UUIDs; e.g., NCI Pathway
Interaction Database, NDEx), and many other variations.

### Origins

Controlled vocabularies arise from several kinds of resources such as:

1. **Ontologies** like the [Gene Ontology (GO)](https://bioregistry.io/go),
   [Chemical Entities of Biological Interest (ChEBI)](https://bioregisty.io/chebi),
   and [Experimental Factor Ontology (EFO)](https://bioregistry.io/efo)
2. **Controlled Vocabularies** like [Entrez Gene](https://bioregistry.io/ncbigene),
   [InterPro](https://biorestry.io/interpro), and [FamPlex](https://bioregistry.io/fplx)
3. **Databases** like [Protein Data Bank](https://bioregistry.io/pdb)
   and [Gene Expression Omnibus](https://bioregistry.io/geo)

### Completeness

Controlled vocabularies typically fall into one of several "completeness"
categories:

1. **Complete by Definition** like [Enzyme Classification](https://bioregistry.io/eccode)
2. **Complete, but Subject to Change** like [HGNC](https://bioregistry.io/hgnc)
3. **Always Incomplete** like [Chemical Entities of Biological Interest (ChEBI)](https://bioregisty.io/chebi)
   and the [Protein Data Bank (PDB)](https://bioregistry.io/pdb)

### Scope

Controlled vocabularies have a variety of scopes:

1. **Single entity type** like [HGNC](https://bioregistry.io/hgnc)
2. **A few entity types** like the [Gene Ontology (GO)](https://bioregistry.io/go)
3. **Many entity types**
   like [Medical Subject Headings (MeSH)](https://bioregistry.io/mesh),
   [Unified Medical Language System (UMLS)](https://bioregistry.io/ums),
   [National Cancer Institute Thesaurus (NCIT)](https://bioregistry.io/ncit)

### Relationship to Projects and Organizations

Controlled vocabularies do not always correspond one-to-one with projects, such
as how the ChEMBL database contains both the [ChEMBL Compound](https://bioregistry.io/chembl.compound)
and [ChEMBL Target](https://bioregistry.io/chembl.target) controlled
vocabularies or how the Uber Anatomy Ontology (UBERON)
contains both [UBERON](https://bioregistry.io/uberon) and UBPROP controlled
vocabularies for terms and properties, respectively.

## Providers

A provider returns information about entities from a given semantic space. A provider
is characterized by a **URI format string**, or URI formatter, into which a
local identifier from its semantic space can be substituted for a special
token (e.g., `$1`). For example, the following formatter can be used to get a
web page about [HRAS](https://bioregistry.io/hgnc:5173) by replacing `$1` in the
URI format string
`http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=$1` by its HGNC
identifier, `5173`.

Well-behaved URI format strings only have one instance of the special token that
occurs at the end. Poorly-behaved URI format strings may have additional
characters following the special token as
in `http://rebase.neb.com/rebase/enz/$1.html` for [REBASE](https://bioregistry.io/rebase)
or as in `http://eawag-bbd.ethz.ch/$1/$1_map.html` for the
[UM-BBD Pathway database](http://bioregistry.io/umbbd.pathway).

### Content Type

While providers typically return human-readable HTML, they can also return
many other data types, including:

- Images (e.g., https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&chebiId=132964 for the ChEBI entry on fluazifop-P-butyl)
- XML (e.g., https://www.uniprot.org/uniprot/P10636.xml for UniProt entry on human Microtubule-associated protein tau)
- JSON (e.g., https://gen3.biodatacatalyst.nhlbi.nih.gov/ga4gh/drs/v1/objects/0000ffeb-36e0-4a29-b21d-84423bda979d for NCBI's BioData Catalyst)
- RDF

Providers can return any other information that can be transferred via HTTP,
FTP, or related data transfer protocols. Alternatively, content negotiation
could be used to return multiple kinds of data from the same provider URI.

### Responsibility

Most controlled vocabularies have an associated first-party provider that
returns information via a web page. Some controlled vocabularies, like ChEBI,
have several first-party providers for different content types (e.g., HTML,
image). Some controlled vocabularies, like Entrez Gene, have additional external
providers, including databases that use its identifiers like the Comparative
Toxicogenomics Database. Some controlled vocabularies, such as many OBO
ontologies, do not have an associated first party provider and rely
solely on third party browsers like AberOWL, OntoBee, and the Ontology Lookup
Service.

## Naming things on the semantic web

There are two (mostly) interchangeable formalisms for naming things in the
semantic web: uniform resource identifiers (URIs) and compact uniform resource
identifiers (CURIEs).

### Uniform Resource Identifiers (URIs)

The semantic web community has adopted the **internationalized resource
identifier (IRI)** as the _de facto_ standard for naming entities. In practice,
usage is often restricted to IRIs that are also **uniform resource identifiers
(URIs)** (i.e., they only use ASCII characters) and that are also **valid
uniform  resource locators (URLs)** (i.e., they point to a web page). In applied
semantic web contexts like biomedicine, the subtleties between URLs, URIs, and
IRIs are disregarded and the term URI is preferred such as in the seminal paper
[Identifiers for the 21st Century](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.2001414#sec001).
A more detailed explanation on the difference between URLs, URIs, and IRIs can
be found [here](https://fusion.cs.uni-jena.de/fusion/2016/11/18/iri-uri-url-urn-and-their-differences/).

For a given semantic space like ChEBI, URIs can usually be constructed
given two parts:

1. A **URI prefix** (in red)
2. A local identifier (in orange)

All URIs from the same semantic space have the same URI prefix (in red),
but a different local identifier (in orange). Here's an example, using the ChEBI
local identifier for [alsterpaullone](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:138488):

<span style="color:red">https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:</span><span style="color:orange">138488</span>

There may be potentially many URI prefixes corresponding to the same
semantic space and therefore many URIs describing the same entity. For example,
ChEBI also serves images with:

<span style="color:red">https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=</span><span style="color:orange">138488</span>

### Compact Uniform Resource Identifiers (CURIEs)

A **compact uniform resource identifier (CURIE)** allows for the replacement of
a URI prefix in a URI with a short prefix. As a short recapitulation of the
[W3C specification](https://www.w3.org/TR/2010/NOTE-curie-20101216), a CURIE has
three parts:

1. A prefix (in red)
2. A delimiter (in black)
3. A local identifier from the given semantic space (in orange)

Since everyone agrees on what ChEBI is within the biomedical domain, it makes
sense to use `chebi` as the prefix for ChEBI local identifiers. However, there
is no globally unique set of prefixes used across the semantic web (nor should
there be). Therefore, when using CURIEs, you need at minimum a prefix map
(described below) and ideally a registry that stores additional metadata about
each prefix.

Here's the same example as in the URI section above for alsterpaullone, but now
condensed into a CURIE:

<span style="color:red">chebi</span><b>:</b><span style="color:orange">138488</span>

### Converting between URIs and CURIEs

A **prefix map** associates each prefix to exactly one URI prefix. It can be
used to expand CURIEs into URIs. Disregarding (for now) how to choose the
best URI prefix, one potential prefix map that could be used to expand the
example CURIE for alsterpaullone could be:

```json
{
  "chebi": "https://www.ebi.ac.uk/chebi/searchId.do?chebiId="
}
```

A simple algorithm for expanding a CURIE to a URI is as follows:

1. Split the CURIE on the first instance of the delimiter, usually a colon `:`
2. Look up the left-hand side of the split (i.e., the prefix) in the prefix map
3. String concatenate the resulting URI prefix with the right-hand side of the
   split (i.e., the local identifier)

A **reverse prefix map** associates one or more URI prefixes to each prefix.
It can be used to contract URIs into CURIEs. Disregarding (for now) how to chose
the best prefix for each URI prefix, one potential reverse prefix map that could
be used to contract the two example URIs for alterpaullone could be:

```json
{
  "https://www.ebi.ac.uk/chebi/searchId.do?chebiId=": "chebi",
  "https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=": "chebi"
}
```

Because it's possible some URI prefixes might overlap, it's a good heuristic to
check a given URI against a reverse prefix map in decreasing order by URI prefix
length.

### Poorly Behaved URIs

Unfortunately, not all URLs that provide information about named entities
in controlled vocabularies can be trivially split into a URI prefix and a
local identifier. For example, the [ViralZone](https://bioregistry.io/viralzone)
entry for [Fusion of virus membrane with host endosomal membrane](https://bioregistry.io/viralzone:992)
has a URL that looks like http://viralzone.expasy.org/all_by_protein/992.html.
Note the pesky `.html` at the end, which can't be removed because of the way
the web server works.

While this creates a big problem for parsing URIs into CURIEs, it's still
possible to generate a URI from a CURIE given a slight variation on a prefix map,
which introduces the notion of a **URI formatter**. A URI formatter is a string
that contains a `$1` character anywhere the local identifier should be put.
For ViralZone, the URI formatter looks like: 
`http://viralzone.expasy.org/all_by_protein/$1.html`. Interestingly, there are
examples where the local identifier appears twice in the URI formatter, like
for the [EAWAG Biocatalysis/Biodegradation Database](http://bioregistry.io/umbbd.pathway),
which has a URI formatter string of `http://eawag-bbd.ethz.ch/$1/$1_map.html`.

A URI prefix corresponds to a special case of a URI formatter where there
is exactly one instance of `$1` that appears at the end of the string.
Therefore, it is more valuable to curate URI formatters and programmatically
generate prefix maps when possible. The fact that some URIs are hard to
construct easily is also one of the motivations for resolver services, described
in a later section.

### Open Biomedical Ontologies CURIEs

The [Open Biomedical Ontologies (OBO) Foundry](http://www.obofoundry.org/)
provides a persistent URL service (PURL) to create stable URIs for biomedical
entities curated in their ontologies (e.g., [Human Disease Ontology](https://bioregistry.io/doid),
[Phenotype And Trait Ontology](https://bioregistry.io/pato)). They have four
parts:

1. A URI prefix (in red; always the same)
2. An ontology prefix (in orange)
3. A delimiter (in black; always the same)
4. An ontology local identifier (in blue)

<span style="color:red">http://purl.obolibrary.org/obo/</span><span style="color:orange">DRON</span>_<span style="color:blue">0000005</span>

Confusingly, some people consider the entire combination of the ontology's
prefix, the delimiter, and the ontology's local identifier
(e.g., `DRON_0000005`) as a local identifier
in the OBO namespace, whose URI prefix is `http://purl.obolibrary.org/obo/`.
This confusion lead to services like Identifiers.org to denote these ontologies
as having the "namespace embedded in the local unique identifier" and therefore
include the prefix again in the regular expression pattern describing the local
identifiers, e.g. `^DOID:\d+$` for the Human Disease Ontology.

This notation makes no sense for a slew of reasons:

1. The regular expression should correspond to the local identifiers of a
   semantic space like `DOID`, not a registry like the OBO PURL system.
2. If you follow the simple algorithm for constructing a CURIE from a prefix and
   identifier, you end up with identifiers that look like CURIEs like
   `DOID:11337` or redundant CURIEs that look like `DOID:DOID:11337`.
3. It creates ambiguities in spreadsheets where columns are supposed to
   contain local identifiers or CURIEs.

The solution is simply to drop the entire notion of namespaces embedded in local
unique identifiers. Since this would require updating a lot of data in a lot
of places, the interim solution is to programmatically normalize identifiers and
CURIEs in the meantime to remove instances of this redundancy.

### Registry

A registry is a special kind of semantic space that assigns unique
identifiers to a collection of controlled vocabularies. For historical reasons, these identifiers are
colloquially called prefixes. A registry collects additional metadata about each
semantic space, though there is a wide variety of metadata standards across existing
registries (Table 1; left). These metadata may include the name, homepage, a
regular expression pattern for validating identifiers, one or more example
identifiers, a default provider, and potentially additional providers.

Like with controlled vocabularies, a high-quality registry should have an associated
first-party provider that comprises a web site for exploring its entries and
their associated metadata.

Some registries are directly imported and reused in other places (e.g., GO
Registry reused in
psi-mi-CV [https://github.com/HUPO-PSI/psi-ms-CV/blob/master/db-xrefs.yaml],
NCBI GenBank Registry reused in https://www.ddbj.nig.ac.jp/ddbj/db_xref-e.html).

### Metaregistry

A metaregistry is a special kind of registry that assigns unique identifiers to
a collection of registries; it could even contain an entry about itself. It
collects additional metadata about each registry, such as a description of its
metadata standards and capabilities (Table 1; right). Most importantly, a
metaregistry contains mappings between equivalent entries in its constituent
registries. Before the publication of this article, to the best of our
knowledge, there were no dedicated metaregistries. Some registries such as
FAIRSharing and the MIRIAM/Identifiers.org registry contain limited numbers of
entries referring to other registries (e.g., BioPortal), but they neither
delineate these records as representing registries, provide additional metadata,
nor provide mappings.

### Resolver

A resolver uses a registry to generate a URI for a given prefix/identifier pair
based on the registry's default provider for the semantic space with the given prefix,
then redirects the requester to the constructed URI. Resolvers are different
from providers in that they are general for many controlled vocabularies and do not host
content themselves. Two well-known resolvers are Identifiers.org and
Name-To-Thing.

Lookup Service A lookup service is like a provider but generalized to provide
for many controlled vocabularies. They typically have a URI format string into which a compact
identifier can be placed like OntoBee, but many require more complicated
programmatic logic to construct. Some well-known lookup services are the OLS,
AberOWL, OntoBee, and BioPortal.