---
layout: post
title: ORCID as OWL
date: 2022-11-21 22:56:00 +0100
author: Charles Tapley Hoyt
tags: bibliometrics
---
There's been an ongoing effort to push the OBO community to embrace using canonical URIs from ORCID to identify
contributors.

Stuff to mention in this post:

1. Different ways of encoding attribution
   - using names (eww)
   - using http ORCID IRIs (eww, fixed protege in order to stop this)
   - using naked IRIs
   - using class-defied IRIs, imported.
      - define as properties 
      - define as instances
2. How to make resources that are self-updating
3. Next steps - how to get this in ODK

Option 1: use ORCID then annotate the `rdfs:label`

![](img/orcid-as-owl/option-1.png)
