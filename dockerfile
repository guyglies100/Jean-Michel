FROM python:3

COPY . /

RUN pip install scipy
RUN pip install discord
RUN pip install asyncio
RUN pip install requests
RUN pip install pickle

CMD [ "python", "./bot.py" ]