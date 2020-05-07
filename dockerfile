FROM python:3

COPY . /

RUN pip install scipy discord asyncio requests

CMD [ "python", "./bot.py" ]