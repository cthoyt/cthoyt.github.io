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
Ultimately, it was a linear mixed-effect model that implicated several clincal exams and
measurements as covariates:

- Clinical Dementia Rating (CDR)
- Clinical Dementia Rating Scale (sum of boxes) (CDR-SOB)
- Mini mental state exam (MMSE)
- APOE ε4 status
- amyloid beta 40
- amyloid beta 42
- hippocampal volume
- hippocampal atrophy
