FROM python:3

COPY . /

RUN apt-get update

RUN apt-get -y install libopus-dev

RUN pip install scipy discord asyncio requests

CMD [ "python", "./bot.py" ]