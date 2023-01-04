---
layout: post
title: Long-term Funding for Small Biomedical Databases
date: 2023-01-04 16:32:00 +0100
author: Charles Tapley Hoyt
tags: funding longevity sustainability
---

Way back in 2021, during the annual general assembly of
the [International Society for Biocuration (ISB)](https://www.biocuration.org) at the
the [14th Annual International Biocuration Conference (Biocuration 2021)](https://www.biocuration.org/14th-annual-biocuration-conference-virtual/)
,
there was a discussion about the notably underutilized budget of the society that resulted in an informal open call for
ideas for new small funding schemes. Concurrently, discussions with external stakeholders for the relatively new
(at the time) [Bioregistry](https://bioregistry.io) project often included questions about the sustainability and
longevity of the resource. We had conservatively estimated it would cost about 100 USD/year to run the
Bioregistry site, so this seemed like the perfect opportunity to ask for a small amount funding distributed over a
relatively long period of time. This post is about the more general reality of funding for small resources in the life
sciences, how we petitioned the ISB for funding, and what happened next.

## Bioregistry Cost Estimate

The Bioregistry is an integrative registry of biomedical ontologies, databases, and other identifier resources that
is useful for standardizing the identification of biomedical concepts, making data more FAIR, and enabling data-
and knowledge integration.

It runs a fully automated nightly [workflow](https://github.com/biopragmatics/bioregistry/actions/workflows/update.yml)
that updates its data, packages its code and data, and pushes it to the Python Package Index (PyPI). We carefully
constructed this workflow to fully run on free, open infrastructure (e.g., GitHub Actions) and require little
maintenance. After running this workflow for nearly three years, we've empirically found that the maintenance effort
averages between 10-15 minutes per month for bug fixes and/or additional data curation. We won't factor this into our
initial cost estimate as this effort could be discretionary (i.e., not tied to a grant, donated by maintainers, users,
etc.).

After, the workflow builds a Docker image
and pushes it to the [biopragmatics/bioregistry](https://hub.docker.com/r/biopragmatics/bioregistry) repository
on [DockerHub](https://hub.docker.com). This image is built with the the latest Python alpine base image, which
significantly reduces non-essential components. It also has the benefit of being compatible with Docker environments
running on both Intel and ARM architectures. The final compressed image weights less than 40 MB of disk space and
runs inside Docker with about 65 MB of memory at baseline. This easily fits on a dedicated
[t4g.nano](https://aws.amazon.com/ec2/instance-types/t4/) instance on Amazon Web Services (AWS) which
costs about 37 USD/year on-demand or around 20 USD/year reserved (i.e., if you pay up front). Two or more of these
instances could be set up behind a [load balancer](https://aws.amazon.com/what-is/load-balancing/) to ensure uptime in
case one goes down, but we won't factor this into our initial cost estimate.

The `bioregistry.io` domain is registered with [Namecheap](https://www.namecheap.com) and costs about
33 USD/year. The SSL/TLS certificate for `bioregistry.io` (so it can be served with HTTPS) is managed through the
[AWS Certificate Manager](https://aws.amazon.com/certificate-manager/) and does not cost anything additional.

Finally, we're going to exclude the costs of proactive curation of the resource. The combination of import from
23+ external registries, the ability for community members to suggest new prefixes in a streamlined way, and the
decentralization of moderation effort across many institutions results in a negligible cost.

In a best case scenario, using a reserved instance and paying for a domain name brings this bill to 53 USD/year.
Duplicating the deployment behind a load balancer would bring it up to 73 USD/year. For good measures in case costs go
up, let's call it 100 USD/year. That's pretty darn cheap for a resource that's already proven useful in several
applications and is being pretty widely adopted. Most resources don't last more than two or three years (disclaimer: I'm
spit-balling here). If we got 1,000 USD, we could already promise people that this service will be running consistently
for ten years. If we got 1,500 USD, we could extend that promise to fifteen years.

In order to gauge how small this amount is, consider that the International Society of Biocuration
is currently offering [six travel grants](https://www.biocuration.org/travel-fellowship/) worth about the same amount
each to attend
the [16th Annual International Biocuration Conference (Biocuration 2023)](https://biocuration2023.github.io/).
Sure, I'm biased since the Bioregistry is my baby, but it would be difficult to argue that this is not pennies on the
dollar compared to what some other resources cost to deploy and maintain.

## What's the Problem with Funding the Bioregistry

The Bioregistry was a spin-off project of a spin-off project. A long time ago, I was working on parsing and validating
biomedical knowledge encoded in the [Biological Expression Language](https://biological-expression-language.github.io/).
In order to support the validation of names and identifiers from various ontologies and databases, I started developing
[PyOBO](https://github.com/pyobo/pyobo) as a tool for unified access to ontologies and databases. I curated extra rules
for standardizing prefixes, CURIEs, and URIs that eventually got spun out into the Bioregistry and took on a life of its
own. Each of these steps was part of a bigger project with bigger goals that weren't necessarily focused on the
development of high-quality, reusable underlying technology. But, developing high-quality, reusable underlying
technology is just the way that I think, so that's how I did it. And I took those nice tools with me from project to
project, improving them as I went. This means that the Bioregistry has now played a role in several of my recent
projects, but never sat up front and center when it came to writing grants.

So here's the more general issue: grants are usually about building new, big things with big budgets that are done
within the short timeframe of a project, then they're usually lost or forgotten. The Bioregistry is a small, important
resource that does not need massive development but it does need a long commitment to maintenance in order to provide
the stability to the community that other resources have yet been able to provide. Further, the fact that it already
exists makes it much less novel and therefore effectively disqualified from being the focus of most potential grants.

With potential costs so low, it would actually feasible for my current department,
the [Laboratory of Systems Pharmacology](https://labsyspharm.org) to commit discretionary funding external to a grant.
However, this doesn't engender trust the same as having external funding or being part of an institution that is
well-known for the longevity of its infrastructure platforms (e.g., the NIH). Further, discretionary funding
also raises questions about what happens when the main people on my team working on the Bioregistry leave,
both from a responsibility and technical perspective. This seemed to be the sentiment from potential stakeholders
of the Bioregistry that were shared at
the [Fall 2021 Workshop on Prefixes, CURIEs, and IRIs](https://biopragmatics.github.io/workshops/WPCI2021.html).

## Communication with the ISB

After thinking about all of this, I finally write up a proposal (somewhere between one and two pages) and shared
it with the executive board of the ISB. Unfortunately, I shared this on Slack and have been unable to find the original
message since you can't search Slack messages older than 90 days now. As a paraphrase, I focused on some of the
following ideas:

As opposed to monolithic infrastructures and projects maintained by large
organizations like
the [United States National Library of Medicines (NLM)](https://www.nlm.nih.gov),
the [European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk), and
the [Swiss Institute of Bioinformatics](https://www.sib.swiss), most
biocuration projects are small and limited in scope. There are several
public systems that could support many of them:

- archival systems (e.g., [Zenodo](https://zenodo.org), [FigShare](https://figshare.com))
- hosting of static sites (e.g., institutional websites, [GitHub Pages](https://pages.github.com/))
- hosting of dynamic sites (e.g., [Amazon Web Services](https://aws.amazon.com/),
  [Microsoft Azure](https://azure.microsoft.com/en-us/), [Heroku](https://www.heroku.com/),
  [Shiny](https://www.shinyapps.io/), [Google Could Platform](https://cloud.google.com/))
- domain name registration (e.g., institutional domain, [NameCheap](https://www.namecheap.com/))
- continuous integration and deployment (e.g., GitHub Actions, GitLab Pipelines)

These are relatively inexpensive and can be used to build resources that have high longevity and sustainability.
Most biocuration projects end up being one-off publications anyway and are never updated, so I suggested that the ISB
give small grants to groups that are using best practices and the above tools to create things that could have
longevity, if given appropriate small funding across a long period of time. The biggest problem facing small curation
projects and websites is that they can not acquire small amounts of long-term funding to support their technical
infrastructure (e.g., domain name hosting, cloud compute resources). It’s becoming easier to build websites for new
small biocuration projects, but again, there are small, recurring costs associated with them like paying for a domain
name and cloud compute resources. I would suggest introducing a small grant whose award would be spread across a
potentially long time (e.g., 10-15 years) to support those costs (but not explicitly not for major development nor
maintenance).

## Is this really a big deal?

My group has recently been thinking about how bad the longevity situation really is. We build the [Bioregistry Health
Report](https://biopragmatics.github.io/bioregistry/health/) that checks on a weekly basis how many prefixes' homepages
still resolve and how many URI format strings still resolve. The results were bleak - only about 27% (as of today) do.
This isn't an indictment of the badness of the Bioregistry or the registries that it imports and aligns either - it's
true that sometimes the URLs for sites change, but this number reflects the more general problem that most just go away.
I also want to S/O to Michel Dumontier's group at Maastricht that has also been thinking about the
same sort of thing, and we're working towards collaborating on a more detailed assessment.

## The Results

Unfortunately, the ISB EC didn't accept the proposal. I didn't get very direct feedback as to why, but I think the
general concept of funding research was problematic for one reason or another for their organizational structure. I'm
not discouraged, I still think this is important and will continue to write and re-write this proposal until it finally
convinces the right funding body. I'll also be touching on this point at my (hopefully accepted abstract) for
Biocuration 2023 that I posted about yesterday. Please let me know if you've got any other arguments supporting doing
this that I can include!
