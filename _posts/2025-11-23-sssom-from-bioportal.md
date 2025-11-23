---
layout: post
title: Extracting Semantic Mappings from BioPortal in SSSOM
date: 2025-11-23 12:08:00 +0100
author: Charles Tapley Hoyt
tags:
  - BioPortal
  - OntoPortal
  - SSSOM
---

Earlier this week, a
[question](https://obo-communitygroup.slack.com/archives/C0281J34Z6J/p1763636752508639)
was asked on OBO Foundry Slack on where to find semantic mappings to terms in
the
[Systematized Nomenclature of Medicine - Clinical Terms (SNOMED-CT)](https://bioregistry.io/registry/snomedct).
While some are available in the
[SeMRA Disease Mappings Database](https://doi.org/10.5281/zenodo.11091885),
there are many more available within BioPortal, which has access to the entire
SNOMED-CT source data and has produced semantic mapping predictions using
[LOOM](https://pubmed.ncbi.nlm.nih.gov/20351849). This post is about how I
implemented an API wrapper for generic OntoPortal instances' mapping endpoints
and a post-processing pipeline that converts OntoPortal's custom mapping format
into SSSOM.

## Interacting with BioPortal

BioPortal is an instance of a more generic backend called
[OntoPortal](https://ontoportal.org). I've previous developed
[`ontoportal-client`](https://github.com/cthoyt/ontoportal-client), a Python
package that both has a generic wrapper for any OntoPortal's API and
pre-configured wrappers for [BioPortal](https://bioportal.bioontology.org),
[AgroPortal](https://agroportal.lirmm.fr),
[EcoPortal](https://ecoportal.lifewatch.eu), and several others.

The OntoPortal API endpoint for retrieving mappings is `/mappings`, which takes
a comma separated pair of two ontologies as a parameter like in
`https://data.bioontology.org/mappings?apikey=<API KEY>&ontologies=SNOMEDCT,AERO`.
I was able to relatively easily implement this in `ontoportal-client` in
[cthoyt/ontoportal-client#10](https://github.com/cthoyt/ontoportal-client/pull/10),
which enables automatically paging through results using the following code:

```python
from ontoportal_client import BioPortalClient

# follow https://github.com/cthoyt/ontoportal-client?tab=readme-ov-file#%EF%B8%8F-configuration
# to configure BioPortalClient to be instantiated without need for explicit configuration
client = BioPortalClient()
for record in client.get_mappings("SNOMEDCT", "AERO"):
    pass
```

Each `record` is a dictionary object corresponding to the JSON returned by the
API (after stripping pagination metadata):

```json
{
  "id": null,
  "source": "LOOM",
  "classes": [
    {
      "@id": "http://purl.obolibrary.org/obo/ogms/OMRE_0000023",
      "@type": "http://www.w3.org/2002/07/owl#Class",
      "links": {
        "self": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023",
        "ontology": "https://data.bioontology.org/ontologies/AERO",
        "children": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/children",
        "parents": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/parents",
        "descendants": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/descendants",
        "ancestors": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/ancestors",
        "instances": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/instances",
        "tree": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/tree",
        "notes": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/notes",
        "mappings": "https://data.bioontology.org/ontologies/AERO/classes/http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023/mappings",
        "ui": "http://bioportal.bioontology.org/ontologies/AERO?p=classes&conceptid=http%3A%2F%2Fpurl.obolibrary.org%2Fobo%2Fogms%2FOMRE_0000023",
        "@context": {
          "self": "http://www.w3.org/2002/07/owl#Class",
          "ontology": "http://data.bioontology.org/metadata/Ontology",
          "children": "http://www.w3.org/2002/07/owl#Class",
          "parents": "http://www.w3.org/2002/07/owl#Class",
          "descendants": "http://www.w3.org/2002/07/owl#Class",
          "ancestors": "http://www.w3.org/2002/07/owl#Class",
          "instances": "http://data.bioontology.org/metadata/Instance",
          "tree": "http://www.w3.org/2002/07/owl#Class",
          "notes": "http://data.bioontology.org/metadata/Note",
          "mappings": "http://data.bioontology.org/metadata/Mapping",
          "ui": "http://www.w3.org/2002/07/owl#Class"
        }
      },
      "@context": {
        "@vocab": "http://data.bioontology.org/metadata/",
        "@language": "en"
      }
    },
    {
      "@id": "http://purl.bioontology.org/ontology/SNOMEDCT/3415004",
      "@type": "http://www.w3.org/2002/07/owl#Class",
      "links": {
        "self": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004",
        "ontology": "https://data.bioontology.org/ontologies/SNOMEDCT",
        "children": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/children",
        "parents": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/parents",
        "descendants": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/descendants",
        "ancestors": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/ancestors",
        "instances": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/instances",
        "tree": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/tree",
        "notes": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/notes",
        "mappings": "https://data.bioontology.org/ontologies/SNOMEDCT/classes/http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004/mappings",
        "ui": "http://bioportal.bioontology.org/ontologies/SNOMEDCT?p=classes&conceptid=http%3A%2F%2Fpurl.bioontology.org%2Fontology%2FSNOMEDCT%2F3415004",
        "@context": {
          "self": "http://www.w3.org/2002/07/owl#Class",
          "ontology": "http://data.bioontology.org/metadata/Ontology",
          "children": "http://www.w3.org/2002/07/owl#Class",
          "parents": "http://www.w3.org/2002/07/owl#Class",
          "descendants": "http://www.w3.org/2002/07/owl#Class",
          "ancestors": "http://www.w3.org/2002/07/owl#Class",
          "instances": "http://data.bioontology.org/metadata/Instance",
          "tree": "http://www.w3.org/2002/07/owl#Class",
          "notes": "http://data.bioontology.org/metadata/Note",
          "mappings": "http://data.bioontology.org/metadata/Mapping",
          "ui": "http://www.w3.org/2002/07/owl#Class"
        }
      },
      "@context": {
        "@vocab": "http://data.bioontology.org/metadata/",
        "@language": "en"
      }
    }
  ],
  "process": null,
  "@id": "",
  "@type": "http://data.bioontology.org/metadata/Mapping"
}
```

There's both a lot of noise in this output and several pieces of key information
that need to be inferred. When designing `ontoportal-client` (and other similar
wrappers), I've had to grapple with staying true to the source, versus injecting
logic that processes and makes useful. For now, I've decided that
`ontoportal-client` shouldn't make any judgments on the data that comes out of
the API. Also, since I wrote the package, the format has changed as well, and I
am not super interested in taking on that maintenance burden (which makes the
suggestion in
[cthoyt/ontoportal-client#3](https://github.com/cthoyt/ontoportal-client/issues/3))
difficult to address.

## Converting to SSSOM

If not in `ontoportal-client`, then where should I put the code that processes
OntoPortal mappings? I had two options. The first is in the Semantic Mapping
Reasoner and Assembler ( SeMRA; [code](https://github.com/biopragmatics/semra),
[paper](https://doi.org/10.1093/bioinformatics/btaf542)), which is a generic
place for assembling semantic mappings. At the time, I designed the internal
data model in SeMRA to go beyond what's possible in SSSOM because I was
interested in keeping track of provenance of how semantic mappings were used to
infer other ones. Slowly, I'm porting out the SSSOM-specific code from SeMRA
into a stand-alone library,
[`sssom-pydantic`](https://github.com/cthoyt/sssom-pydantic). This serves as an
alternative to the [`sssom-py`](https://github.com/mapping-commons/sssom-py)
(which I also help maintain) that is more focused on creating a reusable and
high-performance data structure based on Pydantic.

Therefore, I implemented processing around a generic OntoPortal client in
[cthoyt/sssom-pydantic#14](https://github.com/cthoyt/sssom-pydantic/pull/14). It
can be used like this (warning: subject to change):

```python
import bioregistry
from sssom_pydantic.contrib.ontoportal import from_bioportal
from sssom_pydantic import SemanticMapping

converter = bioregistry.get_converter()
mappings: list[SemanticMapping] = from_bioportal("SNOMEDCT", "AERO", converter=converter)
```

You have to bring your own `curies.Converter` because OntoPortal's data model
doesn't return a meaningful prefix map for parsing IRIs. The Bioregistry is a
good and quick way to get a comprehensive prefix map.

Warning: BioPortal doesn't provide an option to only return mappings between
entities defined in the two given ontologies. For example, if you ask for
mappings between `SNOMEDCT` and `AERO`, you will also get mappings between OGMS
and SNOMEDCT (because OGMS terms are imported in AERO). This means that you
should probably apply post-hoc filtering to only retain relevant mappings.

One way to do this is to rely on the definition of the converter, since any
mappings with subject or objects with URIs that can't be parsed are discarded:

```python
import curies
from sssom_pydantic.contrib.ontoportal import from_bioportal

converter = curies.Converter.from_prefix_map(
    {
        "AERO": "http://purl.obolibrary.org/obo/AERO_",
        "SNOMEDCT": "http://purl.bioontology.org/ontology/SNOMEDCT/",
    }
)
mappings = from_bioportal("SNOMEDCT", "AERO", converter=converter)
```

## Bulk Download

Ideally, I could get _all_ mappings from BioPortal in bulk, instead of needing
to hit the mappings API many times for each pair of two ontologies. The
motivation for this post originally came from a question on the OBO Foundry
Slack about where one could get SNOMED-CT mappings, so I wrote the following
script to go through all ontologies in the Bioregistry that have BioPortal
alignment to check for semantic mappings from SNOMED-CT to that mapping.

```python
import bioregistry
import click
import pystow
import requests.exceptions
import sssom_pydantic
from sssom_pydantic import MappingSet
from sssom_pydantic.contrib.ontoportal import from_bioportal
from tqdm.contrib.logging import logging_redirect_tqdm
from tqdm import tqdm

MODULE = pystow.module("semra", "bioportal")
internal_to_bioportal = bioregistry.get_registry_map("bioportal")
converter = bioregistry.get_converter()

for internal, bioportal in tqdm(sorted(internal_to_bioportal.items())):
    if bioportal == "SNOMEDCT":
        continue
    name = f"snomedct-{internal}.sssom.tsv"
    path = MODULE.join(name=name)
    if path.is_file():
        tqdm.write(click.style(f"{bioportal} already cached to {path}", fg="green"))
        continue
    tqdm.write(click.style(bioportal, fg="green"))
    metadata = MappingSet(id=f'https://w3id.org/biopragmatics/mappings/bioportal/{name}')
    with logging_redirect_tqdm():
        try:
            mappings = from_bioportal("SNOMEDCT", bioportal, converter=converter)
        except requests.exceptions.HTTPError:
            tqdm.write(click.style(f"failed on {bioportal}\n", fg="red"))
        else:
            tqdm.write(click.style(f"{bioportal} got {len(mappings):,} mappings", fg="green"))
            if mappings:
                sssom_pydantic.write(mappings, path, converter=converter, metadata=metadata)
                tqdm.write(click.style(f"{bioportal} wrote to {path}\n", fg="green"))
```

As of writing, I haven't been able to get this script to run to completion. The
BioPortal API is often slow and gives timeouts. I included caching so I could
resume after failure. As I mentioned earlier, this script doesn't yet
post-process mappings to the correct subset.

---

Thanks to John Graybeal for the suggestion on where to begin. He's also helped
me get in touch with the BioPortal team, so hopefully we can collaborate to get
the API working using SSSOM directly or at least to get a bulk export of
mappings.
