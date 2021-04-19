## Installing Docker and ``docker-compose``


## Writing a Dockerfile

https://github.com/bionames/bionames-docker

```dockerfile
FROM python:3.8

RUN python -m pip install --upgrade pip
RUN python -m pip install gunicorn
RUN python -m pip install git+https://github.com/pyobo/pyobo.git#egg=pyobo[web,database]
ENTRYPOINT pyobo apps resolver --port 8765 --host "0.0.0.0" --sql --with-gunicorn --workers 4
```

```yaml
version: '3'

services:
  resolver:
    build: .
    environment:
      PYOBO_SQLALCHEMY_URI: ${PYOBO_SQLALCHEMY_URI}
    restart: always
    ports:
      - 8765:8765
```

```bash
docker-compose up --build
```

## Pushing to Dockerhub

https://ropenscilabs.github.io/r-docker-tutorial/04-Dockerhub.html

```shell
docker login
docker tag bb23120a27a1 cthoyt/bionames:latest
docker push cthoyt/bionames
```

