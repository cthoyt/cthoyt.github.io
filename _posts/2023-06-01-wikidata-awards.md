## Get all awards I've been nominated for

```sparql
SELECT ?award ?awardLabel ?beginning ?conferer ?confererLabel
WHERE { 
  wd:Q47475003 p:P166 ?award_statement .
  ?award_statement ps:P166 ?award .
  OPTIONAL { ?award_statement pq:P585 ?beginning . }
  OPTIONAL { ?award_statement pq:P1027 ?conferer . }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
```

## Get all recipients for awards from the ISB (Q23809291)

```sparql
SELECT ?award ?awardLabel ?nominee ?nomineeLabel ?year 
WHERE { 
  ?nominee p:P166 ?award_statement .
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
Switch the P166 to P1411 (nominated for)