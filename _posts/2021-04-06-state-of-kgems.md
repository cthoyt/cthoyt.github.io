### Testing/Validation Leakage

Leakage is when triples in the testing/validation sets can be trivially inferred from triples in the training set. This
leads to an over-estimation in the performance of the model.

The most common form of leakage occurs when a knowledge graph contains inverse triples. An example:

- `A` and `B` are entities in a knowledge graph
- `part of` and `has part` are inverse relations in the knowledge graph
- `A part of B` is in the training
- `B has part A` is in the testing set

This scenario occurs in two datasets widely used in knowledge graph embedding model benchmarking:
the FreeBase 15K (FB15k) dataset proposed by
[Bordes *et al.* (2013)](http://papers.nips.cc/paper/5071-translating-embeddings-for-modeling-multi-relational-data.pdf)
alongside the [TransE model](https://pykeen.readthedocs.io/en/latest/api/pykeen.models.TransE.html) and the WordNet-18 (
WN18) dataset proposed by
[Bordes *et al.* (2014)](https://arxiv.org/abs/1301.3485) alongside
the [Unstructured Model](https://pykeen.readthedocs.io/en/latest/api/pykeen.models.UnstructuredModel.html).
[Toutanova and Chen (2015)](https://www.aclweb.org/anthology/W15-4007) outlined an algorithm for removing leakage due to
inverse triples and applied it to respectively derive two new datasets: the Freebase 15K-237 (FB15k-237) dataset and the
WordNet-18 (RR; WN-18RR) dataset.

| Dataset   | Entities | Relations | Triples |
|-----------|---------:|----------:|--------:|
| WN-18     |   40,943 |        18 | 151,442 |
| WN-18RR   |   40,559 |        11 |  92,583 |
| FB15k     |   14,951 |     1,345 | 592,213 |
| FB15k-237 |   14,505 |       237 | 310,079 |

These datasets are of roughly the same size and are widely available. Therefore, if I read a paper that presents results
on only FB15k and WN-18 but not FB15k-237 and WN-18RR, I am concerned that the authors either do not know about this
problem, or are intentionally misleading the reader.

An alternative kind of testing leakage can occur in chemoinformatic applications. The following three chemical
structures are from a structural class called [statins (CHEBI:87631)](https://identifiers.org/CHEBI:87631) that inhibit
the HMG-CoA reductase enzyme and are often used to lower blood pressure to reduce the risk of heart disease.

| [mevastatin (CHEBI:34848)](https://identifiers.org/CHEBI:34848) | [lovastatin (CHEBI:40303)](https://identifiers.org/CHEBI:40303) | [simvastatin (CHEBI:9150)](https://identifiers.org/CHEBI:9150) |
|--------|--------|--------|
| ![mevastatin](https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=34848) | ![lovastatin](https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=40303) | ![simvastatin](https://www.ebi.ac.uk/chebi/displayImage.do?defaultImage=true&imageIndex=0&chebiId=9150) |

All three share a stereospecific cyclic lactone motif (top right part of the molecule) that result in their functional
activity. If you're building a classifier for activity against HMG-CoA reductase, or more generally, a link prediction
model that includes chemical-protein or chemical-enzyme class predictions, including some of these molecules in the
training set and others in the test set would enable trivial inference and ultimately result in an over-estimation of
the performance of your model (barring discussion about how this could be considered trivial is a huge triumph of modern
pharacology and chemoinformatics). The solution often referenced in
[proteochemometrics](https://www.universiteitleiden.nl/en/research/research-projects/science/lacdr-proteochemometrics)
papers is to use scaffold-based splitting like Bemis-Murcko scaffold splitting or to pre-cluster molecules based on
structural similarity and to split based on clusters. More information on these methods is reviewed in
[Bongers *et al.* (2019)](https://www.sciencedirect.com/science/article/pii/S1740674920300111) and
[Parks *et al.* (2020)](https://www.frontiersin.org/articles/10.3389/fmolb.2020.00093/full).

### Redundant Information in Graphs

Transcriptomics experiments are often analyzed with statistical over-representation analysis
or [gene set enrichment analysis (GSEA)](https://www.gsea-msigdb.org/gsea/index.jsp) with respect to gene sets derived
from pathway databases like KEGG, Reactome, WikiPathways, the Pathway Interaction Database, and BioCyc, functional
annotations such as those from the Gene Ontology, and biological signatures such as those listed in MSigDB. In addition
to *p*-values, the high number of statistical tests also motivates the reporting of adjusted *p*-values to
address [multiple hypothesis testing](https://en.wikipedia.org/wiki/Multiple_comparisons_problem). However, these
adjustments do not consider the high overlap in information due to the redundancy of pathway databases or potential
correlations between expert-defined pathways and certain functional or biological signatures. Therefore, several results
from the same theme or biological phenomena often co-occur as enriched which often leads to an inflated sense of
concordance of results and thus higher confirmation bias. Further, [Mubeen *et
al.* (2019)](https://www.frontiersin.org/articles/10.3389/fgene.2019.01203/full) showed that the variability of
definitions in each pathway database for the "same" pathway (e.g., apoptosis) caused significantly different results in
many downstream tasks.

Many benchmark biological knowledge graphs such as [Hetionet](https://het.io/) and
[OpenBioLink](https://github.com/openbiolink/openbiolink) include multiple pathway databases. Therefore, link prediction
tasks between genes and pathways (such as the case scenario presented in
[Ali *et al* (2019)](https://doi.org/10.1093/bioinformatics/btz117)) could be skewed both during the training and
evaluation of link prediction models, and ultimately in the interpretation of predicted results. While methodological
improvements like SetRank
([Simillion *et al.* (2017)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1571-6) have been
proposed to mitigate the redundancies in the over-representation analysis setting, there have not yet been
methodological improvements for link prediction models that consider these kinds redundancies. Further, these kinds of
redundancies do not fit as neatly into the "leakage" issue.

Tools like [ComPath](https://github.com/compath/) can be used to enrich KGs with links between functionally equivalent
pathways, but this kind of information is not readily used by typical KGEMs. Alternative rule-based and symbolic 
reasoning systems might present solutions in this area.
