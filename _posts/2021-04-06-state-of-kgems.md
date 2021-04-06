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

A more thorough listing of statins can be found through the ChEBI ontology browser under the entry. There are other
statins that do not share this privileged scaffold
