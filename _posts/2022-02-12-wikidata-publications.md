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

## 1. Ensure content is available

### 1A. Get content in EndNote XML

[Mendeley](https://www.mendeley.com) is a citation manager that can export
EndNote XML documents.

![](/img/wikidata-publications/mendley.png)

1. Select your publications
2. Right click on one of them
3. Select "export"
4. Choose "EndNote XML" as the filetype

### 1B. Wikidata Integrator

1. Create an account on [Wikidata](https://www.wikidata.org).
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
   $ python -m citation_url.endnote <PATH TO YOUR ENDNOTE FILE>
   ```

This will now parse your EndNote XML file and do its best to populate Wikidata
with all the DOIs, PubMed identifiers, PMC identifiers, arXiv identifiers, PDF
links, and other references.

## 2. Update your Wikidata profile

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

## 3. Curation interface

1. Start by navigating to your Scholia curation by replacing `<YOUR Q NUMBER>`
   in `https://scholia.toolforge.org/author/<YOUR Q NUMBER>/curation#missing-author-resolving`
   with your Wikidata identifier. It's starts with a Q followed by some numbers
   coming directly after the title on your page. For example, mine
   is `Q47475003`. You can
   follow [this link](https://scholia.toolforge.org/author/Q47475003/curation#missing-author-resolving)
   to see my curation page on Scholia as an example to make sure you're in the
   right place for yours.
2. Click the link next to the specific text string you want to curate:

   ![](/img/wikidata-publications/scholia-interface.png)
4. This will bring you to
   the [Author Disambiguator](https://author-disambiguator.toolforge.org) page.
   If it prompts you to sign in to Oauth2 with Wikidata, just follow the
   prompts. You might have to go back to Step 1 if it doesn't redirect you
   properly (sorry). Remember, your Wikidata account is not the same as the
   Wikidata entry about you.
5. Select which publication(s) (or use the boxes to check entire groups) are in
   fact yours
6. Select the radio box corresponding to your Wikidata entry (1), then click "
   Link Selected Works to Author" (2)

   ![](/img/wikidata-publications/scholia-interface.png)
