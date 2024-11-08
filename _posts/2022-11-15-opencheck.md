---
layout: post
title: A First Look at OpenCheck
date: 2022-11-15 19:39:00 +0100
author: Charles Tapley Hoyt
tags: 
- bibliometrics
- social media
---
There has been legitimate concern about the future of Twitter over the last week due to its new ownership and
management. This is pretty upsetting considering how great it's been to use to connect to and to follow other
researchers. [OpenCheck](https://web.archive.org/web/20241008073132/https://opencheck.is/) is currently
working to map Twitter handles to [ORCID identifiers](https://orcid.org) and capture the directed follow graph of researchers
on Twitter in case the service becomes unusable in the near future. This post is about my initial exploration
of the resource. **Update in November 2024** - OpenCheck has been shut down.

## How It Works

The OpenCheck website is pretty sleek. There are two big buttons to connect it to your Twitter account and ORCID
account. After authorization, it uses the Twitter API to look your followers and follows. Then, it looks up
if any of those Twitter accounts have also registered and adds it
to [this CSV](https://opencheck.is/scitwitter/orcidgraph)
which they make available under the permissive CC0 license.

## Wikidata to the Rescue

My first thought was that there are tons of ORCID-Twitter connections available under the CC0 license through Wikidata
that they could use to complement this content. The following SPARQL query retrieves all of these links:

```sparql
SELECT ?item ?itemLabel ?orcid ?twitter
WHERE 
{
  ?item wdt:P31 wd:Q5; 
        wdt:P496 ?orcid; 
        wdt:P2002 ?twitter .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

This query can be run using the Wikidata Query Service by following [this link](https://w.wiki/5xaE) and pressing
the play button. As of November 15th, 2022, it returns 13,784 results.

## Graph Machine Learning

The OpenCheck ORCID graph is a relatively small directed graph, so my second thought was that would be interesting to
apply some graph machine learning methodologies to it. I wrote a simple script
using [GRAPE](https://github.com/AnacletoLAB/grape) to learn low-dimensional vector representations (i.e., embeddings)
for nodes in the graph (i.e., ORCID identifiers) that could be useful for clustering, classification, or other
downstream machine learning tasks. These resulting embeddings for each ORCID identifier can be downloaded as a TSV file
[here](https://github.com/cthoyt/opencheck-embed/raw/main/embeddings/line.tsv) and are summarized below:

![](https://github.com/cthoyt/opencheck-embed/raw/main/embeddings/line.png)

I put this script in [cthoyt/opencheck-embed](https://github.com/cthoyt/opencheck-embed)
and additionally configured GitHub Actions to automatically re-run the script every night to generate new embeddings for
the newest dataset.

I had first tested the idea of *continuous analysis* built on top of GitHub's continuous integration
service by periodically generating [differential reaction fingerprints](https://github.com/reymond-group/drfp) on the
[Rhea reaction database](https://www.rhea-db.org) in [cthoyt/rhea-fingerprints](https://github.com/cthoyt/rhea-fingerprints).
The OpenCheck ORCID graph is a different scenario because the data are updated in real time and aren't versioned.
Overall, I think these are both good examples of what is possible using modern, public infrastructure, and I would like
to see them used in more and more scientific workflows.

---

It appears that OpenCheck is an effort from a company called [Metarational, LLC](https://www.metarational.net) run
by [John Beatty](https://twitter.com/john_d_beatty) that has has a more long-term goal of supporting
verification online (i.e., better than an $8 blue star). I'm excited to see what they do next!

If you want to make sure that your ORCID, Twitter, and other academic profiles on the internet are linked, check
out my [previous post]({% post_url 2021-08-17-self-organization %}) on curating your own Wikidata profile.
