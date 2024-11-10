import os
import re

import pandas as pd


csv_directory = './result'


structured_log_path = os.path.join(csv_directory, 'HDFS.log_structured.csv')

df_structured = pd.read_csv(structured_log_path)

df_structured['BlockId'] = df_structured['Content'].apply(lambda x: re.search(r'blk_(|-)[0-9]+', x).group(0) if re.search(r'blk_(|-)[0-9]+', x) else None)
df_structured = df_structured.dropna(subset=['BlockId'])
columns = ['BlockId'] + [col for col in df_structured.columns if col != 'BlockId']
df_structured = df_structured[columns]
structured_log_path_with_blockid = os.path.join(csv_directory, 'HDFS.log_structured_blk.csv')
df_structured.to_csv(structured_log_path_with_blockid, index=False)
print(f"Le fichier structuré avec BlockId est généré et sauvegardé dans {structured_log_path_with_blockid}")