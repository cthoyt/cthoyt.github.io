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
that the team constructed SQLite dumps for all previous versions, too. This is
great, because I use the SQLite dump as the primary mechanism for querying the
database.

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

1. to get _all_ versions of ChEMBL, it needs to include v22.1 and v24.1.
   [`chembl.versions()`](https://chembl-downloader.readthedocs.io/en/latest/api/chembl_downloader.versions.html)
   provides convenient access to construct this iterator
2. SQLite does not allow for opening a compressed database
   ([without paying for an extension](https://www.sqlite.org/zipvfs/doc/trunk/www/readme.wiki)),
   so each version needs to be uncompressed. Unfortunately, most personal
   computers (including mine) don't enough hard disk space to have an
   uncompressed copy of each version of ChEMBL

## Results of Temporal Analysis

I wrote a CLI utility
[ `chembl_downloader history`](https://chembl-downloader.readthedocs.io/en/latest/cli.html#chembl-downloader-history)
which downloads, decompresses, analyzes, and then deletes each version of ChEMBL
iteratively over the span of about three hours.

It summarizes the dates of release, number of compounds, number of named
compounds, (i.e., with a `pref_name`), number of assays, and number of
activities, and several other entity types to (almost) match what's summarized
on the ChEMBL [homepage](https://www.ebi.ac.uk/chembl). The results can be
[downloaded as a TSV](https://github.com/cthoyt/chembl-downloader/raw/refs/heads/main/docs/_data/summary.tsv)
and are as follows:

| Version | Date       | Compounds | Named Compounds |    Assays | Activities | Documents | Targets | Cells | Tissues | Drug Warnings | Drug Indications | Drug Mechanisms |
| ------: | ---------- | --------: | --------------: | --------: | ---------: | --------: | ------: | ----: | ------: | ------------: | ---------------: | --------------: |
|      35 | 2024-12-01 | 2,496,335 |          42,231 | 1,740,546 | 21,123,501 |    92,121 |  16,003 | 2,129 |     782 |         1,676 |           55,442 |           7,330 |
|      34 | 2024-03-28 | 2,431,025 |          42,387 | 1,644,390 | 20,772,701 |    89,892 |  15,598 | 2,023 |     782 |         1,676 |           55,442 |           7,330 |
|      33 | 2023-05-31 | 2,399,743 |          41,923 | 1,610,596 | 20,334,684 |    88,630 |  15,398 | 2,021 |     782 |         1,636 |           51,582 |           7,098 |
|      32 | 2023-01-26 | 2,354,965 |          41,923 | 1,536,903 | 20,038,828 |    86,361 |  15,139 | 2,015 |     759 |         1,636 |           51,582 |           7,098 |
|      31 | 2022-07-12 | 2,331,700 |          41,585 | 1,498,681 | 19,780,369 |    85,431 |  15,072 | 2,000 |     757 |         1,293 |           48,816 |           6,656 |
|      30 | 2022-02-22 | 2,157,379 |          41,549 | 1,458,215 | 19,286,751 |    84,092 |  14,855 | 1,991 |     752 |         1,293 |           48,816 |           6,656 |
|      29 | 2021-07-01 | 2,105,464 |          41,383 | 1,383,553 | 18,635,916 |    81,544 |  14,554 | 1,978 |     743 |         1,262 |           45,902 |           6,202 |
|      28 | 2021-01-15 | 2,086,898 |          41,049 | 1,358,549 | 17,276,334 |    80,480 |  14,347 | 1,950 |     739 |         1,256 |           42,988 |           5,347 |
|      27 | 2020-05-18 | 1,961,462 |          40,834 | 1,221,361 | 16,066,124 |    76,086 |  13,382 | 1,831 |     707 |             0 |           37,259 |           5,134 |
|      26 | 2020-02-14 | 1,950,765 |          40,822 | 1,221,311 | 15,996,368 |    76,076 |  13,377 | 1,830 |     707 |             0 |           37,259 |           5,070 |
|      25 | 2019-02-01 | 1,879,206 |          39,885 | 1,125,387 | 15,504,603 |    72,271 |  12,482 | 1,670 |     655 |             0 |           29,457 |           4,992 |
|    24.1 | 2018-05-01 | 1,828,820 |          39,877 | 1,060,283 | 15,207,914 |    69,861 |  12,091 | 1,667 |     655 |             0 |           29,163 |           4,992 |
|      24 | 2018-05-01 | 1,828,820 |          39,877 | 1,060,283 | 15,207,914 |    69,861 |  12,091 | 1,667 |     655 |             0 |           29,163 |           4,992 |
|      23 | 2017-05-18 | 1,735,442 |          39,584 | 1,302,147 | 14,675,320 |    67,722 |  11,538 | 1,624 |     125 |             0 |           13,504 |           4,305 |
|    22.1 | 2016-11-17 | 1,686,695 |          39,422 | 1,246,683 | 14,371,197 |    65,213 |  11,224 | 1,619 |     111 |             0 |           12,573 |           3,834 |
|      22 | 2016-09-28 | 1,686,695 |          39,422 | 1,246,132 | 14,371,219 |    65,213 |  11,224 | 1,619 |     111 |             0 |           12,573 |           3,834 |
|      21 | 2015-02-12 | 1,592,191 |          39,347 | 1,212,831 | 13,968,617 |    62,502 |  11,019 | 1,612 |       0 |             0 |            5,951 |           3,799 |
|      20 | 2015-02-03 | 1,463,270 |          39,016 | 1,148,942 | 13,520,737 |    59,610 |  10,774 | 1,647 |       0 |             0 |                0 |           2,266 |
|      19 | 2014-07-23 | 1,411,786 |          38,910 | 1,106,285 | 12,843,338 |    57,156 |  10,579 | 1,653 |       0 |             0 |                0 |           2,239 |
|      18 | 2014-04-02 | 1,359,508 |          35,817 | 1,042,374 | 12,419,715 |    53,298 |   9,414 | 1,655 |       0 |             0 |                0 |           2,233 |
|      17 | 2013-09-16 | 1,324,941 |          32,692 |   734,201 | 12,077,491 |    51,277 |   9,356 | 1,746 |       0 |             0 |                0 |           2,213 |
|      16 | 2013-05-15 | 1,295,510 |          23,532 |   712,836 | 11,420,351 |    50,095 |   9,844 | 1,432 |       0 |             0 |                0 |               0 |
|      15 | 2013-01-30 | 1,254,575 |          23,528 |   679,259 | 10,509,572 |    48,735 |   9,570 | 1,432 |       0 |             0 |                0 |               0 |
|      14 | 2012-07-18 | 1,213,242 |          16,573 |   644,734 | 10,129,256 |    46,133 |   9,003 |     0 |       0 |             0 |                0 |               0 |
|      13 | 2012-02-29 | 1,143,682 |          16,397 |   617,681 |  6,933,068 |    44,682 |   8,845 |     0 |       0 |             0 |                0 |               0 |
|      12 | 2011-11-30 | 1,077,189 |          16,658 |   596,122 |  5,654,847 |    43,418 |   8,703 |     0 |       0 |             0 |                0 |               0 |
|      11 | 2011-06-07 | 1,060,258 |          16,264 |   582,982 |  5,479,146 |    42,516 |   8,603 |     0 |       0 |             0 |                0 |               0 |
|      10 | 2011-06-07 | 1,000,468 |          16,159 |   534,391 |  4,668,202 |    40,624 |   8,372 |     0 |       0 |             0 |                0 |               0 |
|       9 | 2011-01-04 |         0 |           3,746 |   499,867 |  3,030,317 |    39,094 |   8,091 |     0 |       0 |             0 |                0 |               0 |
|       8 | 2010-11-05 |   636,269 |               0 |   488,898 |  2,973,034 |    38,462 |   8,088 |     0 |       0 |             0 |                0 |               0 |
|       7 | 2010-09-03 |   602,500 |               0 |   485,095 |  2,948,069 |    38,204 |   8,078 |     0 |       0 |             0 |                0 |               0 |
|       6 | 2010-09-03 |   600,625 |               0 |   481,752 |  2,925,588 |    38,029 |   8,054 |     0 |       0 |             0 |                0 |               0 |
|       5 | 2010-06-07 |   578,715 |               0 |   459,823 |  2,787,240 |    36,624 |   7,493 |     0 |       0 |             0 |                0 |               0 |
|       4 | 2010-05-26 |   565,245 |               0 |   446,645 |  2,705,136 |    35,821 |   7,330 |     0 |       0 |             0 |                0 |               0 |
|       3 | 2010-04-30 |   547,133 |               0 |   432,022 |  2,490,742 |    34,982 |   7,330 |     0 |       0 |             0 |                0 |               0 |
|       2 | 2009-12-07 |   517,261 |               0 |   416,284 |  2,404,622 |    33,956 |   7,192 |     0 |       0 |             0 |                0 |               0 |
|       1 | 2009-10-28 |   440,055 |               0 |   329,250 |  1,936,969 |    26,299 |   5,694 |     0 |       0 |             0 |                0 |               0 |

The same results can be viewed as charts:

![](https://github.com/cthoyt/chembl-downloader/raw/main/docs/_data/summary.svg)

These charts show when certain features were introduced, such as cells in v15,
drug indications in v20, tissues in v22, and drug warnings in v28.

The number of named compounds seems to have plateaued in v19 in 2014. This is
strange, considering that ChEMBL links to many external resources like ChEBI
that have nice preferred names that be imported. However, much like I found in
[my recent post]({% post_url 2025-04-17-chembl-indications-efo-exploration %})
about the EFO identifier column in ChEMBL's diseases table, the `pref_name`
column in the compounds table might not actually mean what I guess it does.

## Change over Time

In order to investigate the changes over time, I also took the discrete
derivative of each:

![](https://github.com/cthoyt/chembl-downloader/raw/main/docs/_data/summary-diff.svg)

There are a few interesting places where the numbers dropped, such as the number
of targets in v17 and the number of assays in v24 (which might have been a
mistake that triggered the v24.1 release). I'm sure there's a bit of explanation
in the READMEs for these releases - please comment at the end of the post if you
happen to take a look and have more explanation.

Overall, this analysis shows that the amount of content added between ChEMBL
versions is relatively consistent (though keep in mind it's on a log axis). The
time for each release is also only slightly increasing on average.

## Future Ideas

I would love to extend the idea of a temporal analysis towards other
target-centric metrics like:

1. Are there examples of targets where the chemical space gets a lot bigger?
2. Conversely, are there targets where new compounds just seem to be in the same
   old neighborhood?
3. Are there widely conflicting activities added over time?
4. How does the ability of a QSAR model trained on a given version of ChEMBL
   perform with respect to the data that's added later?

I presented one such example in the `chembl-downloader` manuscript where I
re-ran one of Pat Walter's analyses on
[5-lipoxygenase activating protein (CHEMBL4550)](https://bioregistry.io/chembl:CHEMBL4550)
in
[this notebook](https://github.com/cthoyt/chembl-downloader/blob/main/notebooks/refresh-static-data.ipynb).
There, the number of activities increased by more than double since the original
analysis, but the distribution was roughly the same.

If you're interested in teaming up to do a retrospective analysis on your
favorite target (or, maybe even using knowledge graphs for interesting
aggregations of targets based on gene sets, disease associations, etc.), then
let me know.
