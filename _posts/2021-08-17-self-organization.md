---
layout: post
title: Organizing the Public Data about a Researcher
date: 2021-08-17 12:21:00 +0100
author: Charles Tapley Hoyt
tags: bibliometrics
---
In a [previous post]({% post_url 2021-01-17-organization-organization %}), I described how to formalize the information
about a research organization using Wikidata. This post follows the same theme, but about this time about a given
researcher. Not only can you follow this post to make your own scientific profile easier to find and navigate, but you
can also use Wikidata to improve the profiles of your co-workers and collaborators.

There are several _other_ places besides Wikidata for putting your scholarly profile. The first (and worst) is by making
a resume in an awful Word document or PDF. Much like what ends up in english prose in scientific texts, this is where
knowledge goes to die. The next less bad is to put it in a closed repository like [LinkedIn](https://www.linkedin.com)
, [ResearchGate](https://www.researchgate.net), [Scopus](https://www.scopus.com), [Loop](https://loop.frontiersin.org/)
or one of many others. These might be nice, but don't forget they're companies and do not want people to be able to use
their troves without paying up. The runner-up is [ORCID](https://orcid.org), which is absolutely amazing for providing
persistent identifiers to individuals, linking published work in high-profile repositories like PubMed, and in some
cases linking grants. While it will be the cornerstone of this tutorial, it ultimately falls short as a tool for
integrating the wide variety of information available about any given researcher. So who's the winner? Wikidata, of
course! It has an incredible flexibility for creating new relationships and a first-class notion of scholarly works,
awards, affiliations, employers, and the relationships between them that make it a perfect place for storing
information.

Anyone can edit Wikidata, meaning you can create an entry for your curmudgeonly PI who wouldn't be caught dead making a
profile on this new thing called "the internet". Even better, there are several people in the bibliometrics community
who have created bots for importing and aligning information from external sources that make the entries that you supply
so much more rich overnight (e.g., some bots automatically translate the descriptions of pages into new languages, some
import publication metadata, some align identifiers with external resources).

Let's get to it.

## Step 1: ORCID

The ORCiD identifier is the single unambiguous identifier for each researcher. If you don't have one, it literally takes
2 minutes to make one [here](https://orcid.org/register). ORCID profiles look like a bunch of sets of 4 numbers/letters
with dashes between them. Mine is [0000-0003-4423-4370](https://bioregistry.io/orcid:0000-0003-4423-4370). You can use a
resolver like the Bioregistry to look up web pages on ORCID IDs with links that look like
[https://bioregistry.io/orcid:0000-0003-4423-4370](https://bioregistry.io/orcid:0000-0003-4423-4370) or more
specifically use ORCID's web address directly
like [https://orcid.org/0000-0003-4423-4370](https://orcid.org/0000-0003-4423-4370).

It's super intuitive how to put information in here. There are a few minimal things to include to make it possible for
people to find you:

1. Include any variations on your name that might appear in publications. In my professional life, I write out my name
   in full, including my middle name, but there are all sorts of variations that pop up including:
    - Charles Hoyt
    - C.T. Hoyt
    - C. Hoyt
    - Hoyt, C.T.
    - Hoyt, C.
    - Hoyt, Charles Tapley
2. Include your education. Since most people reference their highest academic degree in prose, this again helps people
   find you and disambiguate you from other people. Even ORCID knows about this

<blockquote class="twitter-tweet" data-partner="tweetdeck"><p lang="en" dir="ltr">As unique as you are, the truth is your name probably isn’t all that unique. ORCID was founded specifically to help solve the problem of name ambiguity in research. Want to learn more? Start here! <a href="https://twitter.com/hashtag/openscience?src=hash&amp;ref_src=twsrc%5Etfw">#openscience</a> <a href="https://twitter.com/hashtag/openresearch?src=hash&amp;ref_src=twsrc%5Etfw">#openresearch</a> <a href="https://twitter.com/hashtag/namedisambiguity?src=hash&amp;ref_src=twsrc%5Etfw">#namedisambiguity</a><a href="https://t.co/Q2J1bVrolc">https://t.co/Q2J1bVrolc</a></p>&mdash; ORCID Organization (@ORCID_Org) <a href="https://twitter.com/ORCID_Org/status/1427578459258249245?ref_src=twsrc%5Etfw">August 17, 2021</a></blockquote>

I happen to spend extra time to maintain my [ORCID profile](https://bioregistry.io/orcid:0000-0003-4423-4370), and
here's what it looks like:

[![ORCID](img/orcid_page.png)](https://bioregistry.io/orcid:0000-0003-4423-4370)