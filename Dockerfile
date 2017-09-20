FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git && \
    pip install --no-cache-dir pandas && \
    pip install bs4 && \
    pip install numpy

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/cspitmit03/CUNYDATA602 /usr/src/app/flask-trader
EXPOSE 5000
CMD [ "python", "/usr/src/app/flask-trader/data602-assignment1.py" ]
