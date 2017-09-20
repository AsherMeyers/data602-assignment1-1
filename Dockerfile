FROM python:3.5

RUN apt-get update -qq && apt-get upgrade -y && \
   apt-get install -y --no-install-recommends \
       libatlas-base-dev gfortran\
        python-pip

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/cspitmit03/CUNYDATA602 /usr/src/app/flask-trader
EXPOSE 5000
CMD [ "python", "/usr/src/app/flask-trader/data602-assignment1.py" ]
