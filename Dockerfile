FROM nikolaik/python-nodejs:python3.9-nodejs14-alpine

RUN apk --update --no-cache add git openssh gcc musl-dev libffi-dev
RUN pip install PyGithub

COPY src/main.py /main.py

ENTRYPOINT [ "python", "/main.py" ]