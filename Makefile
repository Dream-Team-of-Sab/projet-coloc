USERNAME:= maxrib
IMAGE:= flat_manager
TAG:= $(shell TZ=UTC date + "%Y%m%d")

all: 

test:
	pipenv run pytest

build:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG)

run:
	docker run -it -p 5000:5000 $(USERNAME)/$(IMAGE):$(TAG)

deliver:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG)
	docker login
	docker tag $(USERNAME)/$(IMAGE):$(TAG1) $(USERNAME)/$(IMAGE):latest 
	docker push $(USERNAME)/$(IMAGE):latest

deploy:
	#utiliser un orchestrateur   
