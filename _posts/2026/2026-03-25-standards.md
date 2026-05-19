---
layout: post
title: Standards are about Community Work
date: 2026-05-19 13:08:00 +0200
author: Charles Tapley Hoyt
tags:
  - knowledge graphs
  - community building
---

In late March 2026, Bruce Herr
[shared](https://obo-communitygroup.slack.com/archives/C01DP18L5GW/p1774444307246689)
on the OBO Community Slack that the USA National Institute of Health (NIH)
Common Fund Data Ecosystem (CFDE) issued a
[request for comments](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw/edit?pli=1&tab=t.0)
for a proposed knowledge graph exchange format entitled _JSON Knowledge Graph
Exchange Format (JKG)_.

Bruce also posed the obvious question: why develop a new standard instead of
reusing an existing one or collaborating to extend or improve an existing one to
a new use case? While Bruce's message specifically mentioned
[Knowledge Graph Exchange (KGX)](https://github.com/biolink/kgx) as an existing
standard from the Monarch / LinkML community, there also exist a myriad of
others including [JSON Graph Format (JGF)](https://jsongraph.github.io),
[Cytoscape Exchange (CX)](<https://cytoscape.org/cx/cx2/specification/cytoscape-exchange-format-specification-(version-2)/>),
others implemented in
[NetworkX](https://networkx.org/documentation/stable/reference/readwrite/index.html),
and more.

The knee-jerk reaction could easily be to reference
[XKCD:927 "Standards"](https://xkcd.com/927/), shrug, write off the effort as
needlessly redundant, then move on. However, I want to share a much more nuanced
take from [Nico Matentzoglu](https://semanticly.ai/about/) in the follow-up
discussion on the OBO Community Slack:

> [...] But it is a little weird that JKG is promoted by HubMap and KidsFirst -
> both of which are relatively close to the Monarch / LinkML ecosystem (not
> quite touch it, but close). Whether it is better or worse I don't know; it
> seems to have a lot of structure around probabilistic, quantitative
> assertions. Let me say it like this:
>
> 1. Creating a standard nowadays takes 4 hours for an experienced developer
> 2. Coordinating a bit of consortium-wide uptake (for a medium-sized consortium
>    like theirs) takes maybe 3 months of work (meetings, etc.)
> 3. Get the world to pick up a specific standard takes years.
>
> The hard work is not to make some proposal and get 4 big fish to approve it.
> The hard part is to come out of that box and convince the world with a
> powerful and mature tool ecosystem that it is worth standardizing against.

I totally agree with everything Nico said here, and I consider him a total
authority on the matter given his community-facing work in developing and
evangelizing the OBO Foundry
[Principles](https://obofoundry.org/principles/fp-000-summary.html) and
[Dashboard](https://dashboard.obofoundry.org/dashboard/index.html),
[Ontology Development Kit (ODK)](https://incatools.github.io/ontology-development-kit/),
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom),
and other standards. I want to comment on each of his points:

> But it is a little weird that JKG is promoted by HubMap and KidsFirst - both
> of which are relatively close to the Monarch / LinkML ecosystem (not quite
> touch it, but close).

This is definitely the part that's most like XKCD:927, and I've done this myself
too. The allure of starting fresh, having full control, not needing to
collaborate, and having something to point to that's your creation (instead of,
_we made minor improvements to an existing resource_) is strong. Nico and I have
had philosophical debates about this kind of thing, and his position is that
it's better to have something that works 80% percent for many use cases, but at
least everyone aligns on the standard.

> 1. Creating a standard nowadays takes 4 hours for an experienced developer

When I've taken the idealistic approach and gone the route of doing it myself,
it's usually the case that I can make something better, but then the more
important reality of his next points set in.

> 2. Coordinating a bit of consortium-wide uptake (for a medium-sized consortium
>    like theirs) takes maybe 3 months of work (meetings, etc.)

This part consumes huge amounts of time, energy, and emotional resilience. Even
if something you make is great

---

When I asked Nico if I could quote him in a blog post, he said this:

> I am happy for you to use this quote :stuck_out_tongue: Not that I am really
> an authority on the subject

Hard disagree.
