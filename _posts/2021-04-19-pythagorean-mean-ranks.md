---
layout: post
title: Pythagorean Mean Rank Metrics
date: 2021-04-19 13:46:00 +0100
author: Charles Tapley Hoyt
tags: pykeen
---
The mean rank (MR) and mean reciprocal rank (MRR) are among the most popular metrics reported for the evaluation of
knowledge graph embedding models in the link prediction task. While they are reported on very different intervals
(MR between {% raw %}$$[1,\infty)$${% endraw %} and MRR between {% raw %}$$(0, 1]$${% endraw %}, their deep theoretical
connection can be elegantly described through the lens of [Pythagorean means](https://en.wikipedia.org/wiki/Pythagorean_means). This blog post describes
ideas [Max Berrendorf](https://github.com/mberr) shared with me that I recently implemented in
[PyKEEN](https://github.com/pykeen/).

## The Formulation of the Link Prediction Task

The link prediction task in knowledge graphs is effectively a binary classification task for each potential triple
(h, r, t) on whether it is true or not. While the accuracy, precision, recall, F<sub>1</sub>,
[Matthews correlation coefficient](https://en.wikipedia.org/wiki/Matthews_correlation_coefficient) (MCC), the area under
[the precision-recall curve](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html)
, and area under
the [receiver operating characteristic curve](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)
(AUC-ROC or AUROC) are typically used as metrics for binary classifications, the link prediction task has the added
twist that there are only positive examples in a knowledge graph. This means that during training, potential negative
triples need to be sampled from the finite set of all possible triples. This is called negative sampling within the
knowledge graph embedding model literature but more generally called *positive unlabeled learning* in the wider machine
learning community. This works because there's a much higher likelihood that a triple not already in the knowledge graph
is negative than positive. Even if a triple is sampled that should be positive, the model and training algorithm should
remain robust.

This also means that alternative metrics need to be introduced that don't rely on the existence or non-existence of
negative examples - enter hits@k, mean rank, and mean reciprocal rank. Each of these relies on the concept of a
ranking (not to be confused with the rank of a matrix) that is calculated based on combining the true and sampled
triples into a list, then sorting based on their scores (calculated by the trained knowledge graph embedding model). The
ranks are the positions of the positive triples in this list, where lower ranks correspond to better performance. For
the molecular biologists reading, this is very similar to the rank-based visual inspection of GSEA results on
differential gene expression experiments. The hits@k, mean rank, and mean reciprocal rank are all summary statistics
over the set of ranks (again, the positions in the list of all true triples + sampled triples, sorted by score).

## Definitions of Rank-based Metrics

This post is about to include some equations. I'm going to use $$\mathcal{I}$$ to denote the set of all ranks for true
triples.

### Hits @ K

While this post isn't about hits@k, it's worth summarizing the alternative approach that it takes to summarizing the
rank list because it's a much more application-driven metric. Effectively, the hits@k describes the fraction of true
entities that appear in the first $$k$$ entities of the sorted rank list. It is given as:

{% raw %}

$$\text{score}_k = \frac{1}{|\mathcal{I}|} \sum \limits_{r \in \mathcal{I}} \mathbb{I}[r \leq k]$$

For example, if Google shows 20 results on the first page, then the percentage of results that are relevant is the hits
@ 20. The hits@k, regardless of k, lies on {% raw %}$$[0,1]$${% endraw %} where closer to 1 is better.

This metric does not differentiate between cases when the rank is larger than $$k$$. This means that a miss with rank
$$k+1$$ and $$k+d$$ where $$d \gg 1$$ have the same effect on the final score. Therefore, it is less suitable for the
comparison of different models.

### Mean Rank

The mean rank (MR) computes the arithmetic mean over all individual ranks. It is given as:

{% raw %}

$$\text{score} =\frac{1}{|\mathcal{I}|} \sum \limits_{r \in \mathcal{I}} r$$

{% endraw %}

It has the advantage over hits@k that it is sensitive to any model performance changes, not only what occurs under a
certain cutoff and therefore reflects average performance. With PyKEEN's standard 1-based indexing, the mean rank lies
on the interval \([1, \infty)\) where lower is better.

While it remains interpretable, the mean rank is dependent on the number of candidates. A mean rank of 10 might indicate
strong performance for a candidate set size of 1,000,000, but incredibly poor performance for a candidate set size of
20.

### Mean Reciprocal Rank

The mean reciprocal rank (MRR) is the arithmetic mean of reciprocal ranks, and thus the inverse of the harmonic mean of
the ranks. It is defined as:

{% raw %}

$$\text{score} =\frac{1}{|\mathcal{I}|} \sum_{r \in \mathcal{I}} r^{-1}$$

{% endraw %}

It has been argued that the mean reciprocal rank has theoretical flaws by
[Fuhr (2018)](https://pykeen.readthedocs.io/en/latest/references.html#fuhr2018). However, this opinion is not
undisputed, cf. [Sakai (2021)](https://pykeen.readthedocs.io/en/latest/references.html#sakai2021).

Despite its flaws, MRR is still often used during early stopping due to its behavior related to low rank values. While
the hits@k ignores changes among high rank values completely, and the mean rank changes uniformly across the full value
range, the mean reciprocal rank is more affected by changes of low rank values than high ones
(without disregarding them completely like hits@k does for low rank values)
Therefore, it can be considered as soft a version of hits@k that is less sensitive to outliers. It is bound on
\((0, 1]\) where closer to 1 is better.

https://pykeen.readthedocs.io/en/stable/tutorial/understanding_evaluation.html
https://github.com/pykeen/pykeen/pull/381
