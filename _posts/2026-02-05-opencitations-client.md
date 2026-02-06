---
layout: post
title: OpenCitations
date: 2026-02-05 13:46:00 +0100
author: Charles Tapley Hoyt
tags:
  - bibliometrics
  - citations
  - citation networks
---

## Background on OpenCitations

[OpenCitations](https://opencitations.net) aggregates and deduplicates
bibliographic information (e.g., from CrossRef, Europe PubMed Central) to
construct a comprehensive, open (i.e., CC0) index of citations between
documents. It provides access via an [API](https://api.opencitations.net) and
[bulk data downloads](https://download.opencitations.net) distributed across
FigShare and Zenodo.

I've been thinking about how to integrate citations into my knowledge graph
infrastructure for years and pushed very hard for

Importantly, it publishes its data under the CC0 public domain license to
democratize

1. What is OpenCitations
2. Why APIs are a problem, referencing many other examples I've blogged about
3. Mapping probelm in open citations
4. Architecture for a package that wraps both API and caching mechanism
5. The other packages I had to implement and improve along the way
6. Workflows in combination with pubmed-downloader
