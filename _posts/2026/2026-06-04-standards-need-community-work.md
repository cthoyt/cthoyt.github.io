---
layout: post
title: Standards Don't Succeed Without Community Work
date: 2026-06-04 09:08:00 +0200
author: Charles Tapley Hoyt
tags:
  - knowledge graphs
  - community building
---

In March 2026, the NIH
[Common Fund Data Ecosystem](https://commonfund.nih.gov/dataecosystem) issued a
[request for comments](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw/edit?pli=1&tab=t.0)
for a proposal for a knowledge graph exchange format entitled _JSON Knowledge
Graph Exchange Format (JKG)_. This post is about the burden of proposing yet
another standard and highlights sage wisdom from Nico Matentzoglu about the
importance of community work in pushing standards.

Discussion in the OBO community began after Bruce Herr
[shared](https://obo-communitygroup.slack.com/archives/C01DP18L5GW/p1774444307246689)
a link to the proposal in the OBO community Slack workspace. Along with a link
to the proposal, Bruce also posed the obvious question: why develop a new
standard instead of reusing an existing one or collaborating to extend or
improve an existing one to a new use case?

Bruce's message specifically mentioned
[Knowledge Graph Exchange (KGX)](https://github.com/biolink/kgx) as an existing
standard from the Monarch / LinkML community, but there also exist a myriad of
others including [JSON Graph Format (JGF)](https://jsongraph.github.io),
[Cytoscape Exchange (CX)](<https://cytoscape.org/cx/cx2/specification/cytoscape-exchange-format-specification-(version-2)/>),
several implemented in
[NetworkX](https://networkx.org/documentation/stable/reference/readwrite/index.html),
and more.

My knee-jerk reaction was to reference
[xkcd 927 (Standards)](https://xkcd.com/927/), shrug, write off the proposal as
needlessly redundant, then move on. However, I want to share a much more nuanced
perspective from [Nico Matentzoglu](https://semanticly.ai/about/) in the
follow-up discussion on Slack:

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

I totally agree with everything Nico said here. He is an authority with a proven
track of the success in the development and evangelization the OBO Foundry
[Principles](https://obofoundry.org/principles/fp-000-summary.html) and
[Dashboard](https://dashboard.obofoundry.org/dashboard/index.html),
[Ontology Development Kit (ODK)](https://incatools.github.io/ontology-development-kit/),
[Simple Standard for Sharing Ontological Mappings (SSSOM)](https://mapping-commons.github.io/sssom),
and other standards. Further, the International Society of Biocuration (ISB)
recognized this in 2023 by conferring on him its
[Advanced Career Award](https://www.biocuration.org/community/biocuration-career-awards/career-award-winners/).

I want to comment on each of the five parts of what Nico wrote:

> But it is a little weird that JKG is promoted by HubMap and KidsFirst - both
> of which are relatively close to the Monarch / LinkML ecosystem (not quite
> touch it, but close).

This is the part that's most like xkcd 927. From my own experience, I can say
there's a strong allure to:

1. starting a project fresh
2. having full control
3. not needing to collaborate or find consensus (see discussion of Nico's 3
   bullet points below)
4. directly addressing one's own use cases
5. finally Getting It Right
6. having something to point to that's your creation (instead of, _we made minor
   improvements to an existing resource_) which might come from, for example,
   pressure to publish for career progression or to do implicit outreach for
   your institution/employer

I can't speak towards why NIH didn't reuse, for example, KGX, but I have
observed their general hesitance to engage with, e.g., the biocuration
community, so their tendency towards reinvention doesn't surprise me.

I've also been on the receiving end of such a snub from groups that I
collaborate with or work in the same space as me , who, at minimum, should have
been aware of what I'm working on. It can hurt and be demotivating when this
happens, especially because many of us who are academic scientific software
developers are doing it because of idealism and pride in the value of our work.

> 1. Creating a standard nowadays takes 4 hours for an experienced developer

Nico and I have had philosophical debates about this kind of thing, and his
position is that it's better to have something that works 80% percent for many
use cases, but at least everyone aligns on the standard. When I've taken the
_idealistic_ approach described above and built something myself, it's usually
the case that I can make something better, but then the more important reality
of his next points set in.

> 2. Coordinating a bit of consortium-wide uptake (for a medium-sized consortium
>    like theirs) takes maybe 3 months of work (meetings, etc.)

This part consumes huge amounts of time, energy, and emotional resilience. Even
if something you make is good, it's almost never the case that the target users
are proactive looking for new standards, tools, etc. Evangelizing new tools
requires (but is not limited to):

1. contacting people, often
2. fighting for their precious attention
3. coordinating setting up meetings
4. preparing presentations and documentation
5. giving the same pitch over and over
6. rewriting presentations and documentation to cover things you missed and
   common points of confusion
7. responding to questions from an audience with a variety of backgrounds, which
   can often be frustrating due to mismatch in your expectations of what the
   audience should know and care about, and what they actually know and care
   about. You still have to be nice, even when frustrated (one reason this
   requires emotional resilience)
8. struggling with when people would rather use someone else's tool than yours,
   especially when you know yours is a better fit (another reason this requires
   emotional resilience)

This is also tough considering that funding often doesn't take any of this into
account. Most grants on which I've been funded are written towards a scientific
goal and are not explicit about the infrastructure and community work required.
Discussing why this is the case is a topic for another post.

> 3. Get the world to pick up a specific standard takes years.

Eventually, you might have some demonstrations of your thing working, some
publications to share, and even some grants that have supported the development
of your thing. If you're lucky (or cursed), then people might actually start
using your thing (assuming you keep doing the Point 2. things).

> The hard work is not to make some proposal and get 4 big fish to approve it.
> The hard part is to come out of that box and convince the world with a
> powerful and mature tool ecosystem that it is worth standardizing against.

Your mileage may vary here. I agree with Nico that talk is cheap. The most
rigorous way is to start collecting requirements, forming consensus, and
building against those expectations. But, this requires a lot of flexibility in
terms of time. But, it still might be the case that you need the right people to
support something before a powerful and mature tool ecosystem is even
considered.

Now that I made it here, I'm not so happy with that being a trailing sentiment.
I've been lucky to have been in a position in the last ten years of my career to
be flexible in the way I allocate my time, to have good mentorship (s/o again to
Nico and Melissa Haendel, who helped me get the Bioregistry/Semantic Farm off
the ground), and to have had the opportunity to improve some of the skills
listed above.

---

There's also a dark side to all of this. It's possible to build something that
is not itself excellent, but be very good at the community work and push a
standard that isn't... great.

Personally, I don't think JKG was created with best practices in linked (open)
data in mind - it has some amateur mistakes like
["id":"UBERON:0011153 CUI"](https://github.com/x-atlas-consortia/json-knowledge-graph/blob/f92fb24a54d899b4716be45f29deea0e2b677a1f/README.md?plain=1#L458),
that's almost a CURIE but looses focus right at the end with `_CUI`. I'll be sad
on the day if/when I need to work with data in this format.

NIH isn't so good at community work, so I don't think that this will be a big
deal. In general, it's even more difficult to convince a group to give up on
their own standards and adopt yours (trust me, I tried / trust me, people have
tried on me).

I assume that at some point, the RFC will get taken down. I archived it as PDF
[here](/assets/cfde-jkg-rfc.pdf).

---

When I asked Nico if I could quote him in a blog post, he said this:

> I am happy for you to use this quote 😛 Not that I am really an authority on
> the subject

Like I said above, hard disagree. Nico is definitely an authority on the
subject.
