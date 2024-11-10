import os
import pandas as pd

# Chemin du répertoire contenant les fichiers CSV
csv_directory = './result'

# Chargement des fichiers CSV
log_structured_path = os.path.join(csv_directory, 'HDFS.log_structured.csv')
log_templates_path = os.path.join(csv_directory, 'HDFS.logs_templates.csv')

# Lecture des fichiers CSV
log_structured = pd.read_csv(log_structured_path)
log_templates = pd.read_csv(log_templates_path)

# Création d'une liste de tous les identifiants d'événements uniques (EventId)
event_ids = log_templates['EventId'].unique()
event_ids_sorted = sorted(event_ids)

# Initialisation de la matrice des occurrences
occurrence_matrix = pd.DataFrame(0, index=log_structured['BlockId'].unique(), columns=event_ids_sorted)

# Ajout des colonnes 'Label' et 'Type' initialisées à vide
occurrence_matrix.insert(0, 'Type', '')
occurrence_matrix.insert(0, 'Label', '')

# Remplissage de la matrice avec le nombre d'occurrences de chaque EventId par BlockId
for _, row in log_structured.iterrows():
    block_id = row['BlockId']
    event_id = row['EventId']
    label = row['Label'] if 'Label' in row else ''
    event_type = row['Type'] if 'Type' in row else ''  # Utilisation de 'Type' si disponible

    # Ajout de la valeur de label et de type
    occurrence_matrix.at[block_id, 'Label'] = label
    occurrence_matrix.at[block_id, 'Type'] = event_type

    # Incrémentation de l'événement si présent dans les EventId
    if event_id in event_ids_sorted:
        occurrence_matrix.at[block_id, event_id] += 1

# Affichage de la matrice pour vérification
print(occurrence_matrix.head())

# Sauvegarde de la matrice des occurrences
output_path = os.path.join(csv_directory, 'HDFS.occurrence_matrix.csv')
occurrence_matrix.to_csv(output_path, index=True)

print(f'Matrice des occurrences générée et sauvegardée dans {output_path}')
