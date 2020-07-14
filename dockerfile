FROM python:3

COPY . /

RUN apt-get update

RUN apt-get -y install ffmpeg
RUN apt-get -y install libopus-dev
RUN apt-get -y install libopus0
RUN apt-get -y install opus-tools

RUN pip install -U discord.py[voice]
RUN pip install scipy asyncio requests azure-cognitiveservices-speech

CMD [ "python", "./bot.py" ]