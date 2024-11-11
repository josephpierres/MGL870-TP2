import os
import re
import json
import pandas as pd
input_dir = './HDFS_v1/'
output_dir = './HDFS_v1/output/'
csv_directory = './result'
json_file_path = os.path.join(output_dir, 'hdfs_log_templates.json')  # Chemin vers le fichier JSON contenant le mapping des EventId
anomaly_label_path = os.path.join(input_dir, "preprocessed/anomaly_label.csv")
# Charger le fichier CSV structuré
structured_log_path = os.path.join(csv_directory, 'HDFS.log_structured.csv')
df_structured = pd.read_csv(structured_log_path)

# Charger le fichier JSON contenant le mapping des EventId vers des labels
with open(json_file_path, 'r') as json_file:
    event_mapping = json.load(json_file)

# Charger le fichier anomaly_label.csv
df_labels = pd.read_csv(anomaly_label_path)
df_labels['Label'] = df_labels['Label'].replace({'Normal': 'Success', 'Anomaly': 'Fail'})

# Ajouter la colonne BlockId en extrayant les identifiants des blocs
df_structured['BlockId'] = df_structured['Content'].apply(lambda x: re.search(r'blk_(|-)[0-9]+', x).group(0) if re.search(r'blk_(|-)[0-9]+', x) else None)

# Supprimer les lignes où BlockId est NaN
df_structured = df_structured.dropna(subset=['BlockId'])

# Remplacer les EventId par les valeurs correspondantes dans le fichier JSON
df_structured['EventId'] = df_structured['EventId'].apply(lambda x: event_mapping.get(x, x))

# Fusionner les DataFrames pour ajouter la colonne Label
df_structured = pd.merge(df_structured, df_labels, on='BlockId', how='left')

# Réorganiser les colonnes pour que BlockId et Label soient les premières
columns = ['BlockId', 'Label'] + [col for col in df_structured.columns if col not in ['BlockId', 'Label']]
df_structured = df_structured[columns]

# Sauvegarder le nouveau fichier structuré
structured_log_path_with_blockid = os.path.join(csv_directory, 'HDFS.log_structured_blk.csv')
df_structured.to_csv(structured_log_path_with_blockid, index=False)

print(f"Le fichier structuré avec BlockId et les EventId remplacés est généré et sauvegardé dans {structured_log_path_with_blockid}")
