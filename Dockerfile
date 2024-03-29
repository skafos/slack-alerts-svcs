FROM skafos/ais-base:0.2.5
EXPOSE 32000

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install -r /usr/src/app/requirements.txt

CMD [ "./run.sh" ]