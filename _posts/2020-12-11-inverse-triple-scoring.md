---
layout: post
title: Scoring Inverse Triples
date: 2020-12-11 00:00:00 -0800
author: Charles Tapley Hoyt
---
When training a knowledge graph embedding model with inverse triples,
two scores are learned for every triple `(h, r, t)` - one for the original
and one for the inverse triple `(t, r', h)`. This blog post is about
investigating when/why there might be meaningful differences between those scores
depending on the dataset, model, and training assumption.

In [PyKEEN](https://github.com/pykeen/pykeen/), each interaction model (e.g., TransE, ConvE, Tucker)
inherits from the base model `pykeen.models.Model` and implements the scoring methods `Model.score_h()`,
`Model.score_r()`, `Model.score_t()`, and `Model.score_hrt()`. The last, `score_hrt()` takes in a
triple or sequence of triples and calculates a real-valued score for each. This is quite efficient in
batch because of the way most models are implemented with matrix multiplication in PyTorch. The remaining
three take pairs:

- `score_h()` takes relation/tail pairs and provides scores across all possible tails
- `score_r()` takes head/tail pairs and provides scores across all possible relations
- `score_t()` takes head/relation pair and provides scores across all possible heads

Each of these functions are used slightly differently during the training and inference workflows. One
of the reviewers for the [PyKEEN software paper](https://arxiv.org/abs/2007.14175) pointed out that
the while ``Model.predict_scores_all_tails()`` and ``Model.predict_scores_all_heads()`` inference workflows
allow the user to choose if the forward triples  or inverse triples are used for predictions, that this
functionality is not exposed to the user for use in further study.

Mehdi ([@mali-git](https://github.com/mali-git); he's a really good guy) began [pykeen/pykeen#208](https://github.com/pykeen/pykeen/pull/208)
refactoring the implementation of the  head prediction and tail prediction workflows in the
`pykeen.model.Model` base  model class that better abstracted the operations for generating inverse
triples, and how they are applied in each inference workflow.

I often serve the role of project manager for PyKEEN, so I was initially a bit skeptical of adding new
functionality without some good examples of what a user might do with it. After a bit of discussion,
Mehdi suggested we could showcase a comparison the distributions of forward and inverse triples scores
and provided a minimal example. While he was busy *actually* working on the implementation, I took his
example to the extreme and created an entire experimental setup for this investigation to accompany
the new implementation.

## Comparison of Distributions

Medhi provided a new implementation of `Model.score_hrt_inverse` for exactly this kind of investigation.
The following code can be used to get the scores for the testing triples from the Nations dataset.

```python
from pykeen.datasets import Nations
from pykeen.pipeline import pipeline

nations = Nations()
testing_triples = nations.testing.mapped_triples

res = pipeline(
    dataset=nations,
    model='RotatE',
    training_loop='LCWA',
    training_kwargs=dict(num_epochs=60),
)

# Score with original triples
scores_forward = res.model.score_hrt(testing_triples)

# Score with inverse triples
scores_inverse = res.model.score_hrt_inverse(testing_triples)
```

These results are both PyTorch tensors, so don't forget to use `scores_*.detach().numpy()`
for use in your own comparisons and visualizations. The first thing I did was plotted the
distributions of both with [`seaborn.histplot`](https://seaborn.pydata.org/generated/seaborn.histplot.html).

The following two plots show that sometimes the distributions match up pretty well, and sometimes they
don't. The distributions are shown normalized to make it easier to compare - the shapes are more important
than the actual counts because the number of testing triples changes from dataset to dataset. Sorry about
the inconsistency in bin widths - I've tried a lot and haven't figured it out. If you know the solution,
please let me know (or make a PR to PyKEEN for ultimate PR cred).

| Nations | Kinships |
|---------|----------|
|![Comparison of Distributions for Nations/RotatE/LCWA](/img/inverse_triple_scoring/nations_rotate_lcwa_overlay.png) | ![Comparison of Distributions for Kinships/RotatE/LCWA](/img/inverse_triple_scoring/kinships_rotate_lcwa_overlay.png) |

This was just one comparison for the same model/training assumption. In order to make
it possible to look at many facets at the same time, the data need to be simplified.
Because the scores have a pairwise correspondence (the same triple was scored two ways), it
makes sense to plot distribution of residuals (the forward score minus the inverse score).
Here's the same plots simplified with residuals:

| Nations | Kinships |
|---------|----------|
|![Comparison of Residuals for Nations/RotatE/LCWA](/img/inverse_triple_scoring/nations_rotate_lcwa_residuals.png) | ![Comparison of Residuals for Kinships/RotatE/LCWA](/img/inverse_triple_scoring/kinships_rotate_lcwa_residuals.png) |

The score axes will not be share because each model produces different ranges of scores with different
density functions. This itself is also an interesting and upcoming avenue of research!

![Inverse Scores Residuals](/img/inverse_triple_scoring/inverse_scores_residuals.png)
