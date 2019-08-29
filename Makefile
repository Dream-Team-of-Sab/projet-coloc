USERNAME:=thomasbar
IMAGE:=flat_manager
TAG:=$(shell TZ=UTC date +"%Y%m%d")
all: build run

build:
	docker build -t $(USERNAME)/$(IMAGE):$(TAG) .

run:
	#A remplir

test:
	docker run -it $(USERNAME)/$(IMAGE):$(TAG) pipenv run pytest # Necessite d'ajouter le repertoire 'tests/'
	                                                             # comprenant des tests fonctionnels

# On produit des binaires, on les stocke qqpart
#
deliver:
	#A remplir

# On utilise les binaires pour faire
# fonctionner le service
#
# deploy:
#     # A remplir
