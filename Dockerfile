FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/cspitmit03/CUNYDATA602/tree/master/data602-assignment1 /usr/src/app/flask-trader
EXPOSE 5000
CMD [ "python", "/usr/src/app/flask-trader/data602-assignment1.py" ]
