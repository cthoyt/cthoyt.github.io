---
layout: post
title: A historical analysis of ChEMBL
date: 2025-08-25 08:57:00 +0200
author: Charles Tapley Hoyt
tags:
  - ChEMBL
  - cheminformatics
  - chemoinformatics
  - chemistry
  - bibliometrics
---

I've recently submitted an article to the
[Journal of Open Source Software (JOSS)](https://joss.theoj.org/) describing
[`chembl-downloader`](https://github.com/cthoyt/), a Python package for
automating downloading and using ChEMBL data in a reproducible way. In this
post, I use `chembl-downloader` to show how the number of compounds, assays,
activities, and other entities in ChEMBL have changed over time.

ChEMBL has made 37 releases so far. 35 of them have been major releases, and two
have been minor releases
([v22.1](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_22_1/)
and
[v24.1](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_24_1/)).
While it only began bundling a SQLite dump of the database
[v19](https://ftp.ebi.ac.uk/pub/databases/chembl/ChEMBLdb/releases/chembl_19/),
Eloy Felix
[recently informed me](https://github.com/cthoyt/chembl-downloader/issues/20)
that the team constructed SQLite dumps for all previous versions, too.

`chembl-downloader` automates downloading any version of ChEMBL's SQLite
database, unpacking it from the TAR archive, connecting to it, making a SQL
query, and returning the results as a Pandas DataFrame object with
[`chembl_downloader.query()`](https://chembl-downloader.readthedocs.io/en/latest/api/chembl_downloader.query.html)
or
[`chembl_downloader.query_scalar()`](https://chembl-downloader.readthedocs.io/en/latest/api/chembl_downloader.query_scalar.html)
like in:

```python
import chembl_downloader

sql = "SELECT * FROM activities LIMIT 5"
rows = chembl_downloader.query(sql, version=1)

sql = "SELECT COUNT(*) FROM activities"
count: int = chembl_downloader.query_scalar(sql, version=1)
```

These functions can be used to write a loop and run the same SQL query over
every version of ChEMBL with a few two caveats:

1. to get _all_ versions of ChEMBL, it needs to include v22.1 and v22.2.
   Therefore, you can use the
   [`chembl.versions()`](https://chembl-downloader.readthedocs.io/en/latest/api/chembl_downloader.versions.html)
   to get the list of all versions, and iterate over that.
2. SQLite does not allow for opening a compressed database
   ([without paying for an extension](https://www.sqlite.org/zipvfs/doc/trunk/www/readme.wiki)),
   so each version needs to be uncompressed. Unfortunately, my laptop doesn't
   have enough hard disk space for this, so I wrote a CLI utility that wraps the
   following analysis, which takes care of deleting old versions after they're
   used.

## Results of Temporal Analysis

I put all of this in the CLI utility `chembl_downloader history`, which takes
about two hours to download, unzip, analyze, and delete all versions of ChEMBL
iteratively. It summarizes the dates of release, number of compounds, number of
named compounds, (i.e., with a `pref_name`), number of assays, and number of
activities. I would also like to extend this to documents, drugs, and other
elements that are summarized on the modern homepage. Here are the results:

| Version | Date       | Compounds |    Assays | Activities | Named Compounds |
| ------- | ---------- | --------: | --------: | ---------: | --------------: |
| 35      | 2024-12-01 | 2,496,335 | 1,740,546 | 21,123,501 |          42,231 |
| 34      | 2024-03-28 | 2,431,025 | 1,644,390 | 20,772,701 |          42,387 |
| 33      | 2023-05-31 | 2,399,743 | 1,610,596 | 20,334,684 |          41,923 |
| 32      | 2023-01-26 | 2,354,965 | 1,536,903 | 20,038,828 |          41,923 |
| 31      | 2022-07-12 | 2,331,700 | 1,498,681 | 19,780,369 |          41,585 |
| 30      | 2022-02-22 | 2,157,379 | 1,458,215 | 19,286,751 |          41,549 |
| 29      | 2021-07-01 | 2,105,464 | 1,383,553 | 18,635,916 |          41,383 |
| 28      | 2021-01-15 | 2,086,898 | 1,358,549 | 17,276,334 |          41,049 |
| 27      | 2020-05-18 | 1,961,462 | 1,221,361 | 16,066,124 |          40,834 |
| 26      | 2020-02-14 | 1,950,765 | 1,221,311 | 15,996,368 |          40,822 |
| 25      | 2019-02-01 | 1,879,206 | 1,125,387 | 15,504,603 |          39,885 |
| 24.1    | 2018-05-01 | 1,828,820 | 1,060,283 | 15,207,914 |          39,877 |
| 24      | 2018-05-01 | 1,828,820 | 1,060,283 | 15,207,914 |          39,877 |
| 23      | 2017-05-18 | 1,735,442 | 1,302,147 | 14,675,320 |          39,584 |
| 22.1    | 2016-11-17 | 1,686,695 | 1,246,683 | 14,371,197 |          39,422 |
| 22      | 2016-09-28 | 1,686,695 | 1,246,132 | 14,371,219 |          39,422 |
| 21      | 2015-02-12 | 1,592,191 | 1,212,831 | 13,968,617 |          39,347 |
| 20      | 2015-02-03 | 1,463,270 | 1,148,942 | 13,520,737 |          39,016 |
| 19      | 2014-07-23 | 1,411,786 | 1,106,285 | 12,843,338 |          38,910 |
| 18      | 2014-04-02 | 1,359,508 | 1,042,374 | 12,419,715 |          35,817 |
| 17      | 2013-09-16 | 1,324,941 |   734,201 | 12,077,491 |          32,692 |
| 16      | 2013-05-15 | 1,295,510 |   712,836 | 11,420,351 |          23,532 |
| 15      | 2013-01-30 | 1,254,575 |   679,259 | 10,509,572 |          23,528 |
| 14      | 2012-07-18 | 1,213,242 |   644,734 | 10,129,256 |          16,573 |
| 13      | 2012-02-29 | 1,143,682 |   617,681 |  6,933,068 |          16,397 |
| 12      | 2011-11-30 | 1,077,189 |   596,122 |  5,654,847 |          16,658 |
| 11      | 2011-06-07 | 1,060,258 |   582,982 |  5,479,146 |          16,264 |
| 10      | 2011-06-07 | 1,000,468 |   534,391 |  4,668,202 |          16,159 |
| 9       | 2011-01-04 |   658,075 |   499,867 |  3,030,317 |           3,746 |
| 8       | 2010-11-05 |         0 |   488,898 |  2,973,034 |               0 |
| 7       | 2010-09-03 |         0 |   485,095 |  2,948,069 |               0 |
| 6       | 2010-09-03 |         0 |   481,752 |  2,925,588 |               0 |
| 5       | 2010-06-07 |         0 |   459,823 |  2,787,240 |               0 |
| 4       | 2010-05-26 |         0 |   446,645 |  2,705,136 |               0 |
| 3       | 2010-04-30 |         0 |   432,022 |  2,490,742 |               0 |
| 2       | 2009-12-07 |         0 |   416,284 |  2,404,622 |               0 |
| 1       | 2009-10-28 |         0 |   329,250 |  1,936,969 |               0 |

Here's what that looks like as a chart:

![](https://github.com/cthoyt/chembl-downloader/raw/main/docs/_data/summary.svg)

## Commentary

The first nine versions did not have a `molecules` table, so the initial results
are missing numbers there. I still need to go back and figure out what the table
was called, then update the `chembl_downloader history` script with some special
cases to use alternate SQL queries on those versions.

The number of named compounds seems to have plateaued in v19 in 2014. This is
strange, considering that ChEMBL links to many external resources like ChEBI
that have nice preferred names that be imported. However, much like I found in a
recent post about the EFO identifier column in ChEMBL's diseases table, the
`pref_name` column in the compounds table might not actually mean what I guess
it does.

There were a few suspicious places where the nuber of activities actually went
down. Perhaps this was due to the correction of problematic data ingestion,
duplication, or something else.

This also lead me to doing a short analysis of taking the discrete derivative.
This would allow for taking the histogram of inter-release times, looking at the
change in productivity of adding new content. I didn't find anything
interesting - the productivity has been about constant.

## Future Ideas

I would love to extend this kind of temporal analysis with e.g., training a QSAR
model for a given target and seeing how the results change over time (though,
this is also affected by the issue wiht aggregating data from multiple assays).
Maybe a different analysis is to quantify the variety of chemicals reported over
time for a given target. Maybe some targets only get small exploration on the
same old series and some targets get lots of new kinds of chemical space

- find reference to the re-analysis i did on pat walter's post in the
  chembl-downloader repo
  [](github.com/cthoyt/chembl-downloader/blob/main/notebooks/refresh-static-data.ipynb)

Maybe doing an analysis of which kinds of targets are covered would also be
interesting. are there any gaps that have been filled? what's still open?
