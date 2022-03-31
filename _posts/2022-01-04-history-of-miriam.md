---
layout: post
title: A History of MIRIAM and Identifiers.org
date: 2022-01-04 15:17:00 +0100
author: Charles Tapley Hoyt
tags: semantics
---
The proliferation of computational models describing biological phenomena
coincident with the emergence of high throughput experimental techniques at the
beginning of the millennium motivated the development of the Minimum Information
Requested in the Annotation of Models (MIRIAM; Le Novère *et al.*, 2005)
guidelines to facilitate their exchange and reuse. One of its three tenets was
to adopt modeling standards like CellML (Garny *et al*, 2008), SBML (Hucka *et al.*, 2003),
and BioPAX (Demir *et al.* 2010) and reference biomedical entities
via high quality controlled vocabularies and databases such as the Gene
Ontology (The Gene Ontology Consortium, 2019), UniProt (Bateman *et al.*, 2021),
and Reactome (Jassal *et al.*, (2020) using unambiguous uniform resource
identifiers (URIs).

In parallel, the MIRIAM Resources (Laibe & Le Novère, 2007) database was
developed to provide metadata about high quality resources including their
names, descriptions, homepages, and associated URIs. Its scope evolved, likely
due to the heterogeneity of URIs and further influence from semantic web, to
assign prefixes to each resource and simplify references to use compact URIs
(CURIEs; sometimes also written as compact identifiers) that comprise only a
prefix and a local unique identifier (Juty *et al.*, 2012). The Identifiers.org
service was deployed to validate and resolve compact URIs as well as assign them
stable URIs in the form of `https://identifiers.org/<prefix>:<identifier>` (Juty *et al.*, 2012)
and later began coordination with the similar Name-to-Thing (N2T) service (Wimalaratne *et al.*, 2018).
The proliferation of biomedical ontologies supporting  the standardization of
biomedical terminologies, thesauri, and taxonomies led to the development of the
Open Biomedical Ontologies (OBO) Foundry (Smith *et al.*, 2007) to coordinate
their evolution and support their integration. Most are modeled,
updated, and maintained using semantic web technologies such as the web ontology
language (OWL) that relies on URIs, the Protégé editor (Musen *et al.*, 2015),
and the ROBOT tool (Jackson *et al.*, 2019). In order to
support the assignment and usage of stable URIs, they use combination of the
Internet Archive's persistent URL (PURL) system and a biomedical domain-specific
PURL system hosted by the OBO Foundry. There are several lookup services that
summarize terms in OBO Foundry ontologies such as AberOwl (Hoehndorf *et al.*, 2015),
Ontobee (ref), and Ontology Lookup Service (OLS; ref) as well
repositories with relaxed quality constraints like BioPortal (ref) that include
additional ontologies not present in the OBO Foundry.

### Bibliography

1. Le Novère, N., *et al.*, (2005). Minimum information requested in the
   annotation of biochemical models (MIRIAM). Nature Biotechnology, 23(12),
   1509–1515. https://doi.org/10.1038/nbt1156
2. Garny, A., *et al.*, (2008). CellML and associated tools and techniques.
   Philosophical Transactions. Series A, Mathematical, Physical, and Engineering
   Sciences, 366(1878), 3017–3043. https://doi.org/10.1098/rsta.2008.0094
3. Hucka, M., *et al.*, (2003). The systems biology markup language (SBML): a
   medium for representation and exchange of biochemical network models.
   Bioinformatics, 19(4), 524–531. https://doi.org/10.1093/bioinformatics/btg015
4. Demir, E., *et al.* (2010). The BioPAX community standard for pathway data
   sharing. Nature Biotechnology, 28(12),
   1308–1308. https://doi.org/10.1038/nbt1210-1308c
5. The Gene Ontology Consortium. (2019). The Gene Ontology Resource: 20 years
   and still GOing strong. Nucleic Acids Research, 47(D1),
   D330–D338. https://doi.org/10.1093/nar/gky1055
6. Bateman, A., *et al.* (2021). UniProt: the universal protein knowledgebase in
    2021. Nucleic Acids Research, 49(D1),
          D480–D489. https://doi.org/10.1093/nar/gkaa1100
7. Jassal, B., *et al.* (2020). The reactome pathway knowledgebase. Nucleic
   Acids Research, 48(D1), D498–D503. https://doi.org/10.1093/nar/gkz1031
8. Laibe, C., & Le Novère, N. (2007). MIRIAM Resources: tools to generate and
   resolve robust cross-references in Systems Biology. BMC Systems Biology, 1,
    58. https://doi.org/10.1186/1752-0509-1-58
9. Juty, N., *et al.* (2012). Identifiers.org and MIRIAM Registry: Community
   resources to provide persistent identification. Nucleic Acids Research, 40(
   D1), 580–586. https://doi.org/10.1093/nar/gkr1097
10. Wimalaratne, S. M., *et al.* (2015). SPARQL-enabled identifier conversion
    with Identifiers.org. Bioinformatics, 31(11),
    1875–1877. https://doi.org/10.1093/bioinformatics/btv064
11. Smith, B., et al. (2007). The OBO Foundry: coordinated evolution of
    ontologies to support biomedical data integration. Nature Biotechnology, 25(
    11), 1251–1255. https://doi.org/10.1038/nbt1346
