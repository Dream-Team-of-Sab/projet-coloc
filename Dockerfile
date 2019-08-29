FROM debian:10

RUN apt-get update && apt-get install -y python3 python3-psycopg2 python3-pip 

RUN pip3 install flask virtualenv python-dotenv psycopg2

# pour mettre tout le code source dans le dossier app qui se situe dans le container
COPY ./coloc_project /app
    
#pour le bash soit directement dans le fichier app
WORKDIR /app

#Pour configurer l'environnement
run virtualenv venv

CMD bash -c "python3 app/database_gen.py;source venv/Scripts/activate;export FLASK_APP=coloc_project.py;flask run --host=0.0.0.0"

