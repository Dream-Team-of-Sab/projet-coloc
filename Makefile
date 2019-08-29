USERNAME:= thomasbar
IMAGE:=appy_flat
TAG:=$(shell TZ=UTC date +"%Y%m%d")

all: 

build:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG) .
run: 
	docker run -it -p 5000:5000  $(USERNAME)/$(IMAGE):$(TAG)

test: 
	docker run -it $(USERNAME)/$(IMAGE):$(TAG) pipenv run pytest

deliver: 
	docker login 
	docker tag $(USERNAME)/$(IMAGE):$(TAG) $(USERNAME)/$(IMAGE):latest	
	docker push $(USERNAME)/$(IMAGE):latest
	
