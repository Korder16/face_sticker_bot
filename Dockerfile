FROM python:3.12-slim

WORKDIR /usr/src/bot

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-opencv \
    libgl1

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["python3", "-u", "bot.py"]
