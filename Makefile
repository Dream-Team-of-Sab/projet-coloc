DOCKERHUB_USERNAME ?= $(shell whoami)
IMAGE := appy_flat
TAG := $(shell TZ=UTC date +"%Y%m%d")

all: 

build:
	docker build -t $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) .

run: 
	@echo "Please use docker-compose to run this project"

test: 
	docker run -it $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) pipenv run pytest

deliver: 
	docker login 
	docker tag $(DOCKERHUB_USERNAME)/$(IMAGE):$(TAG) $(DOCKERHUB_USERNAME)/$(IMAGE):latest	
	docker push $(DOCKERHUB_USERNAME)/$(IMAGE):latest
	
