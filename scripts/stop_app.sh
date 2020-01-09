#!/bin/bash

cd /src/api-flat
isExistApp="pgrep docker"
if [[ -n $isExistApp ]]; then
	docker stop $(docker ps -a -q)
	docker rm $(docker ps -a -q)
fi
