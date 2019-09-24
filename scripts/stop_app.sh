#!/bin/bash

cd /src/api-flat

isExistApp="pgrep docker"
if [[ -n $isExistApp ]]; then
	docker-compose down
fi
