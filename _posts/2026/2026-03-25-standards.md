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
on the OBO Community Slack that the United States National Institutes of Health
(NIH) Common Fund Data Ecosystem issued a
[request for comments](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw/edit?pli=1&tab=t.0)
for a proposed knowledge graph exchange format entitled _JSON Knowledge Graph
Exchange Format (JKG)_. This post is about the invisible effort behind making
standards, and some sage wisdom from Nico Matentzoglu.

Along with sharing the RFC, Bruce also posed the obvious question: why develop a
new standard instead of reusing an existing one or collaborating to extend or
improve an existing one to a new use case? While Bruce's message specifically
mentioned [Knowledge Graph Exchange (KGX)](https://github.com/biolink/kgx) as an
existing standard from the Monarch / LinkML community, there also exist a myriad
of others including [JSON Graph Format (JGF)](https://jsongraph.github.io),
[Cytoscape Exchange (CX)](<https://cytoscape.org/cx/cx2/specification/cytoscape-exchange-format-specification-(version-2)/>),
others implemented in
[NetworkX](https://networkx.org/documentation/stable/reference/readwrite/index.html),
and more.

The knee-jerk reaction could easily be to reference
[xkcd:927 "Standards"](https://xkcd.com/927/), shrug, write off the effort as
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
authority on the matter given his experience in community-facing work in
developing and evangelizing the OBO Foundry
[Principles](https://obofoundry.org/principles/fp-000-summary.html) and
[Dashboard](https://dashboard.obofoundry.org/dashboard/index.html),
[Ontology Development Kit (ODK)](https://incatools.github.io/ontology-development-kit/),
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom),
and other standards. Further, the International Society of Biocuration (ISB)
recognized this in 2023 by conferring on him its
[Advanced Career Award](https://www.biocuration.org/community/biocuration-career-awards/career-award-winners/).

I want to comment on several of his points:

> But it is a little weird that JKG is promoted by HubMap and KidsFirst - both
> of which are relatively close to the Monarch / LinkML ecosystem (not quite
> touch it, but close).

This is the part that's most like `xkcd:927`. I'm not so virtuous either - I've
been guilty of doing the same thing. From my own experience, I can say there's a
strong allure to:

1. starting fresh
2. having full control
3. not needing to collaborate or find consensus (see discussion of Nico's 3
   bullet points below)
4. Doing It Right This Time For The Last Time™
5. having something to point to that's your creation (instead of, _we made minor
   improvements to an existing resource_) which might come from, for example,
   pressure to publish for career progression or to do implicit outreach for
   your institution/employer

I can't speak towards why NIH didn't reuse, for example, KGX, but based on their
general hesitance to engage with the community in other things, their tendency
towards reinvention doesn't surprise me.

All that being said, I've also been on the receiving end of such a snub from
groups that I collaborate with and from groups that, at minimum, should be aware
of what I'm working on. It can hurt and be demotivating when this happens,
especially because many of us who are academic scientific software developers
are doing it because of idealism and pride in the value of our work, despite
there are often much better job prospects elsewhere.

> 1. Creating a standard nowadays takes 4 hours for an experienced developer

Nico and I have had philosophical debates about this kind of thing, and his
position is that it's better to have something that works 80% percent for many
use cases, but at least everyone aligns on the standard. When I've taken the
"idealistic" approach described above and built something myself, it's usually
the case that I can make something better, but then the more important reality
of his next points set in.

> 2. Coordinating a bit of consortium-wide uptake (for a medium-sized consortium
>    like theirs) takes maybe 3 months of work (meetings, etc.)

This part consumes huge amounts of time, energy, and emotional resilience. Even
if something you make is good, it's almost never the case that the target users
are proactive looking for new tools. Evangelizing new tools requires (but is not
limited to):

1. contacting people, often
2. fighting for their precious attention
3. coordinating setting up meetings
4. preparing presentations and documentation
5. giving the same pitch over and over
6. rewriting presentations and documentation to cover things you missed
7. responding to questions from an audience with a variety of backgrounds and
   can often be frustrating due to mismatch in your expectations of what the
   audience should know and care about, and what they actually know and care
   about. You still have to be nice, even when frustrated (one reason this
   requires emotional resilience)
8. struggling with when people would rather use someone else's tool than yours,
   especially when you know yours is a better fit (another reason this requires
   emotional resilience)
9. and so it goes 🐦

This is also tough considering that funding often doesn't take any of this into
account. It's usually "make and deliver the thing" or "do the science" and you
sneak "making the thing" in later, because you knew that "make the thing"
wouldn't be a very good selling point when applying for funding.

> 3. Get the world to pick up a specific standard takes years.

Eventually, you might have some demonstrations of your thing working, some
publications to share, and even some grants that (after waving your hands) can
be claimed to have supported the development of your thing. If you're lucky (or
cursed), then people might actually start using your thing (assuming you keep
doing the Point 2. things).

> The hard work is not to make some proposal and get 4 big fish to approve it.
> The hard part is to come out of that box and convince the world with a
> powerful and mature tool ecosystem that it is worth standardizing against.

Your mileage may vary here. I agree with Nico that talk is cheap. The best way
is to start collecting requirements, forming consensus, and building against
those expectations. But, this requires a lot of flexibility in terms of time. It
might be the case that you need the right people to support something before
even getting started.

Now that I made it here, I'm not so happy with that being a trailing sentiment.
I've been lucky to have been in a position in the last 10 years of my career to
be flexible in the way I allocate my time, to have good mentorship (s/o again to
Nico and Melissa Haendel, who helped me get the Bioregistry / Semantic Farm off
the ground), and to have a very particular set of skills, skills I have acquired
over a (very) long career, skills that make me a ~nightmare for people like you~
minimally okay fit for this kind of work.

---

There's also a dark side to all of this. It's possible to build something that
is not itself excellent, but be very good at the community work and push a
standard that isn't... great.

Personally, I don't think JKG was created with best practices in linked (open)
data in mind - it has some amateur mistakes like
["id":"UBERON:0011153 CUI"](https://github.com/x-atlas-consortia/json-knowledge-graph/blob/f92fb24a54d899b4716be45f29deea0e2b677a1f/README.md?plain=1#L458),
that's almost a CURIE but looses focus right at the end with `_CUI`. I'll be sad
on the day if/when I need to write my own code to consume content in this
format.

NIH isn't so good at community work, so I don't think that this will be a big
deal. In general, it's even more difficult to convince a group to give up on
their own standards and adopt yours (trust me, I tried / trust me, people have
tried on me).

I assume that at some point, the RFC will get taken down. I archived it as PDF
[here](/assets/cfde-jkg-rfc.pdf).

---

When I asked Nico if I could quote him in a blog post, he said this:

> I am happy for you to use this quote :stuck_out_tongue: Not that I am really
> an authority on the subject

Hard disagree.
