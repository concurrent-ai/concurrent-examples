import mlflow
import os
import infinstor_mlflow_plugin
import boto3
import tempfile
import pandas as pd
import json
import sys
from concurrent_plugin import concurrent_core

print('listfiles: Entered', flush=True)
df = concurrent_core.list(None, input_name='input1')

print('Concurrent Core DataFrame Columns:', flush=True)
cn = df.columns.values.tolist()
print(str(cn))

lp = concurrent_core.get_local_paths(df)
print('Concurrent Core Local paths:')
for one_file in lp:
    print(str(one_file), flush=True)
os._exit(os.EX_OK)
