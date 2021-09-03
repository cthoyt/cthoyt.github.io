---
layout: post
title: Pre-loading a PostgreSQL Docker Container
date: 2021-08-28 15:44:00 +0100
author: Charles Tapley Hoyt
tags: docker ontology
---
[PostgreSQL](https://www.postgresql.org/) is a powerful relational database management system that
can be easily downloaded and installed from
its [official image on DockerHub](https://hub.docker.com/_/postgres)
using [Docker](https://www.docker.com/). However, it's not so straightforward to pre-load your own
data. This blog post is about preparing a derivative of the base PostgreSQL Docker image that's
preloaded with your own database and pushing it back to DockerHub for redistribution.

**Prerequisites** I'm going to assume you have a modern version of docker running. I'm using
[Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac/). I've
also installed PostgreSQL using `brew install postgresql`, which puts a suite of command line
utilities, including `createdb`, which I use in the middle of this tutorial. I'm usually
using [fish](https://fishshell.com/), but the following instructions are given with Bourne-again
shell (bash) syntax.

**Notes** Throughout this post, I'll shorten PostgreSQL to postgres. All the commands in this
tutorial are run from the shell of the host system, i.e. I did not ssh or exec into the Docker image
itself to run them.

## Run the base image

The first step is to run a base image. This could be as simple as `docker run postgres`, but there
are a few options to add to make the rest of this process more simple. I've written this post while
preparing the docker image for the Biolookup Service, so `biolookup` appears many times as
names/passwords throughout. I'll definitely be writing another post soon about what that service is
and what it does (think [Ontology Lookup Service](https://www.ebi.ac.uk/ols/index), but not just
restricted to ontologies).

```shell
$ docker pull postgres
$ docker run \
    -p 5434:5432 \
    --name postgres-biolookup \
    --detach \
    -e POSTGRES_PASSWORD=biolookup \
    -e PGDATA=/var/lib/postgresql/pgdata \
    --shm-size 1gb
    postgres
```

1. `-p`/`--publish` This takes an argument looking like `<X>:<Y>`. The `<Y>` corresponds to the port
   inside the docker container, and the `<X>` corresponds to what's visible outside. I'm mapping
   from the default postgres port inside the container (i.e., 5432) to a non-default one outside
   (i.e., 5434) to avoid conflict with my local installation of postgres.
3. `--name` This gives a nice name to the container for lookup later. This doesn't have to be the
   same as the name you give when you push to dockerhub, but it's probably better to stay
   consistent. If you don't give one, docker assigns a silly name for you.
4. `-d`/`--detach` Rather than running in my current shell, this backgrounds it. Since I
   used `--name`, I can look up my image directly
   using `$(docker ps --filter "name=postgres-biolookup" -q)`.
5. `-e`/`--env` This allows you to specify environment variables.
    1. Setting `POSTGRES_PASSWORD` explicitly sets the password for the default postgres user
       (named `postgres`).
    3. Setting `PGDATA` ensures that a docker commit will actually persist the database's content.
       The cryptic path that came after is just the standard path postgres uses. Move along.
6. `--shm-size` By default, the shared memory is 64mb. When loading up this big database, this
   caused the following crash:

   ```python-traceback
     ...
     File "/Users/cthoyt/dev/pyobo/src/pyobo/database/sql/cli.py", line 52, in load
       _load(
     File "/Users/cthoyt/dev/pyobo/src/pyobo/database/sql/loader.py", line 65, in load
       _load_definition(engine=engine, table=defs_table, path=defs_path, test=test)
     File "/Users/cthoyt/dev/pyobo/src/pyobo/database/sql/loader.py", line 97, in _load_definition
       _load_table(
     File "/Users/cthoyt/dev/pyobo/src/pyobo/database/sql/loader.py", line 311, in _load_table
       cursor.execute(sql)
   psycopg2.errors.DiskFull: could not resize shared memory segment "/PostgreSQL.1699521131" to 67128576 bytes: No space left on device
   ```

   Luckily, [StackOverflow](https://stackoverflow.com/questions/56751565/pq-could-not-resize-shared-memory-segment-no-space-left-on-device)
   had me covered and suggested increasing the shared memory to 1gb using `--shm-size`.

## Create the database

Creating the database on the already running postgres docker image is a bit more straightforwards:

```shell
$ PGPASSWORD=biolookup createdb -h localhost -p 5434 -U postgres biolookup
```

`PGPASSWORD=biolookup` sets the password in the environment when this command gets run so there's no
need to manually interact with it. `-h` is for host, `-p` is for password, and `-U` is for
username. `-e` can be added optionally to show the commands that are run for debugging. The final
part `biolookup` is the name of the database that gets created.

## Load the database

The motivation for this post was to prepare a rather large database for the Biolookup Service, which
contains hundreds of millions of identifiers, names, definitions, and alternative identifiers for
biomedical entities. I've written [previously]({% post_url 2020-04-18-ooh-na-na %}) about building
this database, which after an incredible effort boils down to running
`pyobo database build` from the shell. It also automatically uploads its contents to Zenodo:

| Data                    | DOI                                                                                                       |
|-------------------------|-----------------------------------------------------------------------------------------------------------|
| Names                   | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4660694.svg)](https://doi.org/10.5281/zenodo.4660694) |
| Definitions             | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4662925.svg)](https://doi.org/10.5281/zenodo.4662925) |
| Alternative Identifiers | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4661368.svg)](https://doi.org/10.5281/zenodo.4661368) |
| Species                 | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5334738.svg)](https://doi.org/10.5281/zenodo.5334738) |

Loading the database requires the [`biolookup`](https://github.com/biopragmatics/biolookup) Python
package. It automatically downloads the data from the latest releases on Zenodo if not available
locally, then puts it in the database.

```shell
$ python -m pip install biolookup
$ biolookup load --uri postgresql+psycopg2://postgres:biolookup@localhost:5434/biolookup --test
```

The `--test` makes the database only load 100K records instead of hundreds of millions of records.
For building a real database, remove this.

## Commit and push to DockerHub

The `docker commit` checks what the difference between the base image and the current state of the
image is. Because of the `-e PGDATA=...`, it also tracks the new data added. For the Biolookup
Service, the image has gone from about 300mb to almost 40gb, so be patient. I went and made
breakfast while this was happening and it was done by the time I came back. For reference, it was a
saturday morning American breakfast.

```shell
$ docker commit \
    -a "Charles Tapley Hoyt <cthoyt@gmail.com>" \
    -m "Added biolookup schema and data" \
    $(docker ps --filter "name=postgres-biolookup" -q) \
    biopragmatics/postgres-biolookup:latest
```

After committing, it's time to push to DockerHub. You might need to do `docker login` before this.
The name of the image takes the form `<organization>/<name>[:<tag>]`. Make sure you push to an
organization that you have rights to, and the tag (the part after the colon) is optional.

```shell
$ docker push biopragmatics/postgres-biolookup:latest
```

You can check to see it was uploaded
properly [here](https://hub.docker.com/repository/docker/biopragmatics/postgres-biolookup).

## Run locally

Since the `biolookup` web application is automatically installed with PyOBO and the database is now
built locally, you can test it locally with:

```shell
$ biolookup web --sql --uri postgresql+psycopg2://postgres:biolookup@localhost:5434/biolookup
```

## Run with Docker Compose

You can use the following configuration as a `docker-compose.yml` file to orchestrate the pre-loaded
database with the front-end web application (more information on
that [here](https://github.com/biopragmatics/biolookup-docker/)):

```yaml
version: '3'

services:
  app:
    image: biopragmatics/biolookup:latest
    environment:
      BIOLOOKUP_SQLALCHEMY_URI: postgresql+psycopg2://postgres:biolookup@database/biolookup
    restart: always
    ports:
      - "8765:8765"
    depends_on:
      - database
  database:
    image: biopragmatics/postgres-biolookup:latest
    ports:
      - "5432:5432"
```

You can run this with `docker-compose up --detach`. When you do this, you need to be patient (1-5
minutes) for the database to start up before making requests from the web application. If you didn't
detach when running docker-compose, postgres will actually log when it's ready. If you try making a
request before it's done starting, you'll probably get an error message that looks like this:

```python-traceback
Traceback (most recent call last):
  ...
  File "/usr/local/lib/python3.9/site-packages/sqlalchemy/pool/base.py", line 605, in __connect
    connection = pool._invoke_creator(self)
  File "/usr/local/lib/python3.9/site-packages/sqlalchemy/engine/create.py", line 578, in connect
    return dialect.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.9/site-packages/sqlalchemy/engine/default.py", line 584, in connect
    return self.dbapi.connect(*cargs, **cparams)
  File "/usr/local/lib/python3.9/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) FATAL:  the database system is starting up
```

If you want to more correct about this, you can use the
[`pg_isready`](https://www.postgresql.org/docs/current/app-pg-isready.html) to check the connection
status of a PostgreSQL server. But I think it's practical enough just to wait a few minutes

## Next Steps

My next steps are to figure out the best way to automate the first three steps (running the base
image, creating the database, and loading the database) then hopefully do it in an automated setting
in GitHub Actions.

---

Special thanks to [Ben Gyori](https://github.com/bgyori) for outlining how to do this and getting me
going in the right direction. Thanks to [Scott Colby](https://github.com/scolby33) for feedback and
pro docker tips.
