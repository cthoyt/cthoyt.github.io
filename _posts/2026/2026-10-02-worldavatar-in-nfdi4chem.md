---
layout: post
title: The World Avatar, NFDI, and the Anatomy of an Open Science Contribution
date: 2026-09-24 13:45:00 +0200
author: Charles Tapley Hoyt
tags:
  - ontology
  - NFDI4Chem
  - chemistry
  - drive-by curation
  - Bioregistry
  - Semantic Farm
  - World Avatar
---

The [World Avatar](https://theworldavatar.io) project aspires to model and
simulate the real world at the chemical, municipal, and geological scales. Its
[computational chemistry ontology](https://semantic.farm/worldavatar.compchem),
[ontology for chemical kinetic reaction mechanisms](https://semantic.farm/worldavatar.kin),
and [chemical species ontology](https://semantic.farm/worldavatar.species) are
of particular interest for reuse, extension, and/or harmonization
with ontologies ued by [NFDI4Chem](https://nfdi4chem.de) and
[NFDI4Cat](https://nfdi4cat.org) (see the respective
[NFDI4Chem ontology list](https://semantic.farm/collection/0000014) and
[NFDI4Cat ontology list](https://semantic.farm/collection/0000011)).

## Background

Specifically, while working with [Mario Wolter](https://github.com/MarioWolter)
and [Robin Ströhmann](https://github.com/CodoRob) to develop an
[ontology for basis sets](https://github.com/NFDI4Chem/basis-set-exchange-ontology),
I manually curated mappings in the
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom)
format between basis sets appearing in the
[Basis Set Exchange](https://www.basissetexchange.org), the
[Gainesville Core Ontology (GC)](https://semantic.farm/gainesville.core),
the
[Elementary Multiperspective Material Ontology (EMMO)](https://semantic.farm/registry/emmo),
and Wikidata in
[NFDI4Chem/basis-set-exchange-ontology#14](https://github.com/NFDI4Chem/basis-set-exchange-ontology/pull/14).

I was also suggested to map to the World Avatar's computational chemistry
ontology, which I wasn't very familiar with, so I went to see what information
was available about it in the Semantic Farm. Initially, it had incomplete and
outdated information, including an Internet Archive link to an old version of
the ontology. I searched the web and found that the World Avatar project not
only had created a new website in the last few months, but also found that they
were maintaining their ontologies via a repository on GitHub
([TheWorldAvatar/ontology](https://github.com/TheWorldAvatar/ontology)). This
not only let me update the three existing World Avatar records in the Semantic
Farm in
[biopragmatics/bioregistry#2074](https://github.com/biopragmatics/bioregistry/pull/2074),
but also got me thinking on how I could systematically construct new records in
the Semantic Farm for _all_ World Avatar ontologies, similarly to what I did for
[SWEET](https://github.com/biopragmatics/bioregistry/pull/1772) (geology
ontologies) and [CESSDA](https://github.com/biopragmatics/bioregistry/pull/1756)
(humanities ontologies and controlled vocabularies).

## Contributing

This is where the open science story begins. It would have been nice if I could
have just written a script to download the repository, parse its ontologies,
extract their respective metadata, and construct new Semantic Farm records. But,
there were many issues that needed addressing first. Because everything was in
an open-source repository, it was time to make some
[drive by curations](https://doi.org/10.32388/KBX9VO).

### Building and Installing the TBox Generator

The first thing I noticed was that the repository contained OWL files that were
produced from CSVs using a custom World Avatar software component called the
[TBox Generator](https://github.com/TheWorldAvatar/baselib/tree/main/src/main/java/uk/ac/cam/cares/jps/base/converter).
How to download, install, or use the TBox Generator wasn't clear from the
ontologies repository, so I opened an issue
[asking for clarification](https://github.com/TheWorldAvatar/ontology/issues/42).

One of the maintainers for the repository responded promptly and pointed me
towards
[documentation](https://github.com/TheWorldAvatar/baselib/tree/main/src/main/java/uk/ac/cam/cares/jps/base/converter#building-and-running)
inside the source code for the TBox Generator. I would have never found that!

The documentation said run `mvn clean install -DskipTests`, which implicitly
meant that I should clone the repository and run Maven (`mvn`) with:

```console
$ git clone https://github.com/TheWorldAvatar/baselib.git
$ cd baselib
$ mvn clean install -DskipTests
```

This immediately failed because some of the Java dependencies were distributed
by GitHub's Maven repository, and this weirdly requires having an access token.
Neither the documentation nor the error given by Maven made this clear, so I had
to do some searching to figure it out. This must be something that you forget
about when you're in the Java universe and already have this set up, but newbies
never know it. In the end, I made a GitHub personal access token at
<https://github.com/settings/tokens/new> and adding into my `~/.m2/settings.xml`
like:

```xml
<settings>
 <servers>
   <server>
     <id>github</id>
     <username>YOUR_GITHUB_USERNAME</username>
     <password>YOUR_PERSONAL_ACCESS_TOKEN</password>
   </server>
 </servers>
</settings>
```

After I was able to download and build the software, I had to figure out the
next step on how to run it. The documentation said
`java -cp jps-base-lib.jar uk.ac.cam.cares.jps.base.converter.TBoxGeneration <path to CSV>`
should work, but again, Java is never so easy. After a lot of troubleshooting, I
learned that I additionally needed `--add-opens java.base/java.lang=ALL-UNNAMED`
incantation to make it work. Honestly, I can't remember why, but this is the
typical experience working with Java.

This was an awful lot of work before even making a contribution, but if I didn't
share my newfound wisdom, then every other contributor in the future would have
to go through the same frustrating experience. Naturally, I made a pull request
([TheWorldAvatar/ontology#44](https://github.com/TheWorldAvatar/ontology/pull/44))
that encoded the download and build commands and documentation into a justfile
that can be run by anyone.

### First Contribution - Fixing

In my first contribution, I realized that the URIs for the traffic incident and
landslide ontologies were incorrect, probably due to forgetting to update rows
copy/pasted from other ontologies. I was able to update the rows in the template
CSVs for these two ontologies in
<https://github.com/TheWorldAvatar/ontology/pull/40>.

I actually did this change before figuring out how to rebuild the ontology files
with the TBox Generator, so this contribution doesn't have corresponding OWL
updates in it. For storytelling purposes, I thought it made sense to explain the
TBox Generator first.

### Adding Missing OWL Files

I identified four ontologies that had source CSV files, but no corresponding OWL
files and opened <https://github.com/TheWorldAvatar/ontology/issues/41>. It
turns out that these CSV files had syntax and semantic issues, which I figured
out through a combination of trial-and-error running the TBox Generator and
pattern matching against how other CSVs look. It's a core skill for biocurators
to be able to do this with your own brain.

Ultimately, I updated the CSVs until they were able to produce OWL files in PR
<https://github.com/TheWorldAvatar/ontology/pull/45>.

### Fixing Existing OWL files

I identified five ontologies that had both source CSV files and OWL output
files, but the CSVs had similar syntax and semantic issues as above. I fixed
these in <https://github.com/TheWorldAvatar/ontology/pull/47/changes>/

### Rebuilding

In <https://github.com/TheWorldAvatar/ontology/pull/48>, I extended the justfile
to run in a loop to rebuild all ontologies. This fixed some inconsistencies and
also materialized the updates from my first contribution. Now, the maintainers
can easily create release products with a single command!

## Adding New Prefixes to the Bioregistry/Semantic Farm

Once the ontologies had been updated, I was ready to write a script to parse
their respective metadata and construct new Bioregistry/Semantic Farm records.
This materialized in <https://github.com/biopragmatics/bioregistry/pull/2051>.

I noticed a few interesting things along the way. First, the World Avatar
doesn't have a standard URI scheme for its ontologies, using a combination of
HTTP/HTTPs protocols and `.io`/`.com` domain names. They also use a non-standard
combination of predicates for annotating metadata onto the ontology itself. It
took several iterations, but I was able to capture these and other rules in my
script for auto-generating records. Importantly, because I was able to parse the
entire ontologies, I was able to extract the URI prefixes and example local
unique identifiers.

I also had to decide on a systematic way of assigning prefixes. The World
Avatar's were simply unusable - the project uses many short prefixes that clash
with better known resources. Luckily, the typical solution is to subspace
prefixes for projects/series like this, which remove the collisions.

## Parting Thoughts

Along the way, I realized that it would be helpful to improve the way that "part
of database" relationships get displayed in a unified way with keywords, so one
can navigate to <https://semantic.farm/keyword/worldavatar> in order to get the
whole list (code changes in
<https://github.com/biopragmatics/bioregistry/pull/2052>).

This all just goes to show that when you're working in an open source setting,
sometimes good ideas require a _lot_ of tangents. Being a good open source
citizen means that all the effort put into this benefits everyone.
