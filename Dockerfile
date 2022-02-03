FROM nikolaik/python-nodejs:python3.10-nodejs17-alpine

RUN apk --update --no-cache add git openssh gcc musl-dev libffi-dev

COPY src/main.py /main.py

RUN pip install PyGithub
ENTRYPOINT [ "python", "/main.py" ]