---
layout: post
title: How to Curate the INDRA Database
date: 2021-09-14 09:47:00 +0100
author: Charles Tapley Hoyt
tags: nlp indra
---
With the recent paper on Gilda and approaching INDRA 2 and INDRA database papers
coming up, I've put together a visual guide on how to curate statements extracted
by INDRA through the web interface at https://db.indra.bio.

Navigate to the INDRA database portal using [this link](https://db.indra.bio).

![The landing page of the INDRA Database search](/img/indra_curation/01_navigate_to_site.png)

Register for an account if you don't already have one by clicking the register
box.

![Register for an account](/img/indra_curation/02_register.png)

Login with your email/password.

![](/img/indra_curation/03_login.png)

Enter search text. This can be a gene symbol, chemical, or any other biomedical
entity. In this tutorial, we'll search for "AKT1."

![](/img/indra_curation/04_begin_search.png)

Now, click the "Ground with Gilda" button.
[Gilda](https://github.com/indralab/gilda) will automatically look up the most
likely database identifier that goes with your search string. It's quite smart
and can even disambiguate different senses of the same word. If it's not sure,
it will ask you to pick from a list.

![](/img/indra_curation/05_input_text.png)

In this example, I chose AKT1, which was pretty easy for Gilda to ground and
didn't need me to check. It also reports the confidence in the grounding and
the namespace to which it grounded in the box. Click the search button
to get going to the next step!

![](/img/indra_curation/06_ground_with_gilda.png)

Now you will see the search results. On the left, it has many
kinds of statements that INDRA models. They're hierarchical, meaning you
can click on one to expand to more specific statement types.

On the right are badges for the different sources that give evidence for each
statement. The ones with the black text correspond to databases, like BioGRID,
and the ones with white text correspond to reading systems, like REACH.

![](/img/indra_curation/07_search_results.png)

The next image shows the expansion of `AKT affects BAD` to
`AKT1 phosphorylates BAD`. Note that the third level is the same as the second -
this is because there are actually some more specific phosphorylation events
contained in here as well!

![](/img/indra_curation/08_navigate_search_results.png)
![](/img/indra_curation/09_open_curation_menu.png)
![](/img/indra_curation/10_select_curation_type.png)
![](/img/indra_curation/11_submit_and_profit.png)

