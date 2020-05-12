---
layout: post
title: The Trouble with Ontologies, or, How to Build an Ontology
date: 2020-05-12 00:00:00 -0800
---
Everyone's talking about biomedical ontologies! Let's
look at where most people go wrong and how to do it right.

# The Trouble with Biomedical Ontologies

There's a lot of confusion within the biomedical community as to what
constitutes an ontology. It's been aggravated by the impenetrable discourse
used by ontologists similar to the way that mathematicians and computer
scientists have a habit of using obscure mathematical notation to obfuscate
their work. Even worse, this has led to confusion within the biomedical
community as to what an ontology is for.

For example, biocurators find ontologies useful as a research tool for looking
up the definitions of entities using tools like the [Ontology Lookup Service (OLS)](https://www.ebi.ac.uk/ols/index).
Database maintainers and biocurators often look to ontologies to decide what
their data should look like and enable other people to understand it readily.
Similarly, natural language processing (NLP) researchers find ontologies
incredibly useful in named entity recognition because ontologies often contain
preferred labels in many languages and synonyms for its terms. Software
developers and end-users find ontologies useful for organizing and conveying
information in a hierarchical manner. 

While it might be true that ontologies have the ability to support all of those
uses, none accurately portray ontologies. The following table presents more
appropriate vocabulary to describe each of these use cases:


| Phrase | Definition |
| ------ | ---------- |
| Controlled Vocabulary | An enumerated set of entities |
| Dictionary | An enumerated set of entities and their definitions |
| Thesaurus | An enumerated set of entities and their synonyms |
| Hierarchy | An enumerated set of entities with one parent for each |
| Multi-Hierarchy | An enumerated set of entities with one or more parents for each |

Database maintainers need controlled vocabularies to improve the utility of
their databases, researchers can leverage dictionaries to learn the
definitions, NLP developers need thesauri containing synonyms to train their
models, and software developers need hierarchies or multi-hierarchies to
support organization.

The actual purpose of an ontology is to first define the rules for how
information is organized and second to apply those rules and actually store
information. This means that ontologies can define that entities need an
identifier, they need a preferred label, they can have synonyms, they can have
equivalences to other entities in other ontologies, they can have
relationships in the form of triples (like parent-child relationships), and
they can even have relationships in the form of quadruples or
higher-dimensional tuples. There are "upper-level" ontologies that take care
of some of the common definitions that can be shared throughout a domain -
you've probably noticed that most biomedical ontologies have this core of
previously mentioned relationship types. That enables "lower-level" ontologies
to focus on storing the information. Since most researchers only interact with
the "lower-level" ontologies, it can be understood where the confusion came
from.

In practice, this confusion is mostly harmless. We have numerous high-quality
ontologies covering a huge amount of biology and related fields, as well as
the [OBO Foundry](http://www.obofoundry.org) to vet them for quality and host
them. Note: [BioPortal](http://bioportal.bioontology.org/) is another place
for hosting, but it seems like it has a much lower (or non-existent?) threshold
for quality.

The danger lies in the edge cases. When there are no high quality biomedical
ontologies in a given area, researchers are often inclined to generate their
own. The rest of this blog post is about what happens next, where it all goes
wrong, and how you can avoid it when you're in the situation that you just
became an ontologist, too.

# How to Build Your Own Biomedical Ontology

The curation I trust most is by people who know what they're doing, and more
importantly by people who love what they're doing.

Given the choice between curating information about a new protein (e.g. the
proteins in the novel coronavirus) myself or having one of the excellent
curators at [UniProt](https://www.uniprot.org/) do it, I would choose
UniProt every time. Given the choice between the world's leading
coronavirus researcher and a UniProt curator with no previous knowledge
about the novel coronavirus, I would still choose the UniProt curator.
The UniProt curators love what they do, they know how to do it well,
and they do it right. Same goes for lots of other groups that I've praised
elsewhere in this blog. So keep in mind while you're reading this guide that
you might be causing more harm than good by making yet another ontology.

## Preparation

Before you start curating you need to do a bit of planning.

### Pick a memorable name and prefix

There are a lot of ontologies, so pick a name that's both unique and
descriptive. Then, you need to pick a relatively short "prefix" which will be
the first part of [compact URIs (CURIEs)](https://en.wikipedia.org/wiki/CURIE)
that point to entries in your ontology. Many ontologies use an acronym as
their prefix, but make sure you don't cause a conflict or confusion with a
previously existing one. You can search through
registries like [Identifiers.org](https://identifiers.org), the OLS, or the
[OBO Foundry](http://www.obofoundry.org/) (which, on a side
note, don't exactly contain all of the same stuff) to check out the existing
landscape.

### Pick a scheme for identifiers

Even if you're just here to build and maintain your controlled vocabulary,
it's still necessary to give identifiers to each of the entries in your
ontology. In practice, each entry's identifier should conform to the [Minimal
Information Requested in the Annotation of Biochemical Models (MIRIAM)](https://pubmed.ncbi.nlm.nih.gov/18078503/)
standard. It states that identifiers should have the following five properties:

1. Uniqueness
2. Perenniality
3. Standards-Compliant
4. Resolvability
5. Free Usability

There's a really important thing to keep in mind - identifiers are not numbers.
Even if they look like them, they're strings. If that doesn't make sense to
you, then just think about what it would mean to "add" two identifiers to each
other. It would be nonsense to think of identifiers as numbers because they
don't do what numbers do. With that in mind, there are a few common identifier
schemes:

- Identifiers that look like numbers, like PubMed identifiers. An example from
  PubMed is [29048466](https://identifiers.org/pubmed:29048466).
- Identifiers that look like numbers, but are a fixed width with left-padded
  zeros. An example from the [Experimental Factor Ontology](https://www.ebi.ac.uk/efo/)
  is [0004859](https://identifiers.org/efo:0004859).
- Identifiers that look like numbers, but are a fixed width with left-padded
  zeros and are prefixed with the prefix itself separated by a colon, so the
  identifier itself looks like a CURIE. An example from the [Gene Ontology](http://geneontology.org/)
  is [GO:0006915](https://identifiers.org/GO:0006915). This is sort of
  confusing, and has been dubbed the GOGO problem. Or the Bananananana problem.
- Identifiers that look like numbers, but are prefixed with part of all of the
  prefix. An example from [ChEMBL](https://www.ebi.ac.uk/chembl/) is
  [CHEMBL941](https://identifiers.org/chembl.compound:CHEMBL941) where the
  prefix is `chembl.compound`.
- Identifiers that have a short letter prefix then a fixed width number with
  left-padded zeros. An example from MeSH is [D013313](https://identifiers.org/mesh:D013313).

My favorite is the MeSH style, because it allows for the most information to be
conveyed succinctly. You should use numbers of width 6 or 7, even if you only
plan on curating a few dozen or hundred terms.

Please don't use the GO style identifiers, because this is creates a ton
of confusion.

You should also write down what the regular expression that goes with your
identifiers for later validation. In the MeSH example, the regular expression
is `^(C|D)\d{6,9}$`, which means it either starts with C or D, and is
followed by between 6 and 9 numbers. The `^` means beginning of the string
and `$` means end of the string, so it's clear that nothing can precede or
follow.

### Pick your scope

The last, and most important, part of planning is to pick the scope of your
ontology. You have to choose what kinds of entities you want to include (genes,
proteins, side effects, etc.). Keep in mind that if you're picking one of these
examples, there's probably already a good nomenclature source for it, so it's
best you don't curate it again.

## Curation

It's time to start curating entries in your ontology. Most people go right to
[Protégé](https://protege.stanford.edu/). 

_Don't_.

Protégé is a really good way to get bogged down in the ivory tower that is
ontology. Instead, it's better to focus on the aspects of the ontology that I
think are practically the most important. So in this guide, we're going to
use a set of interconnected tab-separated values (TSV) documents. Why TSV?
Because comma-separated values (CSV) documents look awful and Excel sheets
can't be diff'd / viewed in GitHub. In a later post, I'll come back
to how to programatically generate OWL, OBO, BEL, and other files from
your curation sheets.

### Curate entities

The most important thing in an ontology is the entities. Make a file called
*entities.tsv*. It needs a few columns to hold the most important information
for each entity:

1. Identifier - the identifier of the entity
2. Name - the preferred name of the entity in the main language of the ontology
3. Type - the entity type. For example, the Gene Ontology has three entity
   types - biological process, cellular component, and molecular function (they
   call them "namespaces"). This isn't the same as the parent of the entity
4. References - keep a comma-separated list of CURIEs pointing to resources
   that have more information about this entity from PubMed, PubMed Central,
   etc.
5. Description - a short description of the entity written as prose.
   Shamelessly borrow from Wikipedia if appropriate, but remember to cite your
   source!
6. Curator [ORCID](https://orcid.org/) identifier - it's really important to
   keep track of who added entries to the ontology so you can get in touch when
   there is confusion or errors are found. The ORCID identifier is the best
   unambiguous way to do this.

You should write and enforce a style guide (e.g., only proper nouns are
capitalized in labels for entities) for names and definitions while you're
here.

If there are other pieces of information that all entities must have in your
ontology, then you can also include it in this sheet. Later, the properties and
relationships sheets can be used for other information and other relationships
such as parent/child relationships, physical properties, etc..

### Curate synonyms

Make a file called *synonyms.tsv*. It needs a few columns to describe synonyms
for each term and the provenance of where they came from:

1. Identifier - the identifier of the entity that matches to the
   *entities.tsv* sheet
2. Synonym - the actual text you found
3. Provenance - a CURIE describing the source that had the synonym. This might
   be a PubMed, PubMed Central, URL, or related.
4. Synonym Semantics - is this an exact synonym, a broad synonym, a narrow
   synonym, or a related synonym? Each entry should only be one of EXACT,
   NARROW, BROAD, or RELATED as defined in the [OBO 1.4
   standard](https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html).
   If you're not sure, just put EXACT.

### Curate xrefs

Make a file called *xrefs.tsv*. It needs three columns:

1. Identifier - the identifier of the entity that matches to the
   *entities.tsv* sheet
2. Xref Prefix - the prefix for the data source that describes
   the same entity
3. Xref Identifier - the local identifier of the entity in the xref's
   data source

The prefix and identifier for the prefix are split to avoid the headache
of parsing CURIEs later.

It's best to consider xrefs as equivalences. All other relationships
should be in the relationships page (later).

### Curate typedefs

An xref is a very specific type of relationship, so it has first-class
status. The parent-child relationship is also first-class and it goes without
saying. The rest of the relationships (that can be expressed realized as
triples) need to be either pulled in from a previously existing ontology
like the [Relation Ontology](http://www.obofoundry.org/ontology/ro.html) or
[PSI-MI](https://www.ebi.ac.uk/ols/ontologies/mi), or defined in a structured
way. Make a file called *typedefs.tsv*, to borrow from the OBO nomenclature
for defining relationships. It should have the following columns:

1. Prefix - could be the same as the current ontology, or an external one
2. Identifier - if it's from the current ontology, you might consider using
   a different identifier scheme than for entities. For example, WikiData
   uses `^Q\d+$` for entities and `^P\d+$` for relationships
3. Name - The preferred name of the relationship
4. (Optional) Inverse Of - If the relationship can be defined as the inverse
   of another, put its CURIE here
5. Parent(s) - a comma-separated list of the relation's parents' CURIEs. This
   is a special case that doesn't appear in the relationships sheets because
   *isA* relationships are so important.

### Curate relationships

You're ready to use the relationships defined in *typedefs.tsv* to write out
relationships. Make *out_relations.tsv* with the following columns:

1. Identifier - the identifier of the entity that matches to
   the *entities.tsv* sheet
2. Relation Prefix
3. Relation Identifier
4. Target Prefix
5. Target Identifier
6. Target Name (Optional, but useful for readers)

Similarly, make another sheet called *in_relations.tsv* with
the following columns:

1. Source Prefix
2. Source Identifier
3. Source Name (Optional, but useful for readers)
4. Relation Prefix
5. Relation Identifier
6. Identifier - the identifier of the entity that matches to the *entities.tsv* sheet

Between these two sheets, you can encode relationships between
entities in the ontology that are both incoming and outgoing, removing
the need to define ad-hoc inverses of common relationships, like *isA*.

### Curate properties

Properties are like relationships that point to scalar values instead of other
entities. For a counterexample, synonyms are a first-class property that
contains lots of extra metadata and therefore get their own sheet.

The rest of the properties will appear here.
A good example of a property is the chemical formula,
SMILES string, and mass of a given small molecule in the [ChEBI ontology](https://www.ebi.ac.uk/chebi/).
However, not all entries in the ChEBI ontology are small molecules, so if they
were following this guide, it might not have made sense to put that property
in the *entities.tsv* sheet. Make a sheet called *properties.tsv* with the
following columns:

1. Identifier - the identifier of the entity that matches to the
   *entities.tsv* sheet
2. Property - it's up to you how to decide what the properties in your
   ontology are. It's not as common to define it as precisely as with
   relationships
3. Value
4. (Optional) Data Type - the XSD data type of the value for the property.
   If this isn't important to you, your life will probably be better by
   leaving it out

Now that you've made all of the sheets, you can make sure that your
curators do their best job to fill out entries in each of them every time
a new entity is added. It's also necessary to keep track of the uniqueness
of entity identifiers as new ones are added. It's best if they're consecutive
and increasing, too.

## Maintenance

One of the other real dangers of starting your own ontology is the entire
concept of maintenance and quality assurance. If you're working in an academic
group, it's highly unlikely that you will have the resources, motivation, or
willpower to maintain the ontology that you are building. This can be proven
by reading through the ontologies listed in BioPortal. While this might be
unavoidable, there are a few things that you can do before your time as a PhD
student, Postdoc, or whatever comes to an end to make sure that your ontology
is actually useful for somebody else.

I've already given my explanation of why to use TSV - it makes sure there's
no conflicts with spaces or commas, tabs never show up in real text, and GitHub
will make nice renders of TSVs and show you the diffs as versions change,
versus Excel documents, which are saved as binary.

### Version Control

As I've just alluded, use version control. Keep track of how your ontology
changes over time by making a repository on GitHub. I've heard rumors that
git was created by Linus Torvalds to slow people down, so you should use
an interactive GUI for git like [GitHub Desktop](https://desktop.github.com/)
(you're not a martyr!). While you're working on GitHub, you should use the
[GitHub Flow workflow](https://guides.github.com/introduction/flow/), which
involves forking (or branching), making pull requests, then reviewing and
discussing before merging into master. This is more relevant for people who
are working on teams. If you're not working on a team, try pulling in a
collaborator to review your work as a pull request. Or email/tweet me!
I'd be happy to help if you're working in open source with a publicly
usable license.

### Tooling

The next few suggestions rely on a bit of technical expertise. The first
is that you should write scripts that validate the content's integrity,
formatting, correctness, or whatever rules you can come up with. Then you
should use continuous integration (e.g., [Travis-CI](https://travis-ci.com/)
or [GitHub Actions](https://github.com/features/actions)) to run those
scripts on every commit to give feedback. If
you're working using the GitHub Flow fork/pull request workflow, then you can
always ask your curators to make sure that their content doesn't make the
validation scripts fail before merging them into master.

Next, you should write scripts that export all of your content into common
formats so others can consume it like OWL, OBO, BEL Namespace, etc.
Additionally, it's nice to automatically build a website that displays all
of the curated content and allows people to explore it. GitHub will even
host the site for free.

These suggestions probably sound a bit abstract or scary if you're not a
seasoned programmer, so in a later post, I'll provide you with a
[cookiecutter](https://github.com/cookiecutter/cookiecutter) template
repository with all of the files, scripts, and configuration that you
need to do this without any programming at all. An example of most of
it in practice is the Curation of Neurodegeneration Supporting Ontology
(CONSO) ([source code](https://github.com/pharmacome/conso);
[web site](https://pharmacome.github.io/conso/)). It has a few differences
from the recommendations I've made in this post - some of them inspired
by choices I made during the curation of CONSO that I think could have
been done better.

### Choose a License

The license tells other people how they're allowed to use your ontology.
If you don't use an appropriate open license, other people will not be
legally allowed to use your ontology. And if that's the case, there really
wasn't a point to making it (yes, I'm being pedantic here). Check out
[https://choosealicense.com/non-software/](https://choosealicense.com/non-software/)
for some pointers. I suggest the
[CC0](https://choosealicense.com/licenses/cc0-1.0/) license, which is the
most usable one out there. Don't fear - people will cite your work and thank
you for it, even if the license doesn't legally obligate them to.

### Making Releases and Long Term Maintenance

If you're using GitHub, you can easily integrate the repository with
[Zenodo](https://zenodo.org/), which archives the repository when you
make a tag and assigns a digital object identifier (DOI) to each release.
You might also want to
make releases to the OBO Foundry or BioPortal. You might also want to
register your prefix at Identifiers.org to give your CURIEs maximum
legitimacy.

Even with the best intentions, you will inevitably have to change some
names over time. This is okay because your identifiers are persistent!
However, you might have to retire entries. This might mean adding an
additional column to *entities.tsv* with the date that a term is made
obsolete.

---

You can't compete with UniProt, the Disease Ontology, the Gene Ontology, or
other groups that exist to maintain high quality resources.

So don't.

Join them.

Make sure that your ontology is written well so the relevant parts can be
incorporated into these and other high quality, maintained ontologies. Then,
get in touch with their maintainers. Tweet at them, send GitHub issues, etc.
They'll be happy to get input on what they should do next, because, like I said
before, these people love what they do. And there's nothing better than seeing
that something you are proud of is useful for other people.

Stay tuned for my next post where I'll give you the code I wrote to do all of
the things I recommended before. I'll put my money where my mouth is and
present my ontology that led to building this curation environment and
ultimately writing this post - the [Curation of Neurodegeneration Supporting
Ontology](https://github.com/pharmacome/conso).
