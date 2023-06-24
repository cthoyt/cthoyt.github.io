---
layout: post
title: Modeling and Querying Awards in Wikidata
date: 2023-06-08 12:09:23 +0200
author: Charles Tapley Hoyt
tags: wikidata bibliometrics
---

I was recently nominated for the International Society for
Biocuration's [Excellence in Biocuration Early Career Award](https://www.biocuration.org/excellence-in-biocuration-early-career-award-2023/)
(results will be announced on June 14<sup>th</sup>!).
This made me curious about how to model nominations and awards on Wikidata. In this post, I'll describe how to curate
awards, nominations, recipients, and how to make SPARQL queries to get them.

## Summarizing an Individual

I'm going to use SPARQL with the [Wikidata Query Service](https://query.wikidata.org/) to see what's already in
Wikidata. First, I want to find all of the awards that I've personally received using the
[P166 (award received)](https://www.wikidata.org/wiki/Property:P166) property. Note that the following query also
takes advantage of Wikidata's reification so I can reach into the qualifiers of each statement to figure out when
the award was given.

```sparql
SELECT ?award ?awardLabel ?year ?conferer ?confererLabel
WHERE { 
  VALUES ?person { wd:Q47475003 }
  ?person p:P166 ?award_statement .
  ?award_statement ps:P166 ?award .
  OPTIONAL { ?award wdt:P1027 ?conferer . }
  OPTIONAL { 
    ?award_statement pq:P585 ?date . 
    BIND(year(?date) AS ?year)
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

See this query in action at [https://w.wiki/6odU](https://w.wiki/6odU).

As of time of writing, the only award that is listed here is the Bernie Lemire Award. This was given to me by
the Northeastern University Department of Chemistry at the end of my bachelor's degree for service to the department and
academic excellence. I am very proud of this award! You can switch out `wd:Q47475003` for your Wikidata
identifier.

A similar SPARQL query can be written to identify all of the awards for which I was nominated by swapping the predicate
to [P1411 (nominated for)](https://www.wikidata.org/wiki/Property:P1411). This isn't necessarily a superset of the
awards received since some awards are decided without a nomination. It might also be the case depending on how curation
is done that these are out of sync.

```sparql
SELECT ?award ?awardLabel ?year ?conferer ?confererLabel
WHERE { 
  VALUES ?person { wd:Q47475003 }
  ?person p:P1411 ?award_statement .
  ?award_statement ps:P1411 ?award .
  OPTIONAL { ?award wdt:P1027 ?conferer . }
  OPTIONAL { 
    ?award_statement pq:P585 ?date . 
    BIND(year(?date) AS ?year)
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

See this query in action at [https://w.wiki/6odV](https://w.wiki/6odV).

## Summarizing an Award

Many awards are given on a periodic basis (e.g., yearly, bi-yearly). [Scholia](https://scholia.toolforge.org/award) is
an excellent frontend to Wikidata that already has a way of summarizing awards. Some examples:

- [Nobel Prize in Chemistry (Q44585)](https://scholia.toolforge.org/award/Q44585)
- [Biocuration Career Award (Q106045191)](https://scholia.toolforge.org/award/Q106045191)

## Summarizing a Conferrer

Finally, I want to summarize all awards nominated or given by an organization. In this example, I'm going to look at
the [International Society for Biocuration (ISB; Q23809291)](https://bioregistry.io/wikidata:Q23809291). 


### Winners

The following query shows all of the recipients for all of the various awards conferred by the ISB:

```sparql
SELECT ?award ?awardLabel ?recipient ?recipientLabel ?year 
WHERE { 
  ?recipient p:P166 ?award_statement .
  ?award_statement ps:P166 ?award .
  OPTIONAL { 
    ?award_statement pq:P585 ?date . 
    BIND(year(?date) AS ?year)
  }
  ?award wdt:P1027 wd:Q23809291 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY DESC(?year) ?awardLabel
```

See this query in action at [https://w.wiki/6odW](https://w.wiki/6odW).

At the time of writing, this only returned a paltry 9 rows, meaning more curation is necessary! Considering this award
is about biocurators, we better get our act together 🙃. **Update June 4<sup>th</sup>, 2023:** I went back and curated the full catalog.

### Nominations

Similarly, the following query can be used to identify all nominations:

```sparql
SELECT ?award ?awardLabel ?nominee ?nomineeLabel ?year 
WHERE { 
  ?nominee p:P1411 ?award_statement .
  ?award_statement ps:P1411 ?award .
  OPTIONAL { 
    ?award_statement pq:P585 ?date . 
    BIND(year(?date) AS ?year)
  }
  ?award wdt:P1027 wd:Q23809291 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
ORDER BY DESC(?year) ?awardLabel
```

See this query in action at [https://w.wiki/6odX](https://w.wiki/6odX).

There are only 5 results at the time of writing, and these are for my fellow nominees for the Excellence in Biocuration
Early Career Award that I recently curated! There's a lot of work to do here for keeping a history of the ISB's awards.
**Update June 4<sup>th</sup>, 2023:** I went back and curated the full catalog. It turns out that the ISB did not
publish the list of nominees for any awards until 2022, so this list will remain short.

### Wikidata-wide Summary

More generally, it turns out that there are only a bit more than 55K nomination relations in total for all
of Wikidata. You can check this with:

```sparql
SELECT (count(*) AS ?count)
WHERE { ?nominee wdt:P1411 ?award . }
```

## Curating an Award

Award objects don't have to be complicated - the most important information is to include
a useful instance annotation (e.g., to [science award (Q11448906)](https://www.wikidata.org/wiki/Q11448906)) and the
following:

1. Field of Work (P101)
2. Conferred By (P1027)
3. Website (P856)
4. Inception (P571)

See [https://www.wikidata.org/wiki/Q118947746](https://www.wikidata.org/wiki/Q118947746) as an example.

## Curating an Individual

On a given Wikidata page, you can add a statement for either *nominated for*
or *award received* using Wikidata's amazing curation interface that has search
built in. It's recommended to add a [point in time (P585)](https://www.wikidata.org/wiki/Property:P585)
annotation to make a distinction between different periods. Further, it's recommended to add a refernce
using the [reference url (P854)](https://www.wikidata.org/wiki/Property:P854) property that pints
to a webpate with an announcement about the nomination or award.

![](/img/wikidata_add_nominee_1.png)

---
Overall, I think modeling awards is hard, since these are less concrete than other academic information such as
employment or education. Still, this is the next step in making my resume 100% auto-generated by SPARQL and Wikidata!

See also [an analysis](https://github.com/cmungall/science-award-analysis) by Chris Mungall of the gender distribution
of awards in Wikidata.

**Update June 4<sup>th</sup>, 2023:** I won the Excellence in Biocuration Early Career Award! Nico Matentzoglu won the
Excellence in Biocuration Advanced Career Award and we are both excited to see that the community was interested to
recognize people who work on fundamental underlying techonologies.