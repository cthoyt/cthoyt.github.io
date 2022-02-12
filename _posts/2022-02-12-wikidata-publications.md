## 1. Get content in EndNote XML

### Mendeley

[Mendeley](https://www.mendeley.com) is a less open citation manager owned by
Elsevier.

![](/img/wikidata-publications/mendley.png)

1. Select your publications
2. Right click on one of them
3. Select "export"
4. Choose "EndNote XML" as the filetype

## 2. Wikidata Integration

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

## 3. Update your Wikidata Profile

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

### 4. Using

1. Navigate to your Scholia curation
   page `https://scholia.toolforge.org/author/<your Q number>/curation#missing-author-resolving`.
   You can follow
   [this link](https://scholia.toolforge.org/author/Q47475003/curation#missing-author-resolving)
   to see mine and make sure you're in the right place.
