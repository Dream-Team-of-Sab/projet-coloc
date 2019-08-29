FROM debian:10

RUN apt-get update \
    && apt-get install -y python3 sqlite3 python3-pip

RUN pip3 install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install flask pytest

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY coloc_project.py /usr/src/.
COPY app/ /usr/src/app/
COPY tests/ /usr/src/tests/
COPY Makefile /usr/src/.
    
WORKDIR /usr/src/

#pour le bash soit directement dans le fichier app
EXPOSE 5000

CMD pipenv run python3 coloc_project.py  
