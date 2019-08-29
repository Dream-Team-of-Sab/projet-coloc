FROM python:3.7-buster
# FROM debian:10

RUN apt-get update \
    && apt-get install -y sqlite3

RUN pip3 install pipenv

WORKDIR /app/

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY .  /app
RUN pipenv install

#pour le bash soit directement dans le fichier app
EXPOSE 5000

CMD pipenv run python3 coloc_project.py  
