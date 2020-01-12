---
layout: page
title: Community
permalink: /community/
---
## Organizations

- OpenBEL Consortium (2017-)
- Erasmus Student Network (2016-)
- American Chemical Society (2011-)

## Events

- 4th Disease Maps Community Meeting. Seville, Spain. October 2-4, 2019.
- The Eighth Joint Sheffield Conference on Chemoinformatics.
  June 17-19th, 2019.
- INCOME Hackathon 2019. Frankfurt, Germany.
  March 18-20th, 2019.
- Summer School on Machine Learning in Drug Design. Leuven, Belgium.
  August 2018.
- Bio-IT World. Boston, USA. May 2018.
- 3rd European Conference on Translational Bioinformatics. Barcelona, Spain.
  April 2018.
- Bioinformatics Strategy Meeting Europe. Zürich, Switzerland. March 2018.
- Intelligent Systems for Molecular Biology and the 16th European Conference
  on Computational Biology. Prague, Czech Republic. March 2017.

## Events on Wikidata

<iframe style="width: 80vw; height: 50vh; border: none;" src="https://query.wikidata.org/embed.html#%0ASELECT%0A%20%20(xsd%3Adate(MIN(%3Fstart))%20AS%20%3Fdate)%20%20%0A%20%20%3Fevent%0A%20%20%3FeventLabel%0A%20%20(GROUP_CONCAT(DISTINCT%20%3Frole%3B%20separator%3D%22%2C%20%22)%20AS%20%3Froles)%0A%20%20(GROUP_CONCAT(DISTINCT%20%3Flocation_label%3B%20separator%3D%22%2C%20%22)%20AS%20%3Flocations)%0AWHERE%20%7B%0A%20%20%20%20BIND(wd%3AQ47475003%20AS%20%3Fperson)%0A%20%20%20%20%7B%20%20%23%20speaker%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP823%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22speaker%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20organizer%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP664%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22organizer%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20participant%0A%20%20%20%20%20%20%3Fperson%20wdt%3AP1344%20%7C%20%5Ewdt%3AP710%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22participant%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20editor%0A%20%20%20%20%20%20%3Fperson%20%5Ewdt%3AP98%20%2F%20wdt%3AP4745%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22editor%20of%20proceedings%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20author%0A%20%20%20%20%20%20%3Fperson%20%5Ewdt%3AP50%20%2F%20wdt%3AP1433%20%2F%20wdt%3AP4745%20%3Fevent%20%20.%0A%20%20%20%20%20%20BIND(%22author%22%20AS%20%3Frole)%0A%20%20%20%20%7D%20UNION%20%7B%20%20%23%20program%20committee%20member%0A%20%20%20%20%20%20%3Fevent%20wdt%3AP5804%20%3Fperson%20.%0A%20%20%20%20%20%20BIND(%22program%20committee%20member%22%20AS%20%3Frole)%0A%20%20%20%20%7D%0A%20%20%20%20OPTIONAL%20%7B%20%3Fevent%20wdt%3AP276%20%3Flocation%20.%20%3Flocation%20rdfs%3Alabel%20%3Flocation_label%20.%20FILTER%20(LANG(%3Flocation_label)%20%3D%20'en')%7D%0A%20%20%20%20OPTIONAL%20%7B%20%3Fevent%20wdt%3AP580%20%7C%20wdt%3AP585%20%3Fstart%20%7D%0A%20%0A%20%20%20%20SERVICE%20wikibase%3Alabel%20%7B%20bd%3AserviceParam%20wikibase%3Alanguage%20%22%5BAUTO_LANGUAGE%5D%2Cen%2Cda%2Cde%2Ces%2Cfr%2Cjp%2Cno%2Cru%2Csv%2Czh%22.%20%7D%0A%7D%0AGROUP%20BY%20%3Fevent%20%3FeventLabel%0AORDER%20BY%20DESC(%3Fdate)%20%0A" referrerpolicy="origin" sandbox="allow-scripts allow-same-origin allow-popups"></iframe>
