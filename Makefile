---

all: 

build:
	sudo docker-compose up -d

test: 
	pipenv run pytest

deliver: 
	./starting_app.sh

