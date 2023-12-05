FROM python:3.6
WORKDIR /web_server
COPY . . 
RUN apt update
RUN apt install -y libsasl2-dev python-dev libldap2-dev libssl-dev
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

ENTRYPOINT [ "/bin/sh" ]
CMD ["run.sh"]
