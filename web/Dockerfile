FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update
RUN apt-get upgrade
# RUN apt install python3-pip

RUN pip install --no-cache-dir -r requirements.txt 
COPY . .
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]