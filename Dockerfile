FROM python:3.10

ENV BOT_GATEWAY_TOKEN= AZURE_STORAGE_CONNECTION_STRING=

WORKDIR /workdir
COPY requirements.txt /workdir/requirements.txt
RUN pip install -r requirements.txt
COPY bot /workdir/bot
COPY script /workdir/script
COPY setup.py /workdir/

RUN pip install -e .

CMD "script/start.sh"