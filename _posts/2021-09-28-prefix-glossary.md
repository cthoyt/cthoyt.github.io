---
layout: post
title: A Glossary for the Bioregistry
date: 2021-09-14 09:47:00 +0100
author: Charles Tapley Hoyt
tags: semantics
---
There are a lot of terms that I've been throwning around when talking about
the Bioregistry, so here's a glossary of each of them.

## Naming things on the semantic web

There are two (mostly) interchangeable formalisms for naming things in the
semantic web: uniform resource identifiers (URIs) and compact uniform
resource identifiers (CURIEs).

### Uniform Resource Identifiers (URIs)

The semantic web community has adopted the internationalized resource identifier
(IRI) as the _de facto_ standard for naming entities. In practice, usage is
often restricted to IRIs that are also uniform resource identifiers (URIs; i.e.,
they only use ASCII characters) and that are also valid uniform resource
locators (URLs, i.e., they point to a web page). In applied semantic web
contexts like biomedicine, the subtleties between URLs, URIs, and IRIs are
disregarded and the term URI is preferred. A more detailed explanation on the
difference between URLs, URIs, and IRIs can be
found [here](https://fusion.cs.uni-jena.de/fusion/2016/11/18/iri-uri-url-urn-and-their-differences/).

For a given nomenclature like the [Chemical Entities of Biological Interest (ChEBI)](https://www.ebi.ac.uk/chebi),
URIs can usually be split into two parts:

1. A URI prefix (in red)
2. A local identifier (in orange)

All URIs from the same nomenclature have the same URI prefix (in red),
but a different local identifier (in orange). Here's an example, using the ChEBI
local identifier
for [alsterpaullone](https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:138488):

<span style="color:red">https://www.ebi.ac.uk/chebi/searchId.do?chebiId=CHEBI:</span><span
style="color:orange">138488</span>

There may be potentially many URI prefixes corresponding to the same local
nomenclature and therefore many URIs describing the same entity. For example,
ChEBI also serves images with:

<span style="color:red">https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=</span><span
style="color:orange">138488</span>

### Compact Uniform Resource Identifiers (CURIEs)


## Resource

A resource assigns unique identifiers to a collection of entities.

### Types of Resources

There are several types of resources such as:

1. **Ontologies** like the [Gene Ontology (GO)](https://bioregistry.io/go)
   , [Chemical Entities of Biological Interest (ChEBI)](https://bioregisty.io/chebi)
   , and [Experimental Factor Ontology (EFO)](https://bioregistry.io/efo)
2. **Controlled Vocabularies**
   like [Entrez Gene](https://bioregistry.io/ncbigene)
   , [InterPro](https://biorestry.io/interpro),
   and [FamPlex](https://bioregistry.io/fplx)
3. **Databases** like [Protein Data Bank](https://bioregistry.io/pdb)
   and [Gene Expression Omnibus](https://bioregistry.io/geo)

### Completeness

Resources typically fall into one of several "completeness" categories:

1. **Complete by Definition**
   like [Enzyme Classification](https://bioregistry.io/eccode)
2. **Complete, but Subject to Change** like [HGNC](https://bioregistry.io/hgnc)
3. **Always Incomplete**
   like [Chemical Entities of Biological Interest (ChEBI)](https://bioregisty.io/chebi)
   and [PDB](https://bioregistry.io/pdb)

### Scope

Resources have a variety of scopes

1. **Single entity type** like [HGNC](https://bioregistry.io/hgnc)
2. **A few entity types** like
   the [Gene Ontology (GO)](https://bioregistry.io/go)
3. **Many entity types**
   like [Medical Subject Headings (MeSH)](https://bioregistry.io/mesh)
   , [Unified Medical Language System (UMLS)](https://bioregistry.io/ums)
   , [National Cancer Institute Thesaurus (NCIT)](https://bioregistry.io/ncit)

### Relationship to Projects and Organizations

Resources do not always correspond one-to-one with projects, such as how the
ChEMBL database contains both the ChEMBL Compound and ChEMBL Target resources or
how the Uber Anatomy Ontology (UBERON) contains both UBERON and UBPROP resources
for terms and properties, respectively.

There are a variety of patterns used for identifiers, including integers (^\d+$;
e.g., PubMed), zero padded integers (`^\d{7}$`; e.g., GO, ChEBI, other OBO
Ontologies), universally unique identifiers (UUIDs; e.g., NCI Pathway
Interaction Database, NDEx), and many other variations.

### Provider

A provider returns information about entities from a given resource. A provider
is characterized by a URL format string into which an identifier from its
resource can be substituted for a special token (e.g., $1). For example, the
following formatter can be used to get a web page about a given HGNC entity
based on its identifier by replacing the $1 with a given HGNC gene identifier
like 5173 for
HRAS: http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=$1.

Well-behaved URL format strings only have one instance of the special token that
occurs at the end. Poorly-behaved URL format strings may have additional
characters following the special token as
in http://rebase.neb.com/rebase/enz/$1.html for REBASE or as
in http://eawag-bbd.ethz.ch/$1/$1_map.html for the UM-BBD Pathway database.

Providers can return information HTML as in the previous example, images (
e.g., https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&chebiId=132964
for the ChEBI entry on fluazifop-P-butyl), XML (
e.g., https://www.uniprot.org/uniprot/P10636.xml for UniProt entry on human
Microtubule-associated protein tau), or any other information that can be
transferred via HTTP, FTP, or related data transfer protocols. Alternatively,
content negotiation could be used to return multiple kinds of data from the same
provider URL.

Most resources have an associated first-party provider that returns information
via a web page. Some resources, like ChEBI, have several first-party providers
for different content types (e.g., HTML, image). Some resources, like Entrez
Gene, have additional external providers, including databases that use its
identifiers like the Comparative Toxicogenomics Database. Some resources, such
as many OBO ontologies, do not have an associated first party provider and rely
solely on third party browsers like AberOWL, OntoBee, and the Ontology Lookup
Service.

### Registry

A registry is a special kind of resource that assigns unique identifiers to a
collection of resources. For historical reasons, these identifiers are
colloquially called prefixes. A registry collects additional metadata about each
resource, though there is a wide variety of metadata standards across existing
registries (Table 1; left). These metadata may include the name, homepage, a
regular expression pattern for validating identifiers, one or more example
identifiers, a default provider, and potentially additional providers.

Like with resources, a high-quality registry should have an associated
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

A resolver uses a registry to generate a URL for a given prefix/identifier pair
based on the registry's default provider for the resource with the given prefix,
then redirects the requester to the constructed URL. Resolvers are different
from providers in that they are general for many resources and do not host
content themselves. Two well-known resolvers are Identifiers.org and
Name-To-Thing.

Lookup Service A lookup service is like a provider but generalized to provide
for many resources. They typically have a URL format string into which a compact
identifier can be placed like OntoBee, but many require more complicated
programmatic logic to construct. Some well-known lookup services are the OLS,
AberOWL, OntoBee, and BioPortal.