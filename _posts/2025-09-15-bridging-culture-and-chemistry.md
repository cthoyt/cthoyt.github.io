
## Operationalizing Iconclass

[Iconclass](https://iconclass.org) is a controlled vocabulary used to annotate parts of images with what they depict. For example, [`iconclass:49E3911`](https://bioregistry.io/iconclass:49E3911) is used to annotate a part of an image depicting an *alchemist trying to make gold*. Iconclass identifiers implicitly contain the hierarchy:

- [`iconclass:49E391`](https://bioregistry.io/iconclass:49E391) is used to annotate an *alchemist at work*
- [`iconclass:49E39`](https://bioregistry.io/iconclass:49E39) is used to annotate *alchemy*
- [`iconclass:49E3`](https://bioregistry.io/iconclass:49E3) is used to annotate *chemistry*
- [`iconclass:49E`](https://bioregistry.io/iconclass:49E) is used to annotate *science and technology*
- [`iconclass:49`](https://bioregistry.io/iconclass:49) is used to annotate *education, science, and learning*
- [`iconclass:4`](https://bioregistry.io/iconclass:4) is used to annotate *Society, Civilization, Culture*

Note that unlike an ontology, the hierarchy implied by Iconclass is merely organizational and isn't (formally) logical.

[![](/img/iconclass-alchemist.png)](https://bioregistry.io/iconclass:49E391)

I added a source to PyOBO to ingest Iconclass in [biopragmatics/pyobo#433](https://github.com/biopragmatics/pyobo/pull/433). This enables it to generate ontology-like artifacts in the OWL and OBO formats, as well as gives access to the text mining utilities built on top of PyOBO.

Along the way, I found that Iconclass has a lot more weird and irregular identifiers than I had earlier assumed. I was able to make an additional pull request to the Bioregistry in [biopragmatics/bioregistry#1686](https://github.com/biopragmatics/bioregistry/pull/1686) to update the underlying regular expression pattern and add extra examples to demonstrate the weirdness. This is important because PyOBO uses the Bioregistry for regular expression validation of identifiers internally, and without this update, the Iconclass source doesn't work!

## Mappings

The [Biomappings](github.com/biopragmatics/biomappings) project provides tools for predicting semantic mappings using lexical matching. It can quickly be used to spin up a workflow for matching any two vocabularies available through PyOBO with a few lines. I gave it a try to match Iconclass to the [Chemical Methods Ontology (CHMO)](https://bioregistry.io/chmo):

```python
from biomappings.lexical import lexical_prediction_cli

if __name__ == "__main__":
    lexical_prediction_cli(__file__, "iconclass", "chmo")
```

This usually works well for matching entities in resources curated as ontologies, but because Iconclass's labels aren't typical, it wasn't able to generate more than a handfull of matches.

This prompted me to take a different approach that relies on language models to generate embeddings, which are better able to capture the subtle differences in the way entities are labeled. This lead me to making an improvement in

1. I added functionality to PyOBO to get a dataframe of embeddings for *all* entities in a given ontology or controlled vocabulary in [](https://github.com/biopragmatics/pyobo/pull/434)
2. I extended the lexical prediction workflow in Biomappings to have a method that combines embedding generation in PyOBO with similarity calculation and finally the application of a similarity cutoff for calling mappings in [](https://github.com/biopragmatics/biomappings/pull/206).

After this, I was able to update my workflow to look like this:

```python
from biomappings.lexical import lexical_prediction_cli

if __name__ == "__main__":
    lexical_prediction_cli(
        __file__,
        "iconclass",
        "chmo",
        method="embedding",
        cutoff=0.9
    )
```





2. make mappings between ICONCLASS and chemicals in ChEBI or instruments in CHMO/OBI -> then we can look up depictions of the chemicals
   1. Tried to do normal biomappings
   1. Enable PyOBO to generate full ontology embedding dataframes
   2. Hack up biomappings to do full ontology embedding-based mapping
3. automate turning SSSOM into RDF
4. Making a federated query 3 ways between chem, culture, and the bridge that finds links between culture objects tagged with icon classes mapped to chemicals mapped to notebooks.


bridging culture and chemistry
