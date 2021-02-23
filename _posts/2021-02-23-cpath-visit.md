In late 2017, I visited the [Critical Path Institute](https://c-path.org/) in Tucson, Arizona with
my colleague Daniel Domingo-Fernández to use
our [Alzheimer's disease map](https://neurommsig.scai.fraunhofer.de/) encoded in the
[Biological Expression Language](https://biological-expression-language.github.io/) and the tools we
built in [PyBEL](https://github.com/pybel/pybel) to help contextualize their mild cognitive
impairment (MCI) conversions models. We got very interesting results, but they had a major overlap
with unpublished work of one of our colleagues on the role of
[KANSL1](https://identifiers.org/hgnc:24565) in Alzheimer's disease, so we never reported them. Last
week, his [paper](https://doi.org/10.3233/JAD-201397) finally made it publication
(congratulations, Sepehr!) so I thought it would be fun to rehash the old results and look at how
the results might have changed over time with improvements to the underlying knowledge graph.

After a long flight from Germany and layover in Phoenix (remember before the pandemic when that was
a thing?), we were received at the Tucson Airport
by [Klaus Romero](https://www.linkedin.com/in/klaus-romero-66356844/), the Director of Quantitative
Medicine at the Critical Path Institute (C-Path). He helped us acclimatized to the quiet, flat
plains of the Sonoran Desert with a ride down its long stretches of highways in his BMW V8 on our
way to our accommodations in the city.

![Cacti outside the Tucson Airport](/img/tucson_cacti.jpg)

We were lucky to have arrived at C-Path when we did - Klaus's team was mostly remote, but met in
person once or twice a year. They were the mavericks of the institute - the team of computational
biologists, pharmacologists, and toxicologists who took advantage of the deep ties of the institute
to regulatory bodies like the American Food and Drug Administration (FDA) to pilot some of the first
computational tools to gain regulatory approval for use in a clinical setting.

As our working lay on the computational side of neurodegeneration, we were introduced to
[Daniela Conrado](https://www.linkedin.com/in/daniela-conrado-82492945/) and her work on a clinical
data-driven conversion model from mild cognitive impairment (MCI) to full Alzheimer's disease.
Ultimately, it was a linear mixed-effect model that implicated several clinical exams and
measurements as co-variates:

- Clinical Dementia Rating (CDR)
- Clinical Dementia Rating Scale (sum of boxes) (CDR-SOB)
- Mini Mental State Exam (MMSE)
- APOE ε4 status
- amyloid beta 40
- amyloid beta 42
- hippocampal volume
- hippocampal atrophy

It became our goal to use NeuroMMSig (the Alzheimer's disease map) to identify a potentially
explanatory subgraph (i.e., a mechanism) that connected all the co-variates. After spending months
re-curating the NeuroMMSig subgraph following the end of the AETIONOMY project, we were excited to
apply it and all of its shiny new goodness.

## Methodology

When we first mapped the co-variates in the MCI conversion model to nodes in our knowledge graph, we
found some had high information density, like the amyloid and APOE nodes, but the clinical
measurements were relatively low. While this would generally lead to poor robustness, an advantage
of curated knowledge graph-based approaches is that we were able to curate additional relevant
knowledge for these nodes by making use of automated and semi-automated relation extraction
pipelines as well as manual curation for enrichment. Further, the clinical relationships were
curated during the work presented
in [NIFT project](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5611802/), so we were able to adapt
the curation guidelines and apply them once again. We did some curation with the help of master's
student of molecular biology Lukas Beniusis who was working in our group back in Germany as a
student research assistant at the time. Ultimately, the resulting curated content found its way to
GitHub in the [CONIB](https://github.
com/pharmacome/conib/blob/master/hbp_knowledge/biomarkers/cdr_sb_associations.bel) repository under
the CC BY 4.0 license. After substantially broadening the connections with other nodes, more
hypotheses could be generated in algorithmic steps.
