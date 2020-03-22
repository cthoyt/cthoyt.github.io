---
layout: page
title: Community
permalink: /community/
---
## Organizations

<ul>
{% for entry in site.data.organizations %}
    <li>
    <a href="{{ entry.url }}">{{ entry.name }}</a> ({ entry.start.year }} - { entry.end.year }})
    </li>
{% endfor %}
</ul>

## Events

<ul>
{% for entry in site.data.events %}
    <li>
    <a href="{{ entry.link }}">{{ entry.name }}</a> at {{ entry.location }} during {{ entry.period }}
    </li>
{% endfor %}
</ul>

## Events on Wikidata

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#%0ASELECT%0A%20%20(xsd%3Adate(MIN(%3Fstart))%20AS%20%3Fdate)%20%20%0A%20%20%3Fevent%0A%20%20%3FeventLabel%0A%20%20(GROUP_CONCAT(DISTINCT%20%3Frole%3B%20separator%3D%22%2C%20%22)%20AS%20%3Froles)%0A%20%20(GROUP_CONCAT(DISTINCT%20%3Flocation_label%3B%20separator%3D%22%2C%20%22)%20AS%20%3Flocations)%0AWHERE%20%7B%0A%20%20%20%20BIND(wd%3AQ47475003%20AS%20%3Fperson)%0A%20%20%20%20%7B%20%20%23%20speaker%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP823%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22speaker%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20organizer%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP664%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22organizer%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20participant%0A%20%20%20%20%20%20%3Fperson%20wdt%3AP1344%20%7C%20%5Ewdt%3AP710%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22participant%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20editor%0A%20%20%20%20%20%20%3Fperson%20%5Ewdt%3AP98%20%2F%20wdt%3AP4745%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22editor%20of%20proceedings%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20author%0A%20%20%20%20%20%20%3Fperson%20%5Ewdt%3AP50%20%2F%20wdt%3AP1433%20%2F%20wdt%3AP4745%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22author%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20program%20committee%20member%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP5804%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22program%20committee%20member%22%20AS%20%3Frole)%0A%20%20%20%20%7D%0A%20%20%20%20OPTIONAL%20%7B%20%3Fevent%20wdt%3AP276%20%3Flocation%20.%20%3Flocation%20rdfs%3Alabel%20%3Flocation_label%20.%20FILTER%20(LANG(%3Flocation_label)%20%3D%20'en')%7D%0A%20%20%20%20OPTIONAL%20%7B%20%3Fevent%20wdt%3AP580%20%7C%20wdt%3AP585%20%3Fstart%20%7D%0A%20%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cda%2Cde%2Ces%2Cfr%2Cjp%2Cno%2Cru%2Csv%2Czh%22.%20%7D%0A%7D%0AGROUP%20BY%20%3Fevent%20%3FeventLabel%0AORDER%20BY%20DESC(%3Fdate)%20%0A" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
