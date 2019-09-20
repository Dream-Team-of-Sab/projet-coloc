DOCKERHUB_USERNAME := thomasbar
IMAGE := api_flat
TAG := $(shell TZ=UTC date +"%Y%m%d")

all: 

build:
	sudo docker build -t $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) .

run: 
	sudo docker run -it -p 5000:5000 $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG)

rund:
	sudo docker run -d -p 5000:5000 $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG)

test: 
	docker run -it $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) pipenv run pytest

deliver: 
	echo "$(DOCKERHUB_PASSWORD)" | docker login -u "$(DOCKERHUB_USERNAME)" --password-stdin
	docker tag $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) $(DOCKERHUB_USERNAME)/$(IMAGE):latest	
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG)
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE):latest

clear_docker:
	sudo docker-compose down
	sudo docker volume rm api_flat_project_dev_data

reset_docker:
	sudo docker-compose down
	sudo docker volume rm api_flat_project_dev_data
	sudo docker-compose up

#postgres_serv:
#	sudo docker run -it -p 5432\
#			-e "POSTGRES_USER=dev"\
#			-e "POSTGRES_PASSWORD=youwillneverguess"\
#			-e "POSTGRES_DB=api_flat_dev"\
#			-v dev_data:/var/lib/postgresql/data/\
#			postgres:11.5
