FROM tensorflow/tensorflow
 
RUN pip install tensorflow && pip install boto3 && pip install mlflow && pip install tensorflow_datasets && pip install pandas && pip install numpy

ARG IGNORECACHE=12
RUN echo "$IGNORECACHE"
RUN pip install --no-cache-dir concurrent-plugin && pip install --no-cache-dir http://cvat.infinstor.com:9876/packages/infinstor/infinstor-2.0.51-py3-none-any.whl
