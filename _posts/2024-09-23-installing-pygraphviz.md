---
layout: post
title: Building Graphviz when installing PyGraphviz
date: 2024-11-05 08:48:00 +0200
author: Charles Tapley Hoyt
tags:
  - Python
  - GraphViz
  - Environments
---

[Graphviz](https://graphviz.org) is software for graph visualization written in
C. [PyGraphviz](https://pypi.org/project/pygraphviz) provides a nice Python
wrapper for it. The issue is that getting Python to know about the C headers
changes every few months. I'll try and keep this blog post updated every time
there are some changes.

# November 2024

These days, `pip install graphviz` seemed to work but `uv pip install graphviz`
gave the following:

```console
$ uv pip install pygraphviz
Using Python 3.12.7 environment at /Users/cthoyt/.virtualenvs/orcid
Resolved 1 package in 597ms
error: Failed to prepare distributions
  Caused by: Failed to download and build `pygraphviz==1.14`
  Caused by: Build backend failed to build wheel through `build_wheel` (exit status: 1)

[stdout]
running bdist_wheel
running build
running build_py
creating build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/scraper.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/graphviz.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/__init__.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/agraph.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/testing.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
creating build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_unicode.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_scraper.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_readwrite.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_string.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/__init__.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_html.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_node_attributes.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_drawing.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_repr_mimebundle.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_subgraph.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_close.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_edge_attributes.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_clear.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_layout.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_attribute_defaults.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
copying pygraphviz/tests/test_graph.py -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz/tests
running egg_info
writing pygraphviz.egg-info/PKG-INFO
writing dependency_links to pygraphviz.egg-info/dependency_links.txt
writing top-level names to pygraphviz.egg-info/top_level.txt
reading manifest file 'pygraphviz.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
adding license file 'LICENSE'
writing manifest file 'pygraphviz.egg-info/SOURCES.txt'
copying pygraphviz/graphviz.i -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
copying pygraphviz/graphviz_wrap.c -> build/lib.macosx-14.0-arm64-cpython-312/pygraphviz
running build_ext
building 'pygraphviz._graphviz' extension
creating build/temp.macosx-14.0-arm64-cpython-312/pygraphviz
clang -fno-strict-overflow -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX14.sdk -DSWIG_PYTHON_STRICT_BYTE_CHAR -I/Users/cthoyt/Library/Caches/uv/builds-v0/.tmpKw7zNP/include -I/opt/homebrew/opt/python@3.12/Frameworks/Python.framework/Versions/3.12/include/python3.12 -c pygraphviz/graphviz_wrap.c -o build/temp.macosx-14.0-arm64-cpython-312/pygraphviz/graphviz_wrap.o

[stderr]
warning: no files found matching '*.swg'
warning: no files found matching '*.png' under directory 'doc'
warning: no files found matching '*.html' under directory 'doc'
warning: no files found matching '*.txt' under directory 'doc'
warning: no files found matching '*.css' under directory 'doc'
warning: no previously-included files matching '*~' found anywhere in distribution
warning: no previously-included files matching '*.pyc' found anywhere in distribution
warning: no previously-included files matching '.svn' found anywhere in distribution
no previously-included directories found matching 'doc/build'
pygraphviz/graphviz_wrap.c:9:9: warning: 'SWIG_PYTHON_STRICT_BYTE_CHAR' macro redefined [-Wmacro-redefined]
#define SWIG_PYTHON_STRICT_BYTE_CHAR
        ^
<command line>:2:9: note: previous definition is here
#define SWIG_PYTHON_STRICT_BYTE_CHAR 1
        ^
pygraphviz/graphviz_wrap.c:3023:10: fatal error: 'graphviz/cgraph.h' file not found
#include "graphviz/cgraph.h"
         ^~~~~~~~~~~~~~~~~~~
1 warning and 1 error generated.
error: command '/usr/bin/clang' failed with exit code 1
  Caused by: This error likely indicates that you need to install a library that provides "graphviz/cgraph.h" for pygraphviz@1.14
```

Here's one solution that work (of the many possible ones):

```python
$ export CFLAGS="-I$(brew --prefix graphviz)/include"
$ export LDFLAGS="-L$(brew --prefix graphviz)/lib"
$ uv pip install pygraphviz
Using Python 3.12.7 environment at /Users/cthoyt/.virtualenvs/orcid
Resolved 1 package in 2ms
   Built pygraphviz==1.14
Prepared 1 package in 908ms
Installed 1 package in 1ms
 + pygraphviz==1.14
```

There's also talk of using `--global-option` to pass
`-I/opt/homebrew/opt/graphviz/include` and `-L/opt/homebrew/opt/graphviz/lib`,
but I couldn't figure this out for `uv pip install`.

# 2023 Era

I was on Python 3.10 on a M2 Mac with macOS 13. `pygraphviz` didn't have a
pre-built wheel for my systen so `python -m pip install pygraphviz` gave the
following error:

```console
$ python -m pip install pygraphviz
...
clang -Wno-unused-result -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX13.sdk -DSWIG_PYTHON_STRICT_BYTE_CHAR -I/Users/cthoyt/.virtualenvs/indra/include -I/usr/local/opt/python@3.10/Frameworks/Python.framework/Versions/3.10/include/python3.10 -c pygraphviz/graphviz_wrap.c -o build/temp.macosx-13-x86_64-cpython-310/pygraphviz/graphviz_wrap.o
      pygraphviz/graphviz_wrap.c:3020:10: fatal error: 'graphviz/cgraph.h' file not found
      #include "graphviz/cgraph.h"
               ^~~~~~~~~~~~~~~~~~~
      1 error generated.
      error: command '/usr/bin/clang' failed with exit code 1
      [end of output]
```

I figured out based on the Homebrew troubleshooting in the docs
(https://pygraphviz.github.io/documentation/stable/install.html#homebrew) that
the following works:

```shell
python -m pip install --use-pep517 \
    --config-setting="--global-option=build_ext" \
    --config-setting="--build-option=-I$(brew --prefix graphviz)/include/" \
    --config-setting="--build-option=-L$(brew --prefix graphviz)/lib/" \
    pygraphviz
```
