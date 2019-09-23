#!/bin/bash

isExistApp="pgrep docker"
if [[ -n $isExistApp ]]; then
	docker-compose down
fi
