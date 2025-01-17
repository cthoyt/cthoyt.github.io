---
layout: post
title: Exploring Event Venues in Wikidata
date: 2025-01-17 18:08:00 +0100
author: Charles Tapley Hoyt
tags:
  - Wikidata
  - bibliometrics
  - open data
---

I was working on making data about scholarly conferences more FAIR and a big
question crossed my mind: what are all the conference venues? This post is about
some queries I wrote for Wikidata, data issues I found, a few
[drive-by curations](https://www.qeios.com/read/KBX9VO), and my ideas for the
future.

## Querying Wikidata

Wikidata is always a good place to start looking for structured data because it
contains a detailed and multidisciplinary ontology whose classes, subclass
relationships, and instances are all queryable via SPARQL.

It has a top-level class for
[event venues (Q18674739)](https://www.wikidata.org/wiki/Q18674739), that even
comes with a high-level schematic diagram on how this class relates to
performance arts spaces:

![](https://upload.wikimedia.org/wikipedia/commons/6/61/Core_classes_for_performing_arts_places_in_Wikidata.png)

Considering that cinemas, theaters, clubs, and several other

I used the following SPARQL query to retrieve all the subclasses and investigate
which might be relevant for conferences.

```sparql
SELECT DISTINCT ?venueType ?venueTypeLabel ?venueTypeDescription
WHERE
{
  ?venueType wdt:P279* wd:Q18674739 .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

The results from this query are embedded in the table below:

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#SELECT%20DISTINCT%20%3FvenueType%20%3FvenueTypeLabel%20%3FvenueTypeDescription%0AWHERE%0A%7B%0A%20%20%3FvenueType%20wdt%3AP279%2a%20wd%3AQ18674739%20.%0A%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cmul%2Cen%22.%20%7D%0A%7D" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups" ></iframe>

The results contain a lot of irrelevant venue types such as cinemas, theaters,
and clubs. It's interesting for me to make a list of these, and refine the query
to exclude them like so:

```sparql
SELECT DISTINCT ?venueType ?venueTypeLabel ?venueTypeDescription
WHERE
{
  ?venueType wdt:P279* wd:Q18674739 .
  FILTER(?venueType NOT IN (wd:Q41253, wd:Q622425))  # this list is shortened for demo purposes
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

## Data Exploration

I encountered two noteworthy data issues the first time I ran this query:

1. Some results had Wikidata identifiers in the labels column
2. Some results appeared to be for specific event venues, and not classes

The first issue can be attributed to the fact that not all Wikidata records have
labels in english. This doesn't mean that they aren't valuable - it's also an
opportunity for doing manual or semi-automated translation to improve the data
in Wikidata.

The second issue is related to the ontology structure of Wikidata. Because this
is a query over subclasses of event venues, specific venues shouldn't show up.
This is because Wikidata records representing specific venues should use the
[instance of (P31)](https://www.wikidata.org/wiki/Property:P31) relationship to
annotate what kind/type of event venue they are.

I identified a couple groups of event venues that seemed to have this issue:

- dive sites, like [Q14213916](https://www.wikidata.org/wiki/Q14213916)
- cinemas in Brazil, like [Q123856958](https://www.wikidata.org/wiki/Q123856958)
- museums in Sweden, like [Q60628067](https://www.wikidata.org/wiki/Q60628067)

I was able to go through and update the relationship types to be correct, so if
you're reading this later, you won't see the issue. That's the power of
[drive-by curation](https://www.qeios.com/read/KBX9VO)!

## Follow-up

Next steps are to make a spreadsheet where I curate for each event venue
subclass if they're relevant or not.

After that, then I can construct a SPARQL query that uses the `VALUES` syntax to
pick the list of superclasses, then the `wdt:P31/wdt:P279*` relation path to get
all instances of any subclass of the selected event venue classes.

```sparql
SELECT DISTINCT ?venue ?venueLabel
WHERE
{
  VALUES ?venueType { wd:Q1329623 }
  ?venue wdt:P31/wdt:P279* ?venueType .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
```

At the time of writing, this query resulted in 8,728 distinct records in about
27 seconds.

---

While Wikidata is a great place to start, its nature as a fully open and
community-driven resource has the drawback of being less trustworthy than
resources that have an expert curation component (whether manual or
semi-automated).

Persistent Identifier (PID) resources like the
[Research Organization Registry (ROR)](https://ror.org/) demonstrated that
there's added value to having an expert-curated layer that both draws from and
contributes back to Wikidata.

I'm working towards seeding a registry for event venues with a similar
philosophy at
[https://github.com/event-venue-registry/evr](https://github.com/event-venue-registry/evr).
Importantly, this resource will follow the
[Open Data, Open Code, Open Infrastructure (O3) principles](https://www.nature.com/articles/s41597-024-03406-w),
meaning that the data and code are all in one GitHub repository that anyone can
contribute to. Please reach out if you'd like to help.
