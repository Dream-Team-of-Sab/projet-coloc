USERNAME:=sabrinatony
IMAGE:=$(shell basename "$$(pwd)")
TAG:=$(shell TZ=UTC date +"%Y%m%d")

all: 

build:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG) .
run: 
	docker run -it -p5000:5000  $(USERNAME)/$(IMAGE):$(TAG)

test: 

deliver: 
	docker login 
	docker tag $(USERNAME)/$(IMAGE):$(TAG) $(USERNAME)/$(IMAGE):latest	
	docker push $(USERNAME)/$(IMAGE):latest
	
