FROM python:3.7-buster

RUN pip install pipenv

EXPOSE 5000

CMD bash
