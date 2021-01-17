---
layout: post title: Organizing the Public Data about your Organization date: 2021-01-17 17:14:00 +0100 author: Charles
Tapley Hoyt
---

## Step 1: Wikidata

[Wikidata](https://www.wikidata.org) is an open, community-curated platform of knowledge. It stores entities, their
relations to other entities, their relations to scalar values, and added context for each relationship.

There are lots of working groups that maintain its ontology (i.e., the rules for how curation should be done) around
certain domains, such representing organization structures. This means there are lots of tools already built in to
Wikidata for potential curators like you and me to create rich pages for their organizations.

One of the curation rules shared across all domains in Wikidata is that each entity should have a "type". This means on
the page for [Albert Einstein](https://www.wikidata.org/wiki/Q937), there is a relationship stating he is an instance of
a [human](https://www.wikidata.org/wiki/Q5). [instance of](https://www.wikidata.org/wiki/Property:P31)
is a special kind of entry in Wikidata called a "property". This is one of the places where the ontology lives - there
are specific rules for each property on how it should be used in a relationship, like what's allowed to be the subject
and what's allowed to be the object. For *instance of*, there are no rules about the subject. However, the object of the
relationship where *instance of* is the property should be a "class" of thing. It wouldn't make sense for the type
of another entity to be an instance of "Albert Einstein".

### Ontology for Organizations

Each of them are either subclasses of the [organization](https://www.wikidata.org/wiki/Q43229) item, parts of an
organization, or a combination of subclasses and parts of an organization. Some examples are:

- [research institute](https://www.wikidata.org/wiki/Q31855) like
  the [Fraunhofer SCAI](https://www.wikidata.org/wiki/Q1451981)
- [department](https://www.wikidata.org/wiki/Q2366457)
  like [Fraunhofer SCAI Department of Bioinformatics](https://www.wikidata.org/wiki/Q67200492)
- [university](https://www.wikidata.org/wiki/Q3918) like [Northeastern University](https://www.wikidata.org/wiki/Q37548)
- [faculty](Q180958) like
  the [Maastricht Faculty of Health, Medicine and Life Sciences](https://www.wikidata.org/wiki/Q48888910)
- [academic department](https://www.wikidata.org/wiki/Q2467461)
  like [Maastricht University Department of Bioinformatics (BiGCaT)](https://www.wikidata.org/wiki/Q19845644)
- [business](https://www.wikidata.org/wiki/Q4830453) like [Pfizer](https://www.wikidata.org/wiki/Q206921)

### Tutorial

1. Create a [new item](https://www.wikidata.org/wiki/Special:NewItem). You don't need to have a Wikidata account or be
   logged in, but there are lots of benefits, so that's highly suggested through
   [this portal](https://www.wikidata.org/w/index.php?title=Special:CreateAccount&returnto=Wikidata%3AMain+Page).
2. Input the name for the item. If you're making a page for the Northeastern Department of Chemistry, it makes most
   sense to include the name of the parent organization inside the label for the item. There are some instances where
   this isn't the case, such as the example above of the Maastricht Faculty of Health, Medicine and Life Sciences, but
   this could cause confusion. The rest of the form is pretty obvious, but if you aren't sure what to entry for the
   description, writing what kind of thing it is might be best. For the Northeastern Department of Chemistry, one might
   write "academic department"

   ![Wikidata create item page](/img/wikidata-create-item.png)
3.

## Step 2: Global Research Identifier Database

The [Global Research Identifier Database (GRID)](https://grid.ac/)

GRID is released about every three months via FigShare under
the [Creative Commons Public Domain 1.0 International licence](https://creativecommons.org/publicdomain/zero/1.0/),
which means anyone can use it any way they want.

## Step 3: Research Organization Registry

The [Research Organization Registry (ROR)](https://ror.org)
