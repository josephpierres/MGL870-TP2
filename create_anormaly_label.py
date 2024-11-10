import os
import pandas as pd
import re
# Chemin du fichier des logs structurés
csv_directory = './result'

log_structured_path = os.path.join(csv_directory, 'HDFS.log_structured.csv')

# Lecture du fichier CSV structuré des logs
log_structured = pd.read_csv(log_structured_path)

# Fonction pour extraire le BlockId à partir du contenu ou de la liste des paramètres
def extract_block_id(row):
    # Recherche d'un identifiant de bloc dans la colonne 'ParameterList'
    pattern = r'blk_[^\s,]+'
    match = re.search(pattern, row['Content'])
    if not match:
        match = re.search(pattern, row['ParameterList'])
    return match.group(0) if match else None

# Application de la fonction pour extraire les BlockIds
log_structured['BlockId'] = log_structured.apply(extract_block_id, axis=1)

# Suppression des lignes sans BlockId
log_structured = log_structured.dropna(subset=['BlockId'])

# Identification des labels (Normal ou Anomaly) en fonction du niveau de log
log_structured['Label'] = log_structured['Level'].apply(lambda x: 'Anomaly' if x in ['ERROR', 'FATAL'] else 'Normal')

# Extraction des BlockId et des labels uniques
block_labels = log_structured[['BlockId', 'Label']].drop_duplicates()

# Sauvegarde du résultat dans un fichier CSV
output_path = os.path.join(csv_directory, 'anomaly_label.csv')
block_labels.to_csv(output_path, index=False)

print(f'Fichier "anomaly_label.csv" généré avec succès dans {output_path}')
