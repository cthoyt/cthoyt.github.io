---
layout: post
title: Standards
date: 2026-05-19 13:08:00 +0200
author: Charles Tapley Hoyt
tags:
  - SSSOM
  - semantic mappings
  - knowledge graphs
---

In late March 2026, Bruce Herr
[shared](https://obo-communitygroup.slack.com/archives/C01DP18L5GW/p1774444307246689)
on the OBO Community Slack that the USA National Institute of Health (NIH)
Common Fund Data Ecosystem (CFDE) issued a
[request for comments](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw/edit?pli=1&tab=t.0)
for a proposed knowledge graph exchange format entitled _JSON Knowledge Graph
Exchange Format (JKG)_. Bruce also posed the obvious question: why develop a new
standard instead of reusing or collaborating on something like
[Knowledge Graph Exchange (KGC)](https://github.com/biolink/kgx),
[JSON Graph Format (JGF)](https://jsongraph.github.io),
[Cytoscape Exchange (CX)](<https://cytoscape.org/cx/cx2/specification/cytoscape-exchange-format-specification-(version-2)/>),
or others?

The knee-jerk reaction is course to reference
[XKCD:927 "Standards"](https://xkcd.com/927/) and write

This post is about a quote from Nico Matentzoglu.

> JKG seems to be rooted in the UMLS culture (at least the way the node
> attributes are named). But it is a little weird that JKG is promoted by HubMap
> and KidsFirst - both of which are relatively close to the Monarch / LinkML
> ecosystem (not quite touch it, but close). Whether it is better or worse I
> don't know; it seems to have a lot of structure around probabilistic,
> quantitative assertions. Let me say it like this:
>
> 1. Creating a standard nowadays takes 4 hours for an experienced developer
> 2. Coordinating a bit of consortium-wide uptake (for a medium-sized consortium
>    like theirs) takes maybe 3 months of work (meetings, etc.)
> 3. Get the world to pick up a specific standard takes years.
>
> The hard work is not to make some proposal and get 4 big fish to approve it.
> The hard part is to come out of that box and convince the world with a
> powerful and mature tool ecosystem that it is worth standardizing against.
