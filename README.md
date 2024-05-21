# cthoyt.github.io

My personal website, served at https://cthoyt.com

## Serve Locally

```shell
docker run --rm --volume="$PWD:/srv/jekyll" -p 4000:4000 -it jekyll/jekyll:4.2.0 jekyll serve
```

Note that the 4.2.0 tag is important - 4.2.2 (latest, released ~2022) does not work.

## License

CC BY 4.0
