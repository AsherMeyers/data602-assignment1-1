FROM python:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache git
RUN pip install bs4
RUN pip install pandas
RUN pip install numpy

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/cspitmit03/CUNYDATA602 /usr/src/app/flask-trader
EXPOSE 5000
CMD [ "python", "/usr/src/app/flask-trader/data602-assignment1.py" ]
