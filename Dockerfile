FROM debian:10

RUN apt-get update \
    && apt-get install -y python3 sqlite3 python3-pip

RUN pip3  install Flask
    
CMD bash
 
