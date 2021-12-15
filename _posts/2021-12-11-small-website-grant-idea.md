# A call for funding to support the longevity of small life science informatics resources

During the community meeting portion of
the [14th Annual Biocuration Conference](https://www.biocuration.org/14th-annual-biocuration-conference-virtual/)
, there was a short discussion about the notably underutilized budget of
the [International Society for Biocuration](https://www.biocuration.org) that
included a call for ideas for new small funding schemes. Since a lot of recent
discussions with potential external stakeholders about the
[Bioregistry](https://bioregistry.io) have devolved into discussions about
sustainability and longevity, I realized this would be the perfect opportunity
to propose a small funding scheme to assuage these kinds of concerns for small
projects like ours.

## What do most modern curation projects look like?

As opposed to monolithic infrastructures and projects maintained by large
organizations like
the [National Library of Medicines (NLM)](https://www.nlm.nih.gov) and
the [European Bioinformatics Institute (EMBL-EBI)](https://www.ebi.ac.uk), most
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

## Drive-by curation

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

For example, I’ve been working on the Bioregistry project and many potential
users have brought up the issue of longevity, i.e., will this site still be
around in 10 years? It’s a small project and its associated costs are about
$33/year for the domain name and about estimated $37/year for the Amazon Web
Services EC2 instance that it runs on. We’ve very carefully built the code on
top of as much free, open infrastructure as possible and automated the
build/deployment/testing in a way such that the service _could_ continue to
exist without any maintenance as long as the EC2 instance is available. It might
be possible to support this small recurring cost with internal discretionary
budget, but this isn’t as reliable as a grant that has both funding and a
mandate associated with it, especially since it’s hard to avoid the fact that
most projects are pretty tied to their original creators. To support the
Bioregistry, I would even round up from my estimated $70/year to $100/year just
in case costs change. I would love to be able to ask for $1,500 to be
distributed over 15 years. This could build huge confidence in my platform.
Similarly, I hope the concept could help other people who are working on small
services the same way. Again, I would limit this kind of grant to projects that
can be easily deployed with Docker to make sure that potential applicants have
really thought about best practices for long-term maintenance. I would also
volunteer to be a reviewer for applications of grants like these because I
believe I have exceptional insight to the needs and potential red flags with
these kinds of projects.
