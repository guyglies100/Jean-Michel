FROM python:3

COPY . /

RUN pip install scipy discord asyncio requests pickle

CMD [ "python", "./bot.py" ]