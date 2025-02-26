FROM python:3.11.3

WORKDIR /web-chat
COPY requirements.txt chat.py ./
COPY app ./app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD [ "python", "chat.py" ]
