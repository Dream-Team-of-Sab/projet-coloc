FROM debian:10

RUN apt-get update \
    && apt-get install -y python3 sqlite3 python3-pip 

RUN pip3 install flask pytest

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY . /app 
    
#pour le bash soit directement dans le fichier app
WORKDIR /app 

EXPOSE 5000

CMD flask run --host=0.0.0.0 
