---
layout: post
title: Connecting Preprints to Peer-reviewed Articles on Wikidata
date: 2023-01-02 13:27:00 -0500
author: Charles Tapley Hoyt
tags: bibliometrics
---

After the [BioCypher](https://arxiv.org/abs/2212.13543) preprint went up on the
_arXiv_, I checked in on the
[missing co-author items](https://scholia.toolforge.org/author/Q47475003/curation#missing-coauthor-items)
list on the Scholia page that reflects
[my Wikidata entry](https://www.wikidata.org/wiki/Q47475003). In addition to the
several co-authors of the BioCypher manuscript that I don't know personally, I
was curious to see which other papers of mine did not have fully complete
co-author annotations. This post has a few SPARQL queries that I used to look
into this as well as a few ongoing questions I have about the relationship
between distinct entries for preprints and published articles.

First, I wrote two SPARQL queries for the
[Wikidata Query Service](https://query.wikidata.org):

- [co-authors of mine that are disambiguated](https://w.wiki/6BNF)
- [co-authors of mine that are _not_ disambiguated](https://w.wiki/6BNB)

There were around 200 co-authors that I had included through a painstaking
combination of manual curation and usage of the
[Author Disambiguator](https://author-disambiguator.toolforge.org) tool.
However, when I looked at the ambiguous authors, i.e., authors that only stored
by name via _author name string_
([P2093](https://www.wikidata.org/wiki/Property:P2093)) instead of by reference
to a Wikidata entry via _author_
([P50](https://www.wikidata.org/wiki/Property:P50)). At the time, this included
co-authors from only four unique manuscripts including:

1. [Democratising Knowledge Representation with BioCypher](http://www.wikidata.org/entity/Q115929717)
2. [A Simple Standard for Sharing Ontological Mappings (SSSOM)](http://www.wikidata.org/entity/Q114032935),
3. [Leveraging Structured Biological Knowledge for Counterfactual Inference: A Case Study of Viral Pathogenesis](http://www.wikidata.org/entity/Q114032921)
4. [Ontology Development Kit: a toolkit for building, maintaining, and standardising biomedical ontologies](http://www.wikidata.org/entity/Q112942500)

The appearance of the BioCypher manuscript on this list was no surprising
because we just preprinted it on _arXiv_. However, I very clearly remember
carefully curating all of the co-authors of the the other papers. After more
careful inspection, it turns out that I had indeed done this curation for the
preprints of each of these articles, but the ones appearing on the list
corresponded to duplicate Wikidata entries not for the preprints, but for the
published papers. This lead me to a couple questions, which I don't have answers
for yet:

1. Should there two different entries for a preprint and a publication?
2. What's even the right word for the dichotomy between a preprint and a
   publication? I don't think it's post-print.
3. It appears that there are multiple different entries between preprints and
   publications, so question 1) is a "perfect world" question. Since, in
   reality, there are duplicates, how should we handle them?
   - Should we connect them via some kind of relationship? I recently noticed
     Tiago Lubiana had been using _followed by_
     ([P156](https://www.wikidata.org/wiki/Property:P156)) for papers he had
     curated and have started using that myself in some cases (see notes below).
   - Should we merge these two entries into one? There are various properties
     for the identifiers within preprint servers that can help point to
     pre-prints, though preprints are given different DOIs than the publication
     so maybe this would create confusion.
   - How will this work with the advent of "overlay journals", like what _eLife_
     is doing by more heavily relying on peer review attached to existing
     preprints?
4. To what extent does this confusion affect Wikidata content related to me
   (e.g., my papers)?

In order to assess my own Wikidata cleanliness, I wrote the following SPARQL
query:

```sparql
SELECT ?preprint ?preprintDate ?followedBy ?article ?articleDate ?label
WHERE
{
  VALUES ?author { wd:Q47475003 }
  ?preprint wdt:P31 wd:Q580922 ;
    wdt:P50 ?author ;
    rdfs:label ?preprintLabel .
  ?article wdt:P31 wd:Q13442814 ;
    wdt:P50 ?author ;
    rdfs:label ?label .
  OPTIONAL { ?preprint wdt:P577 ?preprintDate }
  OPTIONAL { ?article wdt:P577 ?articleDate }
  OPTIONAL { ?preprint wdt:P156 ?followedBy }
  FILTER (LCASE(?preprintLabel) = LCASE(?label))
  FILTER (?preprint != ?article)
  FILTER (LANG(?preprintLabel) = "en")
  FILTER (LANG(?label) = "en")
}
ORDER BY DESC(?articleDate)
```

Here are the live results from running that SPARQL query, embedded via the
Wikidata Query Service:

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#%0ASELECT%20%3Fpreprint%20%3FfollowedBy%20%3Farticle%20%3Flabel%0AWHERE%20%0A%7B%0A%20%20VALUES%20%3Fauthor%20%7B%20wd%3AQ47475003%20%7D%0A%20%20%3Fpreprint%20wdt%3AP31%20wd%3AQ580922%20%3B%0A%20%20%20%20wdt%3AP50%20%3Fauthor%20%3B%0A%20%20%20%20rdfs%3Alabel%20%3FpreprintLabel%20.%0A%20%20%3Farticle%20wdt%3AP31%20wd%3AQ13442814%20%3B%0A%20%20%20%20wdt%3AP50%20%3Fauthor%20%3B%0A%20%20%20%20rdfs%3Alabel%20%3Flabel%20.%0A%20%20OPTIONAL%20%7B%20%3Fpreprint%20wdt%3AP156%20%3FfollowedBy%20%7D%0A%20%20FILTER%20%28LCASE%28%3FpreprintLabel%29%20%3D%20LCASE%28%3Flabel%29%29%0A%20%20FILTER%20%28%3Fpreprint%20%21%3D%20%3Farticle%29%0A%20%20FILTER%20%28LANG%28%3FpreprintLabel%29%20%3D%20%22en%22%29%0A%20%20FILTER%20%28LANG%28%3Flabel%29%20%3D%20%22en%22%29%0A%7D%0AORDER%20BY%20DESC%28%3FarticleDate%29" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups" ></iframe>

At the time of writing, there are 15 duplicates (based on case insensitive
string matching). I've begun curating the followed-by relationships, but am
holding out since I might be able to come up with a script to automatically
generate appropriate
[quickstatements](https://quickstatements.toolforge.org/#/).

Interestingly, the fact that these are different entries allows an alternate
view that gives insight in turnover from preprint date to publication date.
Considering that I typically preprint the paper and send for peer review
simultaneously, this is an interesting statistic.

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#%23defaultView%3ATimeline%0ASELECT%20%3Fpreprint%20%3FpreprintDate%20%3Farticle%20%3FarticleDate%20%3Flabel%0AWHERE%20%0A%7B%0A%20%20VALUES%20%3Fauthor%20%7B%20wd%3AQ47475003%20%7D%0A%20%20%3Fpreprint%20wdt%3AP31%20wd%3AQ580922%20%3B%0A%20%20%20%20wdt%3AP50%20%3Fauthor%20%3B%0A%20%20%20%20rdfs%3Alabel%20%3FpreprintLabel%20.%0A%20%20%3Farticle%20wdt%3AP31%20wd%3AQ13442814%20%3B%0A%20%20%20%20wdt%3AP50%20%3Fauthor%20%3B%0A%20%20%20%20rdfs%3Alabel%20%3Flabel%20.%0A%20%20OPTIONAL%20%7B%20%3Fpreprint%20wdt%3AP577%20%3FpreprintDate%20%7D%0A%20%20OPTIONAL%20%7B%20%3Farticle%20wdt%3AP577%20%3FarticleDate%20%7D%0A%20%20FILTER%20%28LCASE%28%3FpreprintLabel%29%20%3D%20LCASE%28%3Flabel%29%29%0A%20%20FILTER%20%28%3Fpreprint%20%21%3D%20%3Farticle%29%0A%20%20FILTER%20%28LANG%28%3FpreprintLabel%29%20%3D%20%22en%22%29%0A%20%20FILTER%20%28LANG%28%3Flabel%29%20%3D%20%22en%22%29%0A%7D%0AORDER%20BY%20DESC%28%3FarticleDate%29%0A" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups" ></iframe>

---

Usually I try and write blog posts about something I made or some insight that I
got out of working on something, but I'm not really sure where to go from here.
Ideally, I'd like to see the entirety of PubMed, PMC, other major scholarly
article indexes, arXiv, bioRxiv, other preprint servers, and other bibliographic
content automatically aligned in full on Wikidata. I've heard that there are
concerns about the technical limitations about the service so this might not be
feasible in the near future. In the mean time, if you've got some answers for my
questions, please let me know.
