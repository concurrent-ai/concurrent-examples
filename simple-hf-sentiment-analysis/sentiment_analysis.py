import mlflow
import os
import infinstor_mlflow_plugin
import boto3
from mlflow.store.artifact.models_artifact_repo import ModelsArtifactRepository
import tempfile
import pandas as pd
import pickle
import json
import sys
from concurrent_plugin import concurrent_core
from transformers import pipeline

print('sentiment_analysis: Entered', flush=True)

print('------------------------------ Begin Loading Huggingface Pipeline ------------------', flush=True)
nlp = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
print('------------------------------ After Loading Huggingface Pipeline ------------------', flush=True)

def do_nlp_fnx(row):
     s = nlp(row['text'])[0]
     return [s['label'], s['score']]

print('------------------------------ Before Inference ------------------', flush=True)
jsonarray = [{'text': 'This is great weather'}, {'text': 'This is bad weather'}]
df1 = pd.DataFrame(jsonarray, columns=['text'])
df1[['label', 'score']] = df1.apply(do_nlp_fnx, axis=1, result_type='expand')
df1.reset_index()
for index, row in df1.iterrows():
    print("'" + row['text'] + "' sentiment=" + row['label'] + ", score=" + str(row['score']))
print('------------------------------ After Inference. End ------------------', flush=True)
os._exit(os.EX_OK)
