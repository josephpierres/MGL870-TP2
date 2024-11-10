import os
import pandas as pd

# Chemin du répertoire contenant les fichiers CSV
csv_directory = './result'

# Chargement des fichiers CSV
log_structured_path = os.path.join(csv_directory, 'train.log_structured.csv')
log_templates_path = os.path.join(csv_directory, 'train.log_templates.csv')

# Lecture des fichiers CSV
log_structured = pd.read_csv(log_structured_path)
log_templates = pd.read_csv(log_templates_path)

# Création d'une liste de tous les identifiants d'événements uniques
event_ids = log_templates['EventId'].unique()
event_ids_sorted = sorted(event_ids)

# Initialisation de la matrice des occurrences
occurrence_matrix = pd.DataFrame(0, index=log_structured['LineId'].unique(), columns=event_ids_sorted)

# Remplissage de la matrice avec le nombre d'occurrences de chaque EventId par LineId
for _, row in log_structured.iterrows():
    block_id = row['LineId']
    event_id = row['EventId']
    if event_id in event_ids_sorted:
        occurrence_matrix.at[block_id, event_id] += 1

# Ajout de la colonne 'Label' à la matrice
# occurrence_matrix.insert(0, 'Label', log_structured.groupby('LineId')['Label'].first())
# Affichage de la matrice pour vérification
print(occurrence_matrix.head())

# Affichage et sauvegarde de la matrice des occurrences
output_path = os.path.join(csv_directory, 'train.occurrence_matrix.csv')
occurrence_matrix.to_csv(output_path, index=True)

print(f'Matrice des occurrences générée et sauvegardée dans {output_path}')


