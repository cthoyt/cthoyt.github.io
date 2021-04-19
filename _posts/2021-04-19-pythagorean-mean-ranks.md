---
layout: post
title: Pythagorean Mean Rank Metrics
date: 2021-04-19 13:46:00 +0100
author: Charles Tapley Hoyt
tags: pykeen
---
The mean rank (MR) and mean reciprocal rank (MRR) are among the most popular metrics reported for the evaluation of
knowledge graph embedding models in the link prediction task. While they are reported on very different intervals (MR
between 1 and ∞ and MRR between 0 and 1), their deep theoretical connection can be elegantly described through the lens
of [Pythagorean means](https://en.wikipedia.org/wiki/Pythagorean_means).

The link prediction task in knowledge graphs is effectively a binary classification task for each potential triple
(h, r, t) on whether it is true or not. While the accuracy, precision, recall, F<sub>1</sub>,
[Matthews correlation coefficient (MCC)](https://en.wikipedia.org/wiki/Matthews_correlation_coefficient), the area under
[the precision-recall curve](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_recall_curve.html)
, and area under
the [receiver operating characteristic curve (AUC-ROC or AUROC)](https://en.wikipedia.org/wiki/Receiver_operating_characteristic)
are typically used as metrics for binary classifications, the link prediction task has the added twist that there are
only positive examples in a knowledge graph. This means that during training, potential negative triples need to be
sampled from the finite set of all possible triples. This is called negative sampling within the knowledge graph
embedding model literature but more generally called *positive unlabeled learning* in the wider machine learning
community. This works because there's a much higher likelihood that a triple not already in the knowledge graph is
negative than positive. Even if by chance, a triple is sampled that should be positive, the model and training algorithm
should remain robust.

As an aside, negative sampling can also be introduced during evaluation to provide estimates of confusion matrix-based
metrics.

## What are Ranks?

not to be confused with the rank of a matrix

##

https://pykeen.readthedocs.io/en/stable/tutorial/understanding_evaluation.html
https://github.com/pykeen/pykeen/pull/381