import pandas as pd
from concurrent_plugin import concurrent_core

df:pd.DataFrame = concurrent_core.list(None, input_name='input1')
# md['FileName'] = one_content['Key']
# md['FileSize'] = one_content['Size']
# md['FileLastModified'] = one_content['LastModified']
# if 'versionId' in one_content:
#     md['FileVersionId'] = one_content['versionId']
print('Concurrent Core DataFrame:', flush=True)
print(df.to_string())
#col_names = df.columns.values.tolist()
#print(str(col_names))

local_paths = concurrent_core.get_local_paths(df)
print('Concurrent Core Local paths: num files=' + str(len(local_paths)))
for one_file in local_paths:
    concurrent_core.concurrent_log_artifact(one_file, "output", one_file=one_file)
