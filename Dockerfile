FROM python:3.9

WORKDIR /home
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

EXPOSE 8443

COPY ./app/ ./app/

ENV SSL_KEYFILE=${SSL_KEYFILE}
ENV SSL_CERTFILE=${SSL_CERTFILE}

CMD ["python", "app/main.py"]
