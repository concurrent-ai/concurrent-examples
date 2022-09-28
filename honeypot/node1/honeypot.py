import mlflow
import os
import infinstor_mlflow_plugin
import boto3
import tempfile
import pandas as pd
import json
import sys
from concurrent_plugin import concurrent_core
import pygeoip

print('honeypot: Entered', flush=True)
df = concurrent_core.list(None, input_name='cowrie')

print('Column Names:', flush=True)
cn = df.columns.values.tolist()
print(str(cn))

lp = concurrent_core.get_local_paths(df)
print('Local paths=' + str(lp))

print('------------------------------ Before Loading GeoIP ------------------', flush=True)
geoip = pygeoip.GeoIP('/tmp/GeoIP.dat')
print('------------------------------ After Loading GeoIP ------------------', flush=True)

print('------------------------------ Before Inference ------------------', flush=True)
totals = {}
for one_local_path in lp:
    print('Begin processing file ' + str(one_local_path), flush=True)
    try:
        with open(one_local_path, 'r') as f:
            jsn = json.load(f)
            print(json.dumps(jsn))
            if 'src_ip' in jsn:
                cc = geoip.country_code_by_addr(jsn['src_ip'])
                print('src_in is in country ' + str(cc))
                if cc in totals:
                    totals[cc] = totals[cc] + 1
                else:
                    totals[cc] = 1
    except Exception as ex:
        print('Caught ' + str(ex) + ' while processing ' + str(one_local_path), flush=True)
print('------------------------------ After Inference. End ------------------', flush=True)

print('totals=' + str(totals), flush=True)
fn = "/tmp/attack_by_country.json"
if os.path.exists(fn):
    os.remove(fn)
with open(fn, 'w') as f:
    f.write(json.dumps(totals))
concurrent_core.concurrent_log_artifact(fn, "")

os._exit(os.EX_OK)
