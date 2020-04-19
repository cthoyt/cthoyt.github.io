---
layout: post
title: Inspector Javert's Xref Database
date: 2020-04-19 00:00:00 -0800
---
On top the issue of [resolving identifiers to their names]({% post_url 2020-04-18-ooh-na-na %}), 
the bioinformatics community has a hard time figuring out when two identifiers from different
databases are equivalent. You know who else has the same problem? Inspector Javert.
Get ready for a *Les Miserables*-themed post on how to address this long-standing problem.

I have to start my tale of woes by disclosing my source material. I loved both the
1985 and 1987 recordings from the respective original London and Broadway casts.
But, for the purposes of this post, I will assume that you've seen the excellent 2012 film adaptation
of Alain Boublil, Jean-Marc Natel, and Herbert Kretzmer's musical adaptation of Victor Hugo's
novel *Les Miserables* and tell the story through that perspective. I also want to you to know that
I enjoyed Russell Crowe's Inspector Javert very much.

*Les Miserables* begins with the Work Song, in which the protagonist, ``prisoner:24601``
is confronted by Inspector Javert while doing some... work. He insists he has a name,
Jean Valjean and his identifier in his [home village](https://en.wikipedia.org/wiki/Faverolles,_Aisne)'s
fictional database (that I just retconned) was ``faverolles:2468``. Javert isn't interested in his name.
It's enough that he has a cross-reference between ``faverolles:2468`` is equivalent to ``prisoner:24601``.
He was only there to inform Jean Valjean that his parole has begun and issues him a *passeport jaune*
(yellow ticket) for the commune of [Pontarlier](https://en.wikipedia.org/wiki/Pontarlier).

I'm sure this passport also had an identifier on it. I'm going to take a bit of creative freedom and
say it was ``pontarlier:25791``. It probably also had Jean Valjean's prisoner number on it so
everybody knew he was in the 1800's fictional French convict database. The fictional 1800's French took
maintaining cross-references very seriously.

Jean Valjean never made it to Pontarlier. Instead, he broke his parole, forged
some new documents, and went to Montreuil-sur-Mer under the new name of Monsieur Madeleine. It's probably
the case that his identifier for the Montreuil-sur-Mer city database was ``montreuil-sur-mer:1357``,
or something like this (more retcons!). It must have been a good fake, because even the king of France
recognized him (note: this plot point did not appear in the film).

Javert figured out Jean Valjean broke his parole basically immediately and set out on his quest to
find and capture ``prisoner:24601`` once again. Until this point, Javert has access to the prisoner
registry and yellow tickets. He knows ``prisoner:24601`` is the same as both ``faverolles:2468`` and
``pontarlier:25791``.

The part that will hit close to home for many bioinformaticians is that when Javert goes to
Montreuil-sur-Mer, he meets Monsieur Madeleine. He is unaware that it is Jean Valjean. There is no
cross-reference between ``faverolles:2468`` and ``pontarlier:25791`` or ``montreuil-sur-mer:1357``.
If there were a cross-reference in the fictional French 1800's inspector database, Javert could
have arrested Jean Valjean on sight.  Instead, Javert had to the hard work of curating cross-references
himself and finding out who was the same in the ``montreuil-sur-mer`` database as ``prisoner:24601``.
Admittedly, he probably would have called this *inspecting*.

The next part that will hit even closer to home for many bioinformaticians is that after his
inspecting, Javert actually identified the wrong guy! This lead to one of the my favorite songs in
musical theater ever ([Who Am I?](https://www.youtube.com/watch?v=izuD30Cp5Ao)), where Monsieur Madeleine
(``montreuil-sur-mer:1357``, also actually Jean Valjean, but Javert didn't yet realize this) admits that
he is actually ``prisoner:24601``. In this extended metaphor of a blog post, Jean Valjean's confession in
"Who Am I" is effectively the same as a database providing its own cross-references to other database. Would
be nice if everyone did this, and did it well, huh? 

You should know that Javert is a powerful cross-reference reasoning machine. He already knew 
``faverolles:2468`` was the same as ``prisoner:24601``. Now he knew that ``montreuil-sur-mer:1357``
was the same as ``prisoner:24601``. This way, he could infer that ``montreuil-sur-mer:1357`` (Monsieur Madeleine)
is actually ``faverolles:2468`` (Jean Valjean). One of the nice properties of cross-references is that
they're transitive through any number of connections. We'll take advantage of this fact later. You'll
also have to excuse the fact that throughout this post, I'm operating under the assumption that "cross-references" and
"equivalences" are the same thing. That's not always true, and sometimes it can even get you in trouble. For example, 
provenance can be a cross-reference, disease-gene associations are considererd as cross-references in MONDO
(I think), and OBO even gives specific semantics for when you should consider this assumption valid. We'll just
have to live with it for now.

Javert might have got lucky that Jean Valjean revealed himself once, but the show must go on! 
Jean Valjean had many more songs to sing and thus had to escape from Montreuil-sur-Mer to Paris.
This meant that Javert has to find *another* mapping to Jean Valjean's new ``paris`` identifier.
And we already know that the French 1800's inspector database of cross-references was not being maintained.
Exhausting!


---


In the bioinformatics community, we have a very similar problem to Inspector Javert. There are lots of
databases that are talking about the same things, but only a few of them provide mappings between each other.
This means that we either have to curate our own cross-references, do our best to infer new cross-references
based on ones we already have, or throw our hands in the air.

Luckily, we have a few standardized resources to fall back on. In addition to standardizing the storage
of identifier/name pairs, the OBO format standardizes the way cross-references are stored and the OBO
Foundry already contains quite a few cross-references imported from the ontologies that it covers.

One of the most difficult entity types to map from database to database are phenotypes because of
the variety of language used to describe each, the differences in semantics of how each is defined,
and the sheer number of databases. Unfortunately, some of the most popular like MeSH and to 
an extent, UMLS, NCIT, SNOMED-CT, and ICD (seemingly the culprits are mostly American!?) provide very little
accessible information. Some are even paid, so the ony cross-references that exist are externally curated ones
from other laudable sources like HP, DOID, and EFO. In fact, dealing with phenotypes is such a pain, that there is a
project called the [Monarch Initiative](https://monarchinitiative.org/) that has a huge staff trying to solve
exactly this problem and publish the results through the [Monarch Disease Ontology (MONDO)](https://github.com/monarch-initiative/mondo).
Normally, I would reference [this XKCD comic about making new standards](https://xkcd.com/927/) when hearing about
something like this. But these are dire times, and one of my opinions is that you should always
trust curators who love what they do.

There are also lots of cross-references available from databases that don't maintain their
nomenclature as an ontology. One example is [BioGRID](https://downloads.thebiogrid.org/File/BioGRID/Latest-Release/BIOGRID-IDENTIFIERS-LATEST.tab.zip),
which assigns proteins internal accession numbers, but almost all of them cross-reference out to Entrez Gene
(I counted less than 15 that didn't, and 3 of them are COVID-related, so cut them some slack). As an aside,
I don't really understand why BioGRID would go through the effort of maintaining their own accession numbers. 
In the literal handful of cases where they can't reference Entrez Gene, I think it would be better to email
the maintainers and work with them to make improvements.

It's also worth noting that excellent resources like HGNC, MGI, RGD, SGD, Ensembl, UniProt, and others in the
genome (and gene product) nomenclature do a stellar job at maintaining cross-references. So to all of the
curators and maintainers who work there, I would like to sincerely thank you.

There are also community-curated cross-references sources. One of the notable ones is from Harvard Medical School,
that's mapping MeSH identifiers to gene identifiers in the [Gilda GitHub repository](https://raw.githubusercontent.com/indralab/gilda/master/gilda/resources/mesh_mappings.tsv).
I think this is really a good time to point out that MeSH contains a bit of everything, is ubiquitous throughout
the bioinformatics community, and in my opnion is is doing a huge disservice by not providing these kinds of mappings
itself. Or, alternatively, it is, and both the Harvard guys and I have never found it. It's not impossible, but
we're all very motivated, so I think we would have found if it did. If any MeSH maintainers are reading this and want
help making this happen, I would be elated to donate my time to you to help solve this problem.

With all these data source in mind, I built an extensible pipeline in [PyOBO](https://github.com/pyobo/pyobo/blob/master/src/pyobo/xrefdb/xrefs_pipeline.py)
for extracting cross-references from entries in OBO Foundry and other cross-reference sources.
Throughout the process, I realized that these sources have an incredible variety in how they name prefixes
and how the OBO format itself has been (ab)used. I made lots of improvements, wrote extensible code that allowed
the specification of new rules through external files (and thus less code writing in the future), and did lots
more curation. I won't get into the technical part of that here, since you can read the code (if you dare).

After all that this coding, I wrote a script (just run `obo javerts-xrefs`) that
takes all available cross-references, normalizes their namespaces, normalizes their
identifiers, and dumps them in a big 'ol TSV file. 5 columns - source namespace, source
identifier, target namespace, target identifier, and provenance (ontology name or URL).
No nonsense. Get it at [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3757266.svg)](https://doi.org/10.5281/zenodo.3757266).
I'll make updates periodically as I add new sources.


---


Once you have a database of cross-references, you have actually built an undirected graph. Equivalences
go both ways, and the are transitive. This means that every connected component in an equivalence graph
represents a set of entities that are mutually equivalent. In other words, if a path exists between
two nodes in an equivalent graph, then they are equivalent.

Even better, you don't have to materialize all of the possible inferred equivalences when you 
have an equivalence graph because identifying all of the nodes in a connected component can be done
in linear time with respect to the size of the connected component, which is usually pretty small, by 
using a breadth-first or depth-first search.

Based off of that, one application of an equivalence graph is to identify all of the nodes that are
equivalent to a given node. You can also get a little tricker and identify the paths through which
the traversal must go if you want to establish an equivalency. You could even go further and weight
edges based on how much you trust the source from which they came to identify how much you should
believe in a mapping. For example, if you have a percent confidence in each mapping being right,
then the confidence in the whole pathway would be the product of the confidences.

The actual problem I set out to solve was given a set of entities, remap all of them based on a prioritized
list. For example, I might have a set of entities that contains HGNC genes, Entrez Genes, and OMIM genes.
If my favorite nomenclature consortium is Entrez, my second favorite is HGNC, and my third favorite
is OMIM and I have an equivalence database, I might want to remap all of my identifiers. This is very
important during the curation of mechanistic biology (such as with BEL), since curators will likely use all sorts of
identifiers with no clear guidelines or rules. This means that the same entity might appear twice with
different identifiers in the same curated data!

Given a priority list, you can even transform an equivalence graph into a directed graph where each identifier
has a single out edge pointing towards the identifier that is the best mapping. Then, each connected component
would become a star graph. There's actually a better data structure for this, since each entity points to exactly
one thing - a mapping. This is a more efficient data structure for storage, and if your graph is implemented
as an adjacency dictionary (becuase you're using `networkx`, right?), then you basically already have this.

I've provided an implementation for all of these in PyOBO. They can be run as a web API with
`python -m pyobo.apps.mapper`. There's a keyword argument to allow you to load the TSV from Inspector
Javert's Xref Database directly, or if you're feeling lucky, to regenerate it yourself. Below I will give
a few examples of how to use it. Later, I would also like to host this service for anyone to use.

1. Install PyOBO with `pip install git+https://github.com/pyobo/pyobo.git`
2. Download Inspector Javert's Xref Database from Zenodo, unpack it, and find the xrefs file.
3. Run the web service with `python -m pyobo.apps.mapper -x inspector_javerts_xrefs.tsv.gz`
4. Use the following code to figure stuff out!

```python
import requests

# Get all entities mapped to MAPT, including through chains of xrefs
successful_request = requests.get('http://localhost:5000/mappings/hgnc:6893').json()
"""
{
    "orphanet:123144": [
        {
            "provenance": "hgnc", 
            "source": "hgnc:6893",
            "target": "orphanet:123144"
        }
    ],
    "pr:P10636": [
        {
            "provenance": "hgnc",
            "source": "hgnc:6893",
            "target": "uniprot:P10636"
        },
        {
            "provenance": "pr",
            "source": "uniprot:P10636",
            "target": "pr:P10636"
        }
    ],
    ...
}
"""

# Keep in mind this isn't a validation service
unsuccessful_request = requests.get('http://localhost:5000/mappings/hgnc:0000').json()
# {"message": "could not find curie", "query": {"curie": "hgnc:0000"}, "success": False}

# Get all paths mapping MAPT in HGNC to Ensembl. Returns a list of paths (which are lists of xrefs)
path_request = requests.get('http://localhost:5000/mappings/hgnc:6893/ensembl:ENSG00000186868').json()
"""
[
    [
        {
            "provenance": "hgnc",
            "source": "hgnc:6893",
            "target": "ensembl:ENSG00000186868"
        }
    ]
]
"""

# Get the priority identifier for MAPT identified by Ensembl
prioritize_request = requests.get('http://localhost:5000/prioritize/cosmic:MAPT').json()
# {"found": True, "query": "cosmic:MAPT", "result": "hgnc:6893"}

# What happens when a CURIE can't be found for prioritization
unsuccessful_prioritize_request = requests.get('http://localhost:5000/prioritize/cosmic:NOPE').json()
# {"found": False, "query": "cosmic:NOPE"}
```

I'd like to give a big thanks to my high school music teacher, Ken Tedeschi, for helping me
(and basically everyone else) fall in love with Les Mis in high school. Writing about my work
was so much more fun in extended metaphor. I would also like to thank Hugh Jackman. You know,
for being Hugh Jackman.

---

I have some random afterthoughts that I think might be worth including, that I'm adding after originally
posting this.

You might be wondering why I didn't get into a discussion about the [Ontology Mapping Service (OXO)](https://www.ebi.ac.uk/about/news/announcement/industry-collaboration-ontology-mapping-service)
from the EBI. It looks to me like this project has been abandoned. Even if not, it's API has most of the same issues
that I described in a [previous post]({% post_url 2020-04-18-ooh-na-na %}).

I'm also aware of [BridgeDB](https://bridgedb.github.io), from which I think I will be able to take
inspiration to include more xrefs later. However, I think they're limited in scope, and PyOBO is more about
standardizing data so nobody has to figure out databases... again and again and again.

One glaring omission from this work is WikiData mappings. I have a plan to include curated information in the
PyOBO metaregistry that links databases to their WikiData properties. That will allow me to build an automated
framework for downloading these mappings, given the curation of the properties.
