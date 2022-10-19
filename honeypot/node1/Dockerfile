ARG CACHEBUST=1
FROM python:3.7

RUN apt install -y curl
RUN pip install mlflow>=1.0 \
    && pip install azure-storage-blob==12.3.0 \
    && pip install numpy==1.21.2 \
    && pip install scipy \
    && pip install pandas==1.3.3 \
    && pip install scikit-learn==0.24.2 \
    && pip install cloudpickle \
    && pip install concurrent_plugin \
    && pip install pygeoip

RUN curl -L -o /tmp/GeoIP.dat.gz https://concurrent-sample-data.s3.amazonaws.com/geoip/GeoIP.dat.gz
RUN gunzip /tmp/GeoIP.dat.gz
