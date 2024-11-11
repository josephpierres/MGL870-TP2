import os
import pandas as pd
import re
input_dir = './HDFS_v1/'
event_traces_file = os.path.join(input_dir, "preprocessed/Event_traces.csv")
anomaly_label_file = os.path.join(input_dir, "preprocessed/anomaly_label.csv")
# Charger les fichiers
output_dir = './HDFS_v1/output/'
output_file = os.path.join(output_dir, "Event_occurence_matrix.csv")

# Charger le fichier anomaly_label.csv et mapper les labels
anomaly_labels = pd.read_csv(anomaly_label_file)
anomaly_labels['Label'] = anomaly_labels['Label'].apply(lambda x: 'Fail' if x == 'Anomaly' else 'Success')
label_dict = anomaly_labels.set_index('BlockId')['Label'].to_dict()

# Charger le fichier Event_traces.csv
event_traces = pd.read_csv(event_traces_file)

# Initialiser les colonnes d'événements (E1 à E29)
event_columns = [f"E{i}" for i in range(1, 30)]
occurrence_matrix = []

# Itérer sur chaque ligne pour construire la matrice d'occurrence
for _, row in event_traces.iterrows():
    block_id = row['BlockId']
    label = label_dict.get(block_id, 'Unknown')
    features = row['Features']
    event_list = re.findall(r"E\d+", features)

    # Compter les occurrences des événements
    event_counts = {event: event_list.count(event) for event in event_columns}
    
    # Ajouter le résultat à la matrice
    occurrence_matrix.append({
        "BlockId": block_id,
        "Label": label,
        "Type": row['Type'] if pd.notna(row['Type']) else '',
        **event_counts
    })

# Convertir en DataFrame et sauvegarder
occurrence_matrix_df = pd.DataFrame(occurrence_matrix)
occurrence_matrix_df = occurrence_matrix_df[['BlockId', 'Label', 'Type'] + event_columns]
occurrence_matrix_df.to_csv(output_file, index=False)
print(f"Event occurrence matrix saved to {output_file}")
