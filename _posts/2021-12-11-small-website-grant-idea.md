---
layout: post
title: Long-term Funding for Small Biomedical Databases
date: 2022-12-20 14:26:00 +0100
author: Charles Tapley Hoyt
tags: semantics
---

Back in 2021, during the annual general assembly of
the [International Society for Biocuration (ISB)](https://www.biocuration.org) at the
the [14th Annual International Biocuration Conference (Biocuration 2021)](https://www.biocuration.org/14th-annual-biocuration-conference-virtual/),
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
initial cost estimate as this effort could be discretionary (i.e., not tied to a grant, donated by maintainers, users, etc.).

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

In a best case scenario, using a reserved instance brings this bill to 53 USD/year. Duplicating the deployment behind a
load balancer would bring it up to 73 USD/year. For good measures in case costs go up, let's call it 100 USD/year.
That's pretty darn cheap for a resource that's already proven useful in several applications and is being pretty widely
adopted. Most resources don't last more than two or three years (disclaimer: I'm spit-balling here). If we got 1,000
USD, we could already promise people that this service will be running consistently for ten years. If we got 1,500 USD,
we could extend that promise to fifteen years.

In order to gauge how small this amount is, consider that the International Society of Biocuration
is currently offering [six travel grants](https://www.biocuration.org/travel-fellowship/) worth about the same amount
each to attend the [16th Annual International Biocuration Conference (Biocuration 2023)](https://biocuration2023.github.io/).
Sure, I'm biased since the Bioregistry is my baby, but it would be difficult to argue that this is not pennies on the
dollar compared to what some other resources cost to deploy and maintain.

## What's the Problem with Funding the Bioregistry



1. money goes away when grants end and they're not typically this long
2. grants are usually about building big things, with big budges, not about maintaining small things with tiny budgets
3.

With a cost this low, it's actually feasible for [my department](https://labsyspharm.org) to commit discretionary
funding that lives

## Communication with the ISB

I wrote a short proposal for the ISB about creating small, long-term funding 

Similarly, I hope the concept could help other people who are working on small
services the same way. Again, I would limit this kind of grant to projects that
can be easily deployed with Docker to make sure that potential applicants have
really thought about best practices for long-term maintenance. I would also
volunteer to be a reviewer for applications of grants like these because I
believe I have exceptional insight to the needs and potential red flags with
these kinds of projects.

have devolved into discussions about sustainability and longevity, I realized
this would be the perfect opportunity to propose a small funding scheme to assuage these kinds of concerns for small
projects like ours.

## What do most modern curation projects look like?

As opposed to monolithic infrastructures and projects maintained by large
organizations like
the [United States National Library of Medicines (NLM)](https://www.nlm.nih.gov),
the [European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk), and
the [Swiss Institute of Bioinformatics](https://www.sib.swiss) most
biocuration projects are small and limited in scope. There are several
public systems that support many of them:

- archival systems (e.g., [Zenodo](https://zenodo.org)
  , [FigShare](https://figshare.com))
- hosting of static sites (e.g., institutional
  websites, [GitHub Pages](https://pages.github.com/))
- hosting of dynamic sites (e.g., [Amazon Web Services](https://aws.amazon.com/)
  , [Microsoft Azure](https://azure.microsoft.com/en-us/)
  , [Heroku](https://www.heroku.com/), [Shiny](https://www.shinyapps.io/)
  , [Google Could Platform](https://cloud.google.com/))
- domain name registration (e.g., institutional
  domain, [NameCheap](https://www.namecheap.com/))

one-off/static updated/dynamic updated

## Major problems for small curation projects

The biggest problem facing small curation projects and websites is that they can
not acquire small amounts of long-term funding to support their technical
infrastructure (e.g., domain name hosting, cloud compute resources).

It’s becoming easier to build websites for new small biocuration projects, but
there are small, recurring costs associated with them like paying for a domain
name and cloud compute resources.

## What would make a project eligible

I would suggest introducing a small grant whose award would be spread across a
potentially long time (e.g., 10-15 years)
to support those costs (but not major development nor maintenance).
