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
import tracemalloc
import time

tracemalloc_last_time = time.time_ns()
tracemalloc_last = None

def periodic_tracemalloc_dump(pfx):
    global tracemalloc_last
    global tracemalloc_last_time
    if (tracemalloc_last_time + (3 * 1000000000)) < time.time_ns():
        tracemalloc_last_time = time.time_ns()
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print(pfx + ": tracemalloc [ Top 20 ]", flush=True)
        for stat in top_stats[:20]:
            print(stat, flush=True)
        if tracemalloc_last:
            cmps = snapshot.compare_to(tracemalloc_last, 'lineno')
            print(pfx + ": tracemalloc differences [ Top 20 ]", flush=True)
            for stat in cmps[:20]:
                print(stat, flush=True)

print('honeypot: Entered', flush=True)
tracemalloc.start()
periodic_tracemalloc_dump('Program Start')
df = concurrent_core.list(None)
periodic_tracemalloc_dump('After concurrent_core.list')
print('Before Local paths')
lp = concurrent_core.get_local_paths(df)
periodic_tracemalloc_dump('After concurrent_core.get_local_paths')
print('Local paths=' + str(lp))

summation = {}
for one_local_path in lp:
    print('Begin processing file ' + str(one_local_path), flush=True)
    periodic_tracemalloc_dump('Processing file ' + str(one_local_path))
    try:
        with open(one_local_path, 'r') as f:
            jsn = json.load(f)
            print(json.dumps(jsn))
            for key, val in jsn.items():
                if key in summation:
                    summation[key] = summation[key] + val
                else:
                    summation[key] = val
    except Exception as ex:
        print('Caught ' + str(ex) + ' while processing ' + str(one_local_path), flush=True)

periodic_tracemalloc_dump('Done processing files')
print('summation=' + str(summation), flush=True)
fn = "/tmp/attack_by_country_summation.json"
if os.path.exists(fn):
    os.remove(fn)
with open(fn, 'w') as f:
    f.write(json.dumps(summation))
periodic_tracemalloc_dump('Before log artifact')
concurrent_core.concurrent_log_artifact(fn, "")
periodic_tracemalloc_dump('After log artifact. Program Finished')

os._exit(os.EX_OK)
