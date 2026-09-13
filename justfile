serve:
  # Note that the 4.2.0 tag is important - 4.2.2 (latest, released ~2022) does not work.
  docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:4.2.0 jekyll serve

pinact:
  pinact run --update

format:
  ruff format
  ruff check --fix --unsafe-fixes .
  pnpx prettier --prose-wrap always --write --check "**/*.md"
  pnpx prettier --prose-wrap always --write --check "**/*.yml"
  pnpx prettier --prose-wrap always --write --check "_includes/custom-head.html"

format-rumdl:
    uvx rumdl fmt

check:
    uvx rumdl check

spelling:
    uvx codespell --builtin 'clear,rare,en-GB_to_en-US' **/*.md
    grep -r "the the"
    grep -r "all of"

clean:
    rm -rf _site
    rm -rf .rumdl_cache
