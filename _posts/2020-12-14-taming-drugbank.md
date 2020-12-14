---
layout: post
title: Making DrugBank Reproducible
date: 2020-12-14 00:00:00 -0800
author: Charles Tapley Hoyt
---
If you're reading my blog, there's a pretty high chance you've used
[DrugBank](https://go.drugbank.com/), a database of drug-target
interations, drug-drug interactions, and other high-granularity information
about clinically-studied chemicals. DrugBank has two major problems, though:
its data are password-protected, and its license does not allow redistribution.
Time to solve these problems once and for all.

I'd guess that most of the thousands of people who use DrugBank have run into
the same issue as me to get the data: you have to navigate through the DrugBank
site, create an account, log in, then download the data manually. There are some
hints on the site on how this can be done through the shell, but I think it's
the unfortunate case that many people using bioinformatics resources just aren't
comfortable using the shell. Further, the file is zipped, which means that
unzipping it requires further knowledge of the arcane arts of which shell programs
and which flags to use with them.

Even after getting past this, users need to write their own programs that read
the XML content of the file, extract the relevant parts, and put it somewhere
for later. If you're like me, you probably want to have as little to do with data
in the  XML format as possible, and you probably deleted the original zip archive
along with the XML file after you got the data out of it that you *actually* wanted.

The trouble with the scenario described in the last two paragraphs is that any
analysis done on the resulting files required lots of manual steps in the middle.
These steps can't be automated, and therefore the downstream analysis can't be
automated either. It's highly likely for a research to have the time or motivation
to do these steps exactly the same way as described in a paper, if it's even described
at all.

This is no small problem - hundreds of papers cite DrugBank per year. The hot field
of drug repositioning for COVID-19 no doubt helped in 2020, with 147
citations as of the time of writing this post on December 14th, 2020.

![DrugBank Citations](/img/drugbank_citations.png)

It's difficult to tell which, if any, of these efforts are meaningful. Without the
ability to reproduce the steps taken to do analyses based on DrugBank, we can not
even begin to evaluate these papers. Even further - imagine the intense pressure
on the few scientists famous in network-based drug repositioning who recieve the
most requests to review more papers. How could we possibly expect these scientists
to provide thorough reviews




In my (still not accepted to a peer-reviewed journal) [article](https://www.biorxiv.org/content/10.1101/631812v1)
on reproducibly downloading and converting a wide range of biological databases into
[Biological Expression Language](https://biological-expression-language.github.io)