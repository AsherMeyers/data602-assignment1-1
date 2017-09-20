FROM python:alpine

RUN apk add --no-cache --virtual=build_dependencies musl-dev gcc python-dev make cmake g++ gfortran && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip install numpy && \
    pip install pandas==0.18.1 && \
    apk del build_dependencies && \
    apk add --no-cache libstdc++ && \
    rm -rf /var/cache/apk/*

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/cspitmit03/CUNYDATA602 /usr/src/app/flask-trader
EXPOSE 5000
CMD [ "python", "/usr/src/app/flask-trader/data602-assignment1.py" ]
