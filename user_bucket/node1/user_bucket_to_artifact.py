from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client
    from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef
else:
    S3Client = object
    ListObjectsV2OutputTypeDef = object
        
import boto3
from infinstor import infin_boto3
import argparse
import os
import tempfile
import mlflow

from concurrent_plugin import concurrent_core

argparser:argparse.ArgumentParser = argparse.ArgumentParser()
argparser.add_argument("--bucket", required=True, help="User bucket defined in infinstor-platform. Can be accessed without aws credentials when running in the platform")
argparser.add_argument("--prefix", required=True, help="end the prefix with a trailing '/' to list the contents of the prefix (directory)")

args:argparse.Namespace = argparser.parse_args()

bucket:str = args.bucket
prefix:str = args.prefix if args.prefix.endswith('/') else args.prefix + '/'

#mlflow.start_run()
s3:S3Client = boto3.client('s3')

continuation_token = None
while True:
    if continuation_token:
        print('Calling list_objects with continuation_token ' + str(continuation_token), flush=True)
        lrv = s3.list_objects_v2(Bucket=bucket, Prefix=prefix,\
                Delimiter='/', MaxKeys=2, ContinuationToken=continuation_token)
    else:
        print('Calling list_objects with no continuation_token', flush=True)
        lrv = s3.list_objects_v2(Bucket=bucket, Prefix=prefix,\
                Delimiter='/', MaxKeys=2)
    # LIST RV= 
    #{
        #'@xmlns': 'http://s3.amazonaws.com/doc/2006-03-01/',
        #'Name': 'hpe-non-infinsnap-bucket',
        #'Prefix': 'bird_species/model/',
        #'KeyCount': '2',
        #'MaxKeys': '1000',
        #'Delimiter': '/',
        #'EncodingType': 'url',
        #'IsTruncated': 'false',
        #'Contents': [{
                #'Key': 'bird_species/model/EfficientNetB4-BIRDS-0.99.h5',
                #'LastModified': '2022-11-15T15:13:00.000Z',
                #'ETag': '"19a6ca4d0153b453c6539378fa8748d3-28"',
                #'Size': '226883768',
                #'StorageClass': 'STANDARD'
            #}, {
                #'Key': 'bird_species/model/class_dict.csv',
                #'LastModified': '2022-11-15T15:13:00.000Z',
                #'ETag': '"4f607190e8156d46f8109b9d44e5595f"',
                #'Size': '12870',
                #'StorageClass': 'STANDARD'
            #}
        #]
    #}
    #{
        #'@xmlns': 'http://s3.amazonaws.com/doc/2006-03-01/',
        #'Name': 'hpe-non-infinsnap-bucket',
        #'Prefix': 'bird_species/',
        #'KeyCount': '2',
        #'MaxKeys': '1000',
        #'Delimiter': '/',
        #'EncodingType': 'url',
        #'IsTruncated': 'false',
        #'CommonPrefixes': [{
                #'Prefix': 'bird_species/data/'
            #}, {
                #'Prefix': 'bird_species/model/'
            #}
        #]
    #}    
    print('LIST RV=' + str(lrv))
    
    for obj in lrv['Contents']:
        obj_key:str = obj['Key']

        # download the object
        local_fname:str = tempfile.gettempdir() + "/" + obj_key.replace('/', '__')
        print(f"Downloading s3://{bucket}/{obj_key} to {local_fname}")
        s3.download_file(bucket, obj_key, local_fname)
        
        # copy the local file as an mlflow artificat
        print(f"uploading {local_fname} as an artifact")
        concurrent_core.concurrent_log_artifact(local_fname, "output", obj_key=local_fname)
        
        # delete the file
        os.unlink(local_fname)
        
    if 'NextContinuationToken' in lrv:
        continuation_token = lrv['NextContinuationToken']
    else:
        break
