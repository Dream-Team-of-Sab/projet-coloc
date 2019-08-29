USERNAME:= maxrib
IMAGE:= flat_manager
TAG:= $(shell TZ=UTC date +"%Y%m%d")

all: 

test:
	docker run -it -p 5000:5000 $(USERNAME)/$(IMAGE):$(TAG) 
	pipenv run pytest

build:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG) .

run:
	docker run -it -p 5000:5000 $(USERNAME)/$(IMAGE):$(TAG)

deliver:
	docker login
	docker tag $(USERNAME)/$(IMAGE):$(TAG) $(USERNAME)/$(IMAGE):latest 
	docker push $(USERNAME)/$(IMAGE):latest

deploy:
	#utiliser un orchestrateur   
