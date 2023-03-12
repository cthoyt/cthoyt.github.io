---
layout: post
title: Compliance of Bioregistry Prefixes to the W3C Standard
date: 2023-01-12 00:17:00 +0100
author: Charles Tapley Hoyt
tags: bioregistry prefixes w3c python
---
This post gives a brief background on the formal definition of the syntax and semantics of [compact uniform
resource identifiers (CURIEs)](https://www.w3.org/TR/2010/NOTE-curie-20101216/#s_syntax) from
the [Worldwide Web Consortium (W3C)](https://www.w3.org) and investigates how many prefixes in the
[Bioregistry](https://bioregistry.io) are compliant with the standard.

## Syntax

The W3C's [CURIE 1.0 Syntax](https://www.w3.org/TR/2010/NOTE-curie-20101216/#s_syntax) is unfortunately obfuscated.
Understanding it requires navigating through several pages and reading cryptic definitions in a
[BNF](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_form)-like notation. Below is a short explanation of the two
important parts and a nice simplification:

```
safe_curie  :=  '[' curie ']'
curie       :=  [ [ prefix ] ':' ] reference
prefix      :=  NCName
reference   :=  irelative-ref 
```

where `NCName` is defined [on this page](http://www.w3.org/TR/1999/REC-xml-names-19990114/#NT-NCName) as

```
NCName     ::= (Letter | '_') (NCNameChar)*
NCNameChar ::= Letter | Digit  | '.' | '-' | '_' | CombiningChar | Extender
```

and `irelative-ref` is defined [here](https://www.w3.org/TR/2010/NOTE-curie-20101216/#ref_IRI)
by referencing external [RFC 3987](http://www.ietf.org/rfc/rfc3987.txt). Understanding this part is not strictly
necessary for checking Bioregistry prefixes.

After unpacking all of these nested references and making the reasonable assumption that the strange characters
referenced by `CombiningChar` and `Extender` are unlikely to appear in any real prefixes, we arrive a the following
regular expression for validating prefixes: `^[a-zA-Z_][a-zA-Z0-9.-_]*`

## Bioregistry Compliance

It's relatively easy to write a script that checks Bioregistry prefixes against this regular expression.

```python
import re
import bioregistry
from tabulate import tabulate

W3C_PREFIX = re.compile("^[a-zA-Z_][a-zA-Z0-9.-_]*")
failed = [
    (
        f"[{resource.prefix}](https://bioregistry.io/{resource.prefix})",
        resource.get_name(),
    )
    for resource in bioregistry.resources()
    if not W3C_PREFIX.match(resource.prefix)
]
print(tabulate(failed, headers=["prefix", "name"], tablefmt="github"))
```

This script produces the following table as an output:

| prefix                                                | name                                         |
|-------------------------------------------------------|----------------------------------------------|
| [3dmet](https://bioregistry.io/3dmet)                 | 3D Metabolites                               |
| [4dn.biosource](https://bioregistry.io/4dn.biosource) | 4D Nucleome Data Portal Biosource            |
| [4dn.replicate](https://bioregistry.io/4dn.replicate) | 4D Nucleome Data Portal Experiment Replicate |

Note that only three prefixes (at the time of writing) are non-compliant, each because it starts with a number
instead of a letter or underscore. Overall, the Bioregistry is doing pretty good! Note that this does not check
preferred prefixes nor synonyms. This might be good for a future update to this post or a follow-up post.

---
In the future, it might be nice to enforce some kind of prefix compliance at the unit test level to automate checking
prefixes are appropriate. This might also include a blacklist of certain generic prefixes (e.g., *gene*) or other
rules discussed in the
project's [contribution guidelines](https://github.com/biopragmatics/bioregistry/blob/main/docs/CONTRIBUTING.md).
