---
layout: post
title: Curating Publications on Wikidata
date: 2022-02-12 19:10:00 +0100
author: Charles Tapley Hoyt
tags: bibliometrics
---
This blog post is a tutorial on how to curate the links between a researcher and
scholarly works (e.g., pre-prints, publications, presentations) on Wikidata
using [Scholia](https://scholia.toolforge.org/) and
the [Author Disambiguator](https://author-disambiguator.toolforge.org) tool.

## Ensure content is available

While Wikidata is full of useful scholarly information, it's up to the community
to include new content. Therefore, before we go about curating links between
your Wikidata entry and your publications, we first have to ensure there are
Wikidata entries for your publications. There are several ways to do this, but
this tutorial will focus on getting the list of your publications from your
citation manager.

This tutorial will assume you're using [Mendeley](https://www.mendeley.com), a
citation manager that can export EndNote XML documents. This tutorial might be
later extended to include an example with [Zotero](https://www.zotero.org/),
which can also export EndNote XML documents. After opening the application,
follow these instructions:

![](/img/wikidata-publications/mendeley.png)

1. Select the publications you want to put into Wikidata
2. Right click on one of them
3. Select "export"
4. Choose "EndNote XML" as the filetype

## Uploading to Wikidata

1. Create an account on [Wikidata](https://www.wikidata.org). Keep in mind this
   is _not_ the same as the Wikidata entry about you.
2. Store your Wikidata credentials in a configuration file
   at `~/.config/wikidata.ini` (where `~` means your home directory). It should
   look like:

   ```ini
   [wikidata]
   username = <your username here>
   password = <your password here>
   ```
3. Install [Python](https://www.python.org).
4. Run the following in your terminal:

   ```shell
   $ pip install citation-url[endnote]
   $ python -m citation_url.endnote <LOCAL FILE PATH TO YOUR ENDNOTE FILE>
   ```

This will now parse your EndNote XML file and do its best to populate Wikidata
with all the DOIs, PubMed identifiers, PMC identifiers, arXiv identifiers, PDF
links, and other references.

## Update your Wikidata entry

This tutorial already assumes you've created a Wikidata entry. If you haven't
done this already, go back and read
[this tutorial]({% post_url 2021-08-17-self-organization %}). Before continuing,
make sure that you've edited the "synonyms" on your Wikidata entry so it has a
wide variety of how your name might have been written in publication. This means
different ordering of first/last name, different usages of single letters versus
writing out in full, sometimes omitting the middle name, using dots after
letters or not, etc.

![](/img/wikidata_researcher_synonyms.png)

This step is crucial because the curation interface in the next step relies on
direct string matching between this list of synonyms and what the Wikidata
Integrator was able to pull from CrossRef, EuropePMC, and other metadata
resources.

## Curate Wikidata using the Author Disambiguator

1. Follow
   [this link](https://author-disambiguator.toolforge.org/names_oauth.php?action=authorize)
   to sign in to the Author Disambiguator tool using your Wikidata
   username/password. We'll need this for later steps.
2. [Scholia](https://scholia.toolforge.org) is a frontend for navigating
   scholarly data within Wikidata. Navigating to your Scholia curation by
   replacing `<YOUR Q NUMBER>`
   in `https://scholia.toolforge.org/author/<YOUR Q NUMBER>/curation#missing-author-resolving`
   with your Wikidata identifier. It starts with a Q followed by some numbers
   coming directly after the title on your page. For example, mine
   is `Q47475003`. You can
   follow [this link](https://scholia.toolforge.org/author/Q47475003/curation#missing-author-resolving)
   to see my curation page on Scholia as an example to make sure you're in the
   right place for yours.
3. Click the link next to the specific text string you want to curate:

   ![](/img/wikidata-publications/scholia-interface.png)
4. This will bring you to
   the [Author Disambiguator](https://author-disambiguator.toolforge.org) page.
   Click the checkboxes on the publications that are yours (1), or use the boxes
   to check entire groups (2).

   ![](/img/wikidata-publications/select.png)
5. Scroll down past all the check boxes to the section labeled
   _Potential Author Items_. Select the radio box corresponding to your Wikidata
   entry (1), then click _Link Selected Works to Author_ (2).

   ![](/img/wikidata-publications/finish.png)
6. A new window will appear so you can track the status of the job, but you can
   close it and it will finish in the background. Give a few minutes, then your
   profile on Scholia will be updated.
