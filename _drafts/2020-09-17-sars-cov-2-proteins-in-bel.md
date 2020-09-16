---
layout: post
title: How to Refer to SARS-CoV-2 Proteins in BEL
date: 2020-06-11 16:48:00 +0100
---
Many of the proteins in the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2)
are cleavage products of the replicase polyprotein 1ab ([uniprot:P0DTD1](https://identifiers.org/uniprot:P0DTD1)).
Unfortunately, the bioinformatics community and infrastructure does not often handle
proteins that act this way.

![SARS-CoV-2 Genome](/img/sars-cov-2-genome.jpeg)

However, because these proteins are all coded by the same gene (gasp!), the community
has taken their time in the last ~7 months deciding how to organize information about its "constituents".

The solution that UniProt gave was that most of the 16 non-structural proteins (usually written as
Nsp1 - Nsp16) 


| PRO_0000449619      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |


| Symbol  | Chain          | Positions   | Name                                  | BEL
| ------- | -------------- | ----------- | ------------------------------------- | ------------------------------------------------- |
| nsp1    | PRO_0000449619 | 1 – 180     | Host translation inhibitor nsp1       | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(1_180))`     |
| nsp2    | PRO_0000449620 | 181 – 818   | Non-structural protein 2              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(181_818))`   |
| nsp3    | PRO_0000449621 | 819 – 2763  | Non-structural protein 3              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(819_2763))`  |
| nsp4    | PRO_0000449622 | 2764 – 3263 | Non-structural protein 4              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(2764_3263))` |
| nsp5    | PRO_0000449623 | 3264 – 3569 | 3C-like proteinase                    | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(3264_3569))` |
| nsp6    | PRO_0000449624 | 3570 – 3859 | Non-structural protein 6              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(3570_3859))` |
| nsp7    | PRO_0000449625 | 3860 – 3942 | Non-structural protein 7              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(3860_3942))` |
| nsp8    | PRO_0000449626 | 3943 – 4140 | Non-structural protein 8              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(3943_4140))` |
| nsp9    | PRO_0000449627 | 4141 – 4253 | Non-structural protein 9              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(4141_4253))` |
| nsp10   | PRO_0000449628 | 4254 – 4392 | Non-structural protein 10             | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(4254_4392))` |
| nsp12   | PRO_0000449629 | 4393 – 5324 | RNA-directed RNA polymerase           | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(4393_5324))` |
| nsp13   | PRO_0000449630 | 5325 – 5925 | Helicase                              | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(5325_5925))` |
| nsp14   | PRO_0000449631 | 5926 – 6452 | Proofreading exoribonuclease          | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(5926_6452))` |
| nsp15   | PRO_0000449632 | 6453 – 6798 | Uridylate-specific endoribonuclease   | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(6453_6798))` |
| nsp16   | PRO_0000449633 | 6799 – 7096 | 2'-O-methyltransferase                | `p(uniprot:P0DTD1 ! R1AB_SARS2, frag(6799_7096))` |

I'm not sure what happened to #11. UniProt isn't listing it here. There's also
the Replicase polyprotein 1a, which lists nsp1-nsp11. I'm not sure what the difference
is yet.
