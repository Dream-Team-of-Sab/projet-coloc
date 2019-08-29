FROM debian:10

RUN apt-get update \
    && apt-get install -y python3 sqlite3 python3-pip

RUN pip3 install pipenv

COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock

WORKDIR /app/

RUN pipenv install

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY .  /app

#pour le bash soit directement dans le fichier app
EXPOSE 5000

CMD pipenv run python3 coloc_project.py  
