My main points for why OMIM and OMIMPS should be considered different:

1. Different type of things are in each space (i.e., phenotypes in OMIM and
   abstract groupings of phenotypes in OMIMPS)
2. Different identifier pattern for each (i.e., OMIM is `^\d+$` and OMIMPS
   is `^PS\d+$`
3. Different resolution endpoints

Counterpoints:

1. MeSH has many entity types in its semantic space
2. GrassBase has a regex that obviously matches two different kinds of
   identifiers but are combine in one regex: `^(imp|gen)\d{5}$`
3. KEGG has several different entity types with different identifier patterns.
   It has not only an über-endpoint, but also several commonly used subspaces (
   e.g., kegg.pathway)

Between these and any other rules I could think of, there’s a counter-example
from a well-known and highly used resource, so I can imagine that anyone with a
strong opinion about one or more of these could on principle reject and
prescription or standard.

However, for OMIM I think the following clash illustrates why these really need
to be in different spaces:

- https://omim.org/entry/214100 (PEROXISOME BIOGENESIS DISORDER 1A (ZELLWEGER);
  PBD1A)
- https://omim.org/phenotypicSeries/PS214100 (Peroxisome biogenesis disorder)

As you can see, there are two entries that have duplicate numbers but indeed
refer to different (albeit, related) entries. One one hand, from a historical
viewpoint, I would guess that the OMIM curators realized that there are more
than one peroxisome biogenesis disorders after curating the first one and made a
shadow entry in the OMIMPS identifier space so they could start grouping them
together. On the other hand, this illustrates that you can’t think about these
identifiers the same way, otherwise why wouldn’t they just pick the next highest
unused number in the OMIM identifier space?

There are lots of excellent recommendations from Julie McMurry’s papers on what
makes “good” identifier schemes:

- “Identifiers for the 21st century: How to design, provision, and reuse
  persistent identifiers to maximize utility and impact of life science
  data” https://www.ncbi.nlm.nih.gov/labs/pmc/articles/PMC5490878/

It wouldn’t be so great to consider OMIM and OMIMPS in one semantic space
because then you have to rely on the PS prefix in the local unique identifier to
tell you what kind of thing it is (this completely punts the discussion on how
OMIM is a hugely frustrating resource with no way to download a full list of
OMIMPS entries, restrictive API access, licensing issues, etc.). In the authors’
words:

> In any case, if you opt to include type in the identifiers you issue, avoid relying on type for uniqueness: that is to say, once a local ID (e.g., 12345) is assigned it should never be recycled for another entity, even an entity of a different type (e.g., …/gene/12345 and …/patient/12345).

I doubt we will be able to engage with the OMIM curators or developers, so we
can not make arguments based on what we think they intended, but rather what we
see. There are two distinct patterns for two distinct entity types resolving on
two distinct pages. If you don’t consider the “embedded meaning” (as McMurry et
al. call it), then there are clashes.

---

A bit of meta-argumentation:

I suppose every group/resource is entitled to deciding how they want to handle
these potentially ambiguous situations. That’s what we have right now and the
consequences are that OBO Foundry ontologies, as laudable as the goals of OBO
Foundry are, are NOT interoperable. They do NOT share semantics. Different
prefixes and URI prefixes are used everywhere for the same things.

The first step towards solving the problem of interoperability is to start to
share semantics. The OBO Library PURL system is an initial step in this
direction - forcing (most) OBO Foundry ontologies to use their PURL system for
prefix/URI prefix combinations on entities from semantic spaces that find their
home in an OBO Foundry ontology. However, OBO Foundry PURL service does not have
the goal to become a standard for prefix/URI prefixes outside of its scope for a
variety of reasons.

This motivates the need for an external resource (i.e. a registry)
that arbitrates what are the canonical prefixes, the canonical URI prefixes
associated with them when used to generate URIs in semantic web applications
like ontologies, and what are the identifier patterns that go with it. Consider
Identifiers.org, which for a long time, was a golden standard external registry
of this kind of metadata. Its page for
OMIM (https://registry.identifiers.org/registry/mim) says that an OMIM entry
should have identifiers matching ^[*#+%^]?\d{6}$.

If you disagree with Identifiers.org, you’re SOL, because they do not widely
accept feedback or suggestions anymore either via their issue
tracker (https://github.com/identifiers-org/identifiers-org.github.io/issues) or
by emailing their main responsible person (AFAIK is still Henning Hermjakob).
The obvious alternative is the Bioregistry, which solves the issue of
non-responsiveness. However, it also is maintained by a
team (https://github.com/orgs/biopragmatics/teams/bioregistry-reviewers) that
also would need to be convinced of new changes. Luckily (as a side note), the
Bioregistry review team’s membership is transparent and their work is all done
on the open forum of the Bioregistry’s issue tracker and via pull request to its
GitHub repository.

If a group/resource aren’t willing to adopt an external standard without the
condition that the standard changes to support their pre-existing use case, then
this line of argumentation is a non-starter. If they also disagree with the
current state of the external standard, then they may be justified in throwing
their hands in the air and saying that deferring to an external standard is a
fool’s errand, because it doesn’t fit their needs, and they should make their
own registry (see an incomplete list of groups who may or may not have thrown
hands into the air before doing this https://bioregistry.io/metaregistry/). I
guess that’s fine, but then we’re back to issue 1, which is that we don’t have
shared semantics. Being pessimistic about the state of things, I’d be tempted to
consider that group/resource as a lost cause. I have some wildly different
theories on why this might happen:

1. Perhaps the reason a group/resource might take this position is because lots
   of people rely on their historical choices and they’re not really able to
   assess the potential impact *any* change that they make. That kind of group
   has a second, completely different problem they also have to deal with into
   which I can’t provide any insight.
2. Perhaps the group/resource might say “We don’t have time to maintain this”,
   “We don’t have money, it’s not part of an ongoing project” or some excuse
   like this, which may be true to some extent, but is more of a facade for the
   issue that it’s too hard for people to make and review contributions (
   recently coined as “drive-by curations”) without a core of highly senior
   people who used to be more involved but now just don’t have the time (
   e.g., can we make several clones of Chris Mungall?)
3. Other reasons I can’t fathom on this cloudy Thursday afternoon Ideally,
   discourse about prefixes like OMIM vs. OMIMPS would be more valuable if it
   were framed around the question of how to update the Identifiers.org or
   Bioregistry’s standard, since it would contribute towards the ability of
   people to share semantics, rather than just the internal philosophy of a
   given group/resource.

From [Nico's reply](https://obo-communitygroup.slack.com/archives/C023P0Z304T/p1643899036042579?thread_ts=1643897317.193139&cid=C023P0Z304T):

> A lot to unpack here; while I do not share all of your sentiments (e.g. OBO ontologies not interoperable is a bit too undifferentiated, neither true nor false), I do share your observation that we need to do more to facilitate drive-by curations. I disagree a bit with combining the prefix debate with a debate on the nature of the entities represented by a resource. While there is some of that (UBERON ids are expected to be anatomical entities), plenty of resources as you point out (SNOMED, MESH, UMLS etc) have idspaces spanning all sorts of entity types. So I wouldnt try to solve the OMIM/OMIMPS debate with entity types. The ID grammar is a good argument though (the preceding PS vs not). I think the cleanest path forward would be if resources lime OMIM would adopt its own purl system, with ids seeping into the wild using that, and only that (rather than URLs). But as we can see with OBO, maintaining such as system is massively difficult. And existing ones like w3id (which we use, at our own peril) are not really build in a way that you can trust that they will always be there.