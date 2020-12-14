---
layout: post
title: Versioning of Biological Databases
date: 2020-12-15 00:00:00 -0800
author: Charles Tapley Hoyt
---
What can be versioned?

- Software
- Databases
- The Internet
- Coca Cola Recipe

This post is about all of the different dimensions
of verioning, including what versions look like,
where version information is stored, ...

## Anatomy of a Version

### Semantic Versioning

Resources whose version numbers follow the format 
X.Y.Z are using *semantic versioning*. The
X refers to a major version, Y to a minor verison,
and Z to a patch. Typically in software, an increase
in the major version denotes a backwards-incompatible
change to the API. With data, this is less defined, but
perhaps could be said that a major version bump should
be necessary if the data's schema (shape/format) changes.

See also: https://semver.org/

Examples: BioGrid, DrugBank

### Sort-of Semantic Versioning

Resources whose versions who follow the format
X.Y are also using *semantic versioning* but
do not use a patch.

Examples: Protein Ontology, MSigDB, miRBase

### Sequential Versioning

Examples: ChEBI, Reactome

### Calendar Versioning

ISO 8601-compliant examples: Gene Ontology, Phenotype And Trait Ontology

Other Examples: WikiPathways, DrugCentral

### Unversioned

#### Daily Build

Entrez Gene database is an example of a dataset that is built daily, and
doesn't really have version information associated with it

#### One-off

Many databases are created with the purpose of being published and forgotten
about. These often don't get a version number assigned to them.

#### Just... Missing

You know what this means

# Where is the Version Information

- Inside data
    - As structured information inside the data
        - OBO Ontologies have the `data-version` tag at the header
        - Biological Expression Langauge has the `SET VERSION` header
        - Unstandardized data like DrugBank has a section with metadata that includes the version
    - As unstructued infomration inside the data
        - Wikidata pathway GMT files contain version information in unstructured data - the GMT format
          is not so respectful of metadata
- In location information of data
    - Many OBO ontologies (if you're using GitHub as a file hosting system instead of the PURL service)
      contain a folder of releases. E.g. DOID: https://github.com/DiseaseOntology/HumanDiseaseOntology/tree/main/src/ontology/releases/2020-12-02
- In the name of the file
    - BioGRID (e.g., https://downloads.thebiogrid.org/File/BioGRID/Release-Archive/BIOGRID-4.2.192/BIOGRID-ALL-4.2.192.mitab.zip)
- On the website
    - Reactome only states the current version on the site and does not have information inside
      the locations, filenames, or the data itself :/
- No version information at all
    - Many databases maintained by small groups (such as excel sheets published as a database)
      do not have care taken for versioning, though hopefully the end of this post will give
      inspiration on how even groups working alone can do this well
      

# Where is data hosted?

- GitHub
  - Example Disease Ontology and many other OBO Foundry ontologies
- FTP server
  - miRBase
- HTTP / custom
  - BioGRID
- Archive Systems
    - Zenodo
      - OpenBioLink
    - FigShare
    - Mendeley
      - CKG

# Longevity of Versions

- All old versions available
    - BioGRID
- Select number of recent versions available (rolling)
    - PubChem Compound
- Only current version available
    - Reactome

# Automatic Identification of Current Version

- Symlink from "latest" or "current"
-