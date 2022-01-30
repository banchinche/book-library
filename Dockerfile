FROM python:3.10

WORKDIR /usr/src/api

RUN apt-get update && apt-get install -y netcat

COPY pyproject.toml /usr/src/api/pyproject.toml

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install --upgrade pip  &&\
    pip install poetry &&\
    poetry config virtualenvs.create false &&\
    poetry install --no-interaction &&\
    poetry shell

COPY . /usr/src/api/

RUN chmod +x entrypoint.sh

CMD ["/usr/src/api/entrypoint.sh"]
