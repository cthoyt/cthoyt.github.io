---
layout: post
title:
  A Reading List of Academic Articles using the Biological Expression Language
  (BEL)
date: 2020-05-22 14:50:00 +0100
author: Charles Tapley Hoyt
tags: bel
---

This post is evolving from a reading list to a review of the academic papers
published that are either about or use the
[Biological Expression Language (BEL)](https://biological-expression-language.github.io).
It's divided into the categories of software/visualization tools,
algorithms/analytical frameworks, data integration, natural language processing,
curation workflows, and downstream applications.

In my [history of BEL]({% post_url 2020-04-28-history-of-bel %}), I imposed some
quality and impact standards. Without getting into a debate about how peer
review is broken because it's missing these standards, this list is more
inclusive to papers whether they are likely to be reproducible or useful to the
community, or not.

Some papers in this list were tricky to find - many of the PMI papers do not
mention BEL in the abstract and the journals in which their papers were
published don't seem to index properly in MEDLINE. You're welcome to use
[my search on PubMed](https://pubmed.ncbi.nlm.nih.gov/?term=%22biological+expression+language%22)
and
[my search on Europe PubMed Central](https://europepmc.org/search?query=%22biological%20expression%20language%22)
to see for yourself. I also looked through the publication lists of some key
authors from Selventa and PMI over the last 10 years to find several other
application papers. As always, this list is incomplete due to the lack of
findability/accessibility of papers, my lack of knowledge of _everything_, and
lack of time to deeply read through all authors' histories. If you know of a
search tool that might be helpful for improving this list, please let me know.
I've been meaning to check out CoCites:

<blockquote class="twitter-tweet" data-partner="tweetdeck"><p lang="en" dir="ltr">Am thrilled this paper is finally out. The most exciting project I&#39;ve ever worked on, a totally new method for searching scientific literature with stunning results.<br><br>We work to launch the method as a webtool in the coming months. Stay tuned. <a href="https://twitter.com/CoCites?ref_src=twsrc%5Etfw">@cocites</a><br>1/<a href="https://t.co/Ok7RW6yXIn">https://t.co/Ok7RW6yXIn</a> <a href="https://t.co/tkpRqOT6bj">pic.twitter.com/tkpRqOT6bj</a></p>&mdash; Cecile Janssens (@cecilejanssens) <a href="https://twitter.com/cecilejanssens/status/1225789201901215744?ref_src=twsrc%5Etfw">February 7, 2020</a></blockquote>

As always, improvements are welcome. Check my contact info at the bottom of this
post. I'll be making a major update to this post later to be more like a review
as I'm putting together the new BEL reference paper.

## Software and Visualization

[**PyBEL: a computational framework for Biological Expression Language**](https://doi.org/10.1093/bioinformatics/btx660).
<br /> Hoyt, C. T., Konotopez, A. & Ebeling, C. (2017). <br /> _Bioinformatics_,
**34**(4), 703–704.

[**BEL Commons: an environment for exploration and analysis of networks encoded in Biological Expression Language**](https://doi.org/10.1093/database).
<br /> Hoyt, C. T., Domingo-Fernández, D., & Hofmann-Apitius, M. (2018). <br />
_Database_, **2018**(3), 1–11

[**INDRA-IPM: Interactive pathway modeling using natural language with automated assembly**](https://doi.org/10.1093/bioinformatics/btz289).
<br /> Todorov, P. V., Gyori, B. M., Bachman, J. A., & Sorger, P. K. (2019).
<br /> _Bioinformatics_, **35**(21), 4501–4503.

## Algorithms and Analytical Frameworks

[**A network-based approach to quantifying the impact of biologically active substances**](https://doi.org/10.1016/j.drudis.2011.11.008).
<br /> Hoeng, J., Deehan, R., Pratt, D., Martin, F., Sewer, A., Thomson, T. M.,
Drubin, D. A., Waters, C. A., de Graaf, D., & Peitsch, M. C. (2012). <br />
_Drug Discovery Today_, **17**(9), 413–418.

[**Assessment of network perturbation amplitudes by applying high-throughput data to causal biological networks**](https://doi.org/10.1186/1752-0509-6-54).
<br /> Martin, F., Thomson, T. M., Sewer, A., Drubin, D. a, Mathis, C.,
Weisensee, D., Pratt, D., Hoeng, J., & Peitsch, M. C. (2012). <br /> _BMC
Systems Biology_, **6**, 54.

[**Quantitative assessment of biological impact using transcriptomic data and mechanistic network models**](https://doi.org/10.1016/j.taap.2013.07.007).
<br /> Thomson, T. M., Sewer, A., Martin, F., Belcastro, V., Frushour, B. P.,
Gebel, S., Park, J., Schlage, W. K., Talikka, M., Vasilyev, D. M., Westra, J.
W., Hoeng, J., & Peitsch, M. C. (2013). <br /> _Toxicology and Applied
Pharmacology_, **272**(3), 863–878.

[**Reverse causal reasoning: applying qualitative causal knowledge to the interpretation of high-throughput data**](https://doi.org/10.1186/1471-2105-14-340).
<br /> Catlett, N. L., Bargnesi, A. J., Ungerer, S., Seagaran, T., Ladd, W.,
Elliston, K. O., & Pratt, D. (2013). <br /> _BMC Bioinformatics_,
**14**(1), 340.

[**An algorithm for score aggregation over causal biological networks based on random walk sampling**](https://doi.org/10.1186/1756-0500-7-516).
<br /> Vasilyev, D. M., Thomson, T. M., Frushour, B. P., Martin, F., & Sewer, A.
(2014). <br /> _BMC Research Notes_, **7**, 516.

[**Quantification of biological network perturbations for mechanistic insight and diagnostics using two-layer causal models**](https://doi.org/10.1186/1471-2105-15-238).
<br /> Martin, F., Sewer, A., Talikka, M., Xiang, Y., Hoeng, J., & Peitsch, M.
C. (2014). <br /> _BMC Bioinformatics_, **15**(1), 238.

[**Multimodal mechanistic signatures for neurodegenerative diseases (NeuroMMSig): a web server for mechanism enrichment**](https://doi.org/10.1093/bioinformatics/btx399).
<br /> Domingo-Fernández, D., Kodamullil, A. T., Iyappan, A., Naz, M., Emon, M.
A., Raschka, T., Karki, R., Springstubbe, S., Ebeling, C., & Hofmann-Apitius, M.
(2017). <br /> _Bioinformatics_, **33**(22), 3679–3681.

[**BEL2ABM: Agent-based simulation of static models in Biological Expression Language**](https://doi.org/10.1093/bioinformatics/bty107).
<br /> Gündel, M., Hoyt, C. T., & Hofmann-Apitius, M. (2018). <br />
_Bioinformatics_, **34**(13), 2316–2318.

[**BioKEEN: a library for learning and evaluating biological knowledge graph embeddings**](https://doi.org/10.1093/bioinformatics/btz117).
<br /> Ali, M., Hoyt, C. T., Domingo-Fernández, D., Lehmann, J., & Jabeen, H.
(2019). <br /> _Bioinformatics_, **35**(18), 3538–3540.

[**Quantifying mechanisms in neurodegenerative diseases using candidate mechanism perturbation amplitude algorithm**](https://doi.org/10.1186/s12859-019-3101-1).
<br /> Karki, R., Kodamullil, A. T., Hoyt, C. T., & Hofmann-Apitius, M. (2019).
<br /> _BMC Bioinformatics_, **20**(1), 494.

[**NPA: an R package for computing network perturbation amplitudes using gene expression data and two-layer networks.**](https://doi.org/10.1186/s12859-019-3016-x).
<br /> Martin, F., Gubian, S., Talikka, M., Hoeng, J., & Peitsch, M. C. (2019).
<br /> _BMC Bioinformatics_, **20**(1), 451.

[**Leveraging Structured Biological Knowledge for Counterfactual Inference: a Case Study of Viral Pathogenesis**](https://doi.org/10.1109/TBDATA.2021.3050680)
<br /> Zucker, J., Paneri, K., Mohammad-Taheri, S., Bhargava, S., Kolambkar, P.,
Bakker, C., Teuton, J., Hoyt, C. T., Oxford, K., Ness, R., & Vitek, O. (2021).
<br /> _IEEE Transactions on Big Data_, 2021.3050680

## Data Integration

[**Using Drugs as Molecular Probes: A Computational Chemical Biology Approach in Neurodegenerative Diseases**](https://doi.org/10.3233/JAD-160222).
<br /> Emon, M. A. E. K., Kodamullil, A. T., Karki, R., Younesi, E., &
Hofmann-Apitius, M. (2017). <br /> _Journal of Alzheimer’s Disease_, **56**(2),
677–686.

[**ComPath: an ecosystem for exploring, analyzing, and curating mappings across pathway databases**](https://doi.org/10.1038/s41540-018-0078-8).
<br /> Domingo-Fernandez, D., Hoyt, C. T., Alvarez, C. B., Marin-Llao, J., &
Hofmann-Apitius, M. (2018). <br /> _npj Systems Biology and Applications_,
**5**(1), 3.

[**Integration of Structured Biological Data Sources using Biological Expression Language**](https://doi.org/10.1101/631812).
<br /> Hoyt, C. T., Domingo-Fernández, D., Mubeen, S., Llaó, J. M., Konotopez,
A., Ebeling, C., Birkenbihl, C., Muslu, Ö., English, B., Müller, S., de Lacerda,
M. P., Ali, M., Colby, S., Türei, D., Palacio-Escat, N., & Hofmann-Apitius, M.
(2019). <br /> _bioRxiv_, 631812.

[**PathMe: merging and exploring mechanistic pathway knowledge**](https://doi.org/10.1186/s12859-019-2863-9).
<br /> Domingo-Fernández, D., Mubeen, S., Marín-Llaó, J., Hoyt, C. T., &
Hofmann-Apitius, M. (2019). <br /> _BMC Bioinformatics_, **20**(1), 243.

[**The Impact of Pathway Database Choice on Statistical Enrichment Analysis and Predictive Modeling**](https://doi.org/10.3389/fgene.2019.01203).
<br /> Mubeen, S., Hoyt, C. T., Gemünd, A., Hofmann-Apitius, M., Fröhlich, H., &
Domingo-Fernández, D. (2019). <br /> _Frontiers in Genetics_, **10**, 654442.

## Natural Language Processing

[**Construction of biological networks from unstructured information based on a semi-automated curation workflow**](https://doi.org/10.1093/database/bav057).
<br /> Szostak, J., Ansari, S., Madan, S., Fluck, J., Talikka, M., Iskandar, A.,
De Leon, H., Hofmann-Apitius, M., Peitsch, M. C., & Hoeng, J. (2015). <br />
_Database_, **2015**, bav057.

[**Training and evaluation corpora for the extraction of causal relationships encoded in biological expression language (BEL)**](https://doi.org/10.1093/database/baw113).
<br /> Fluck, J., Madan, S., Ansari, S., Kodamullil, A. T., Karki, R.,
Rastegar-Mojarad, M., Catlett, N. L., Hayes, W., Szostak, J., Hoeng, J., &
Peitsch, M. (2016). <br /> _Database_, **2016**, 1–20.

[**BioCreative V track 4: a shared task for the extraction of causal network information using the Biological Expression Language**](https://doi.org/10.1093/database/baw067).
<br /> Rinaldi, F., Ellendorff, T. R., Madan, S., Clematide, S., van der Lek,
A., Mevissen, T., & Fluck, J. (2016). <br /> _Database_, **2016**, baw067.

[**Coreference resolution improves extraction of Biological Expression Language statements from texts**](https://doi.org/10.1093/database/baw076).
<br /> Choi, M., Liu, H., Baumgartner, W., Zobel, J., & Verspoor, K. (2016).
<br /> _Database_, **2016**, 1–14.

[**The BEL information extraction workflow (BELIEF): evaluation in the BioCreative V BEL and IAT track**](https://doi.org/10.1093/database/baw136).
<br /> Madan, S., Hodapp, S., Senger, P., Ansari, S., Szostak, J., Hoeng, J.,
Peitsch, M., & Fluck, J. (2016). <br /> _Database_, **2016**(September), 1–17.

[**BelSmile: a biomedical semantic role labeling approach for extracting biological expression language from text**](https://doi.org/10.1093/database/baw064).
<br /> Lai, P. T., Lo, Y. Y., Huang, M. S., Hsiao, Y. C., & Tsai, R. T. H.
(2016). <br /> _Database_, **2016**(June), 1–9.

[**BELTracker: evidence sentence retrieval for BEL statements**](https://doi.org/10.1093/database/baw079).
<br /> Rastegar-Mojarad, M., Komandur Elayavilli, R., & Liu, H. (2016). <br />
_Database_, **2016**(June), 1–11.

[**BELMiner: Adapting a rule-based relation extraction system to extract biological expression language statements from bio-medical literature evidence sentences**](https://doi.org/10.1093/database/baw156).
<br /> Ravikumar, K. E., Rastegar-Mojarad, M., & Liu, H. (2017). <br />
_Database_, **2017**(1), 1–12.

[**Automatic Extraction of BEL-Statements based on Neural Networks**](http://publica.fraunhofer.de/eprints/urn_nbn_de_0011-n-4972978.pdf).
<br /> Ali, M., Madan, S., Fischer, A., Petzka, H., & Fluck, J. (2017). <br />
_Proceedings of BioCreative VI Challenge and Workshop_, October.

[**From word models to executable models of signaling networks using automated assembly**](https://doi.org/10.15252/msb.20177651).
<br /> Gyori, B. M., Bachman, J. A., Subramanian, K., Muhlich, J. L., Galescu,
L., & Sorger, P. K. (2017). <br /> _Molecular Systems Biology_, **13**(11), 954.

[**The extraction of complex relationships and their conversion to biological expression language (BEL) overview of the BioCreative VI (2017) BEL track**](https://doi.org/10.1093/database/baz084).
<br /> Madan, S., Szostak, J., Komandur Elayavilli, R., Tsai, R. T. H., Ali, M.,
Qian, L., Rastegar-Mojarad, M., Hoeng, J., & Fluck, J. (2019). <br />
_Database_, **2019**(1), 1–17.

[**Combining relation extraction with function detection for BEL statement extraction**](https://doi.org/10.1093/database/bay133).
<br /> Liu, S., Cheng, W., Qian, L., & Zhou, G. (2019). <br /> _Database_,
**2019**(4), 1–12.

[**Hierarchical sequence labeling for extracting BEL statements from biomedical literature**](https://doi.org/10.1186/s12911-019-0758-3).
<br /> Liu, S., Shao, Y., Qian, L., & Zhou, G. (2019). <br /> _BMC Medical
Informatics and Decision Making_, **19**(Suppl 2).

[**Extraction of causal relations based on SBEL and BERT model**](https://doi.org/10.1093/database/baab005)
<br /> Shao, Y., Li, H., Gu, J., Qian, L., & Zhou, G. (2021). <br /> _Database_,
**2021**.

## Curation Workflows

[**On crowd-verification of biological networks**](https://doi.org/10.4137/BBI.S12932).
<br /> Ansari, S., Binder, J., Boue, S., Di Fabio, A., Hayes, W., Hoeng, J.,
Iskandar, A., Kleiman, R., Norel, R., O’Neel, B., Peitsch, M. C., Poussin, C.,
Pratt, D., Rhrissorrakrai, K., Schlage, W. K., Stolovitzky, G., & Talikka, M.
(2013). <br /> _Bioinformatics and Biology Insights_, **7**, 307–325.

[**sbv IMPROVER: Modern Approach to Systems Biology BT - Biological Networks and Pathway Analysis**](https://doi.org/10.1007/978-1-4939-7027-8_2).
<br /> Guryanova, S., & Guryanova, A. (2017). <br /> _T. V Tatarinova & Y.
Nikolsky (eds.)_, pp. 21–29. Springer New York.

[**Re-curation and rational enrichment of knowledge graphs in Biological Expression Language**](https://doi.org/10.1093/database/baz068).
<br /> Hoyt, C. T., Domingo-Fernández, D., Aldisi, R., Xu, L., Kolpeja, K.,
Spalek, S., Wollert, E., Bachman, J., Gyori, B. M., Greene, P., &
Hofmann-Apitius, M. (2019). <br /> _Database_, **2019**(1).

## Content and Applications

[**A computable cellular stress network model for non-diseased pulmonary and cardiovascular tissue**](https://doi.org/10.1186/1752-0509-5-168).
<br /> Schlage, W. K., Westra, J. W., Gebel, S., Catlett, N. L., Mathis, C.,
Frushour, B. P., Hengstermann, A., Van Hooser, A., Poussin, C., & Wong, B.
(2011). <br /> _BMC Syst Biol_, **5**.

[**Construction of a Computable Cell Proliferation Network Focused on Non-Diseased Lung Cells**](https://doi.org/10.1186/1752-0509-5-105).
<br /> Westra, J. W., Schlage, W. K., Frushour, B. P., Gebel, S., Catlett, N.
L., Han, W., Eddy, S. F., Hengstermann, A., Matthews, A. L., & Mathis, C.
(2011). <br /> _BMC Syst Biol_, **5**.

[**Construction of a computable network model for DNA damage, autophagy, cell death, and senescence**](https://doi.org/10.4137/BBI.S11154).
<br /> Gebel, S., Lichtner, R. B., Frushour, B., Schlage, W. K., Hoang, V.,
Talikka, M., Hengstermann, A., Mathis, C., Veljkovic, E., Peck, M., Peitsch, M.
C., Deehan, R., Hoeng, J., & Westra, J. W. (2013). <br /> _Bioinformatics and
Biology Insights_, **7**, 97–117.

[**A modular cell-type focused inflammatory process network model for non-diseased pulmonary tissue**](https://doi.org/10.4137/BBI.S11509).
<br /> Westra, J. W., Schlage, W. K., Hengstermann, A., Gebel, S., Mathis, C.,
Thomson, T., Wong, B., Hoang, V., Veljkovic, E., Peck, M., Lichtner, R. B.,
Weisensee, D., Talikka, M., Deehan, R., Hoeng, J., & Peitsch, M. C. (2013).
<br /> _Bioinformatics and Biology Insights_, **7**, 167–192.

[**Systematic verification of upstream regulators of a computable cellular proliferation network model on non-diseased lung cells using a dedicated dataset**](https://doi.org/10.4137/BBI.S12167).
<br /> Belcastro, V., Poussin, C., Gebel, S., Mathis, C., Schlage, W. K.,
Lichtner, R. B., Quadt-Humme, S., Wagner, S., Hoeng, J., & Peitsch, M. C.
(2013). <br /> _Bioinformatics and Biology Insights_, **7**, 217–230.

[**Case study: the role of mechanistic network models in systems toxicology**](https://doi.org/10.1016/j.drudis.2013.07.023).
<br /> Hoeng, J., Talikka, M., Martin, F., Sewer, A., Yang, X., Iskandar, A.,
Schlage, W. K., & Peitsch, M. C. (2014). <br /> _Drug Discovery Today_,
**19**(2), 183–192.

[**In vitro systems toxicology approach to investigate the effects of repeated cigarette smoke exposure on human buccal and gingival organotypic epithelial tissue cultures.**](https://doi.org/10.3109/15376516.2014.943441).
<br /> Schlage, W. K., Iskandar, A. R., Kostadinova, R., Xiang, Y., Sewer, A.,
Majeed, S., Kuehn, D., Frentzel, S., Talikka, M., Geertz, M., Mathis, C.,
Ivanov, N., Hoeng, J., & Peitsch, M. C. (2014). <br /> Toxicology Mechanisms and
Methods, **24**(7), 470–487.

[**A vascular biology network model focused on inflammatory processes to investigate atherogenesis and plaque instability**](https://doi.org/10.1186/1479-5876-12-185).
<br /> De León, H., Boué, S., Schlage, W. K., Boukharov, N., Westra, J. W.,
Gebel, S., VanHooser, A., Talikka, M., Fields, R. B., Veljkovic, E., Peck, M.
J., Mathis, C., Hoang, V., Poussin, C., Deehan, R., Stolle, K., Hoeng, J., &
Peitsch, M. C. (2014). <br /> _Journal of Translational Medicine_, **12**(1).

[**Micropublications: A semantic model for claims, evidence, arguments and annotations in biomedical communications**](https://doi.org/10.1186/2041-1480-5-28).
<br /> Clark, T., Ciccarese, P. N., & Goble, C. A. (2014). <br /> _Journal of
Biomedical Semantics_, **5**(1), 1–33.

[**Computational Modelling Approaches on Epigenetic Factors in Neurodegenerative and Autoimmune Diseases and Their Mechanistic Analysis**](https://doi.org/10.1155/2015/737168).
<br /> Khanam Irin, A., Tom Kodamullil, A., Gündel, M., & Hofmann-Apitius, M.
(2015). <br /> _Journal of Immunology Research_, **2015**, 1–10.

[**Semi-automated curation allows causal network model building for the quantification of age-dependent plaque progression in ApoE−/− mouse**](https://doi.org/10.4137/GRSB.S40031).
<br /> Szostak, J., Martin, F., Talikka, M., Peitsch, M. C., & Hoeng, J. (2016).
<br /> _Gene Regulation and Systems Biology_, **10**, 95–103.

[**Community-reviewed biological network models for toxicology and drug discovery applications**](https://doi.org/10.4137/GRSB.S39076).
<br /> Namasivayam, A. A., Morales, A. F., Lacave, Á. M. F., Tallam, A.,
Simovic, B., Alfaro, D. G., Bobbili, D. R., Martin, F., Androsova, G.,
Shvydchenko, I., Park, J., Val Calvo, J., Hoeng, J., Peitsch, M. C., Racero, M.
G. V., Biryukov, M., Talikka, M., Pérez, M. B., Rohatgi, N., … Xiang, Y. (2016).
<br /> _Gene Regulation and Systems Biology_, **10**, 51–66.

[**Reasoning over genetic variance information in cause-and-effect models of neurodegenerative diseases**](https://doi.org/10.1093/bib/bbv063).
<br /> Naz, M., Kodamullil, A. T., & Hofmann-Apitius, M. (2016). <br />
_Briefings in Bioinformatics_, **17**(3), 505–516.

[**Of Mice and Men: Comparative Analysis of Neuro-Inflammatory Mechanisms in Human and Mouse Using Cause-and-Effect Models**](https://doi.org/10.3233/JAD-170255).
<br /> Kodamullil, A. T., Iyappan, A., Karki, R., Madan, S., Younesi, E., &
Hofmann-Apitius, M. (2017). <br /> _Journal of Alzheimer’s Disease_, **59**(3),
1045–1055.

[**Comorbidity Analysis between Alzheimer’s Disease and Type 2 Diabetes Mellitus (T2DM) Based on Shared Pathways and the Role of T2DM Drugs**](https://doi.org/10.3233/JAD-170440).
<br /> Karki, R., Kodamullil, A. T., & Hofmann-Apitius, M. (2017). <br />
_Journal of Alzheimer’s Disease_, **60**(2), 721–731.

[**Novel approaches to develop community-built biological network models for potential drug discovery**](https://doi.org/10.1080/17460441.2017.1335302).
<br /> Talikka, M., Bukharov, N., Hayes, W. S., Hofmann-Apitius, M.,
Alexopoulos, L., Peitsch, M. C., & Hoeng, J. (2017). <br /> _Expert Opinion on
Drug Discovery_, **12**(8), 849–857.

[**A systematic approach for identifying shared mechanisms in epilepsy and its comorbidities**](https://doi.org/10.1093/database/bay050).
<br /> Hoyt, C. T., Domingo-Fernández, D., Balzer, N., Güldenpfennig, A., &
Hofmann-Apitius, M. (2018). <br /> _Database_, **2018**(1).

[**Construction of a suite of computable biological network models focused on mucociliary clearance in the repiratory tract**](https://doi.org/10.3389/fgene.2019.00087).
<br /> Yepiskoposyan, H., Talikka, M., Vavassori, S., Martin, F., Sewer, A.,
Gubian, S., Luettich, K., Peitsch, M. C., & Hoeng, J. (2019). <br /> _Frontiers
in Genetics_, **10**(FEB), 1–12.

[**34th Annual Meeting & Pre-Conference Programs of the Society for Immunotherapy of Cancer (SITC 2019): part 2 : National Harbor, MD, USA. 10 November 2019**](https://doi.org/10.1186/s40425-019-0764-0).
<br /> (2019). <br /> _Journal for Immunotherapy of Cancer_, **7**(Suppl
1), 283.

- See entry entitled "Reverse causal inferencing on lung adenocarcinoma patients
  reveals a stem cell-like molecular subtype associated with pack year history"

[**The reduction of DSS-induced colitis severity in mice exposed to cigarette smoke is linked to immune modulation and microbial shifts.**](https://doi.org/10.1038/s41598-020-60175-3)
<br /> Lo Sasso, G., Phillips, B. W., Sewer, A., Battey, J. N. D., Kondylis, A.,
Talikka, M., Titz, B., Guedj, E., Peric, D., Bornand, D., Dulize, R., Merg, C.,
Corciulo, M., Ouadi, S., Yanuar, R., Tung, C. K., Ivanov, N. V, Peitsch, M. C.,
& Hoeng, J. (2020). <br /> _Scientific Reports_, **10**(1), 3829.

[**A Computational Approach for Mapping Heme Biology in the Context of Hemolytic Disorders**](https://doi.org/10.3389/fbioe.2020.00074).
<br /> Humayun, F., Domingo-Fernández, D., Paul George, A. A., Hopp, M. T.,
Syllwasschy, B. F., Detzel, M. S., Hoyt, C. T., Hofmann-Apitius, M., & Imhof, D.
(2020). <br /> _Frontiers in Bioengineering and Biotechnology_, **8**(March),
1–10.

[**COVID-19 Knowledge Graph: a computable, multi-modal, cause-and-effect knowledge model of COVID-19 pathophysiology**](https://doi.org/10.1101/2020.04.14.040667).
<br /> Domingo-Fernández, D., Baksi, S., Schultz, B., Gadiya, Y., Karki, R.,
Raschka, T., Ebeling, C., Hofmann-Apitius, M., & Kodamullil, A. T. (2020).
<br /> _bioRxiv_, 2020.04.14.040667.

[**Unravelling the debate on heme effects in COVID-19 infections**](https://doi.org/10.1101/2020.06.09.142125).
<br /> Hopp, M., Domingo-Fernández, D., Gadiya, Y., Detzel, M. S., Schmalohr, B.
F., Steinbock, F., Imhof, D., & Martin Hofmann-Apitius, M. (2020). <br />
_bioRxiv_, 2020.06.09.142125

[**Data-Driven Modeling of Knowledge Assemblies in Understanding Comorbidity Between Type 2 Diabetes Mellitus and Alzheimer’s Disease**](https://doi.org/10.3233/JAD-200752).
<br /> Karki, R., Madan, S., Gadiya, Y., Domingo-Fernández, D., Kodamullil, A.
T., & Hofmann-Apitius, M. (2020). <br /> _Journal of Alzheimer’s Disease_,
**78**(1), 87–95.

[**A Systems Biology Approach for Hypothesizing the Effect of Genetic Variants on Neuroimaging Features in Alzheimer’s Disease**](https://doi.org/10.3233/JAD-201397).
<br /> Khatami, S. G., Domingo-Fernández, D., Mubeen, S., Hoyt, C. T., Robinson,
C., Karki, R., Iyappan, A., Kodamullil, A. T., & Hofmann-Apitius, M. (2021).
<br /> _Journal of Alzheimer’s Disease_, 201397
