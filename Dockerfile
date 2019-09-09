FROM python:3.7-buster

RUN apt-get update \
    && apt-get install -y sqlite3

RUN pip3 install pipenv

WORKDIR /app/

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY .  /app
RUN pipenv install

CMD /bin/sh -c "pipenv run python3 db/sqlite_database_gen.py; pipenv run python3 api_flat.py"
