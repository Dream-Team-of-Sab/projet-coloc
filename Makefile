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
	
