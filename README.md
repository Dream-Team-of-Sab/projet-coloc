# README

# starting the app :

#  >> (sudo) docker-compose up

# Restarting application and db :

#  >> make reset_docker

# Restarting application and db :

#  You need to remove the docker volume if you want to erase
#  DB. In order to do this, use the following command:

#  >> (sudo) docker volume rm <volume name>

#  And if you don't know the volume name :
#  >> (sudo) docker volume ls

#  After this, use:
#  >> make reset docker

# and go to "http://0.0.0.0/" on your favorite browser and enjoy ;)
