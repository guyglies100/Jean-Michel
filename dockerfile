FROM mcr.microsoft.com/windows/servercore:ltsc2019

COPY . /

RUN pip install scipy discord asyncio requests pickle

CMD [ "python", "./bot.py" ]