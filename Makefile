---

all: 

build:
	sudo docker-compose up 

test: 
	pipenv run pytest

deliver: 
	./starting_app.sh

