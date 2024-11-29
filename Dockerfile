FROM python:3.12.7
ADD . /code
WORKDIR /code
ENTRYPOINT ["flask", "run"]