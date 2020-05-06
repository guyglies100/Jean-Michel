FROM python:3

COPY . /

RUN pip install pystrich

CMD [ "python", "./bot.py" ]