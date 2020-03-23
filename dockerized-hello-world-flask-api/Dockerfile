FROM python:latest

WORKDIR /app

RUN pip install flask

COPY . /app

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "hello.py" ]