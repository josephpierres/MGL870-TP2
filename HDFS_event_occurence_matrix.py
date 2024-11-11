import sys
import os
import re
import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm
from logparser import Spell, Drain

sys.path.append('../')

# Configuration des chemins
input_dir = './HDFS_v1/'
output_dir = './HDFS_v1/output/'
csv_directory = './result'
log_file = "HDFS.log"
log_structured_file = os.path.join(csv_directory, 'HDFS.log_structured_blk.csv')
log_templates_file = os.path.join(csv_directory, 'HDFS.log_templates.csv')
log_sequence_file = os.path.join(input_dir, "preprocessed/Event_traces.csv")
blk_label_file = os.path.join(input_dir, "preprocessed/anomaly_label.csv")
json_template_file = os.path.join(output_dir, "hdfs_log_templates.json")

# def mapping():
#     log_temp = pd.read_csv(log_templates_file).sort_values(by="Occurrences", ascending=False)
#     log_temp_dict = {event: f"E{idx + 1}" for idx, event in enumerate(log_temp["EventId"])}
    
#     # Sauvegarde du dictionnaire de mappage
#     output_path = os.path.join(output_dir, "hdfs_log_templates.json")
#     with open(output_path, "w") as f:
#         json.dump(log_temp_dict, f)
#     print("Mapping completed and saved to", output_path)
#     return log_temp_dict

# def convert_log_structured_file():
#     json_file_path = os.path.join(output_dir, 'hdfs_log_templates.json')  # Chemin vers le fichier JSON contenant le mapping des EventId

#     # Charger le fichier CSV structuré
#     structured_log_path = os.path.join(csv_directory, 'HDFS.log_structured.csv')
#     df_structured = pd.read_csv(structured_log_path)

#     # Charger le fichier JSON contenant le mapping des EventId vers des labels
#     with open(json_file_path, 'r') as json_file:
#         event_mapping = json.load(json_file)

#     # Ajouter la colonne BlockId en extrayant les identifiants des blocs
#     df_structured['BlockId'] = df_structured['Content'].apply(lambda x: re.search(r'blk_(|-)[0-9]+', x).group(0) if re.search(r'blk_(|-)[0-9]+', x) else None)

#     # Supprimer les lignes où BlockId est NaN
#     df_structured = df_structured.dropna(subset=['BlockId'])

#     # Remplacer les EventId par les valeurs correspondantes dans le fichier JSON
#     df_structured['EventId'] = df_structured['EventId'].apply(lambda x: event_mapping.get(x, x))

#     # Réorganiser les colonnes pour que BlockId soit la première
#     columns = ['BlockId'] + [col for col in df_structured.columns if col != 'BlockId']
#     df_structured = df_structured[columns]

#     # Sauvegarder le nouveau fichier structuré
#     structured_log_path_with_blockid = os.path.join(csv_directory, 'HDFS.log_structured_blk.csv')
#     df_structured.to_csv(structured_log_path_with_blockid, index=False)

#     print(f"Le fichier structuré avec BlockId et les EventId remplacés est généré et sauvegardé dans {structured_log_path_with_blockid}")
    
# def load_anomaly_labels(file_path):
#     # Charger le fichier de labels et créer un dictionnaire de mapping BlockId -> Label
#     label_df = pd.read_csv(file_path)
#     label_dict = label_df.set_index('BlockId')['Label'].to_dict()
#     return label_dict


    
# def hdfs_sampling(log_file, json_template, output_file, window='session'):
#     assert window == 'session', "Only window=session is supported for HDFS dataset."
#     print("Loading", log_file)

#     # Lire les logs structurés
#     df = pd.read_csv(log_file, engine='c', na_filter=False, memory_map=True, dtype={'Date': object, 'Time': object})
    
#     # Charger le mapping des EventId depuis le fichier JSON
#     with open(json_template, "r") as f:
#         event_num = json.load(f)
        
#     # Mapper les EventId vers des indices numériques
#     df["EventId"] = df["EventId"].apply(lambda x: event_num.get(x, -1))
    
#     # data_dict, time_dict = defaultdict(list), defaultdict(list)
#     # for _, row in tqdm(df.iterrows(), total=df.shape[0]):
#     #     blkId_set = set(re.findall(r'(blk_-?\d+)', row['Content']))
#     #     for blk_Id in blkId_set:
#     #         data_dict[blk_Id].append(row["EventId"])
#     #         time_dict[blk_Id].append(row["Time"])

#     # rows = []
#     # for block_id, events in data_dict.items():
#     #     # Construire la liste des features
#     #     features = [event_num.get(str(event), event) for event in events if event != -1]
        
#     #     # Prétraiter les valeurs de temps pour s'assurer qu'elles sont au format HHMMSS
#     #     formatted_times = []
#     #     for time_str in time_dict[block_id]:
#     #         if len(time_str) < 6:
#     #             time_str = time_str.zfill(6)  # Ajouter des zéros pour obtenir HHMMSS
#     #         formatted_times.append(time_str)
            
        
#     #     try:
#     #         # Conversion en datetime avec format HHMMSS
#     #         times = pd.to_datetime(formatted_times, format='%H%M%S')
#     #     except ValueError as e:
#     #         print(f"Error parsing times for BlockId {block_id}: {e}")
#     #         continue  # Passer à la prochaine itération en cas d'erreur

#     #     if len(times) > 1:
#     #         time_intervals = [(times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))]
#     #         latency = (times[-1] - times[0]).total_seconds()
#     #     else:
#     #         time_intervals = []
#     #         latency = 0
#     #     # Attribuer le label correct (Success ou Failed)
#     #     label = "Failed" if label_dict.get(block_id, "Normal") == "Anomaly" else "Success"
#     #     rows.append({
#     #         "BlockId": block_id,
#     #         "Label": label,
#     #         "Type": "",
#     #         "Features": str(features),
#     #         "TimeInterval": str(time_intervals),
#     #         "Latency": latency
#     #     })

#     # # Créer un DataFrame à partir des lignes
#     # data_df = pd.DataFrame(rows, columns=['BlockId', 'Label', 'Type', 'Features', 'TimeInterval', 'Latency'])
#     data_dict = defaultdict(list) #preserve insertion order of items
#     for idx, row in tqdm(df.iterrows()):
#         blkId_list = re.findall(r'(blk_-?\d+)', row['Content'])
#         blkId_set = set(blkId_list)
#         for blk_Id in blkId_set:
#             data_dict[blk_Id].append(row["EventId"])

#     data_df = pd.DataFrame(list(data_dict.items()), columns=['BlockId', 'EventSequence'])
#     # Sauvegarder le DataFrame en CSV
#     data_df.to_csv(output_file, index=False)
#     print("HDFS sampling completed. Output saved to", output_file)

def generate_train_test(hdfs_sequence_file, n=None, ratio=0.3):
    blk_df = pd.read_csv(blk_label_file)
    blk_label_dict = {row["BlockId"]: 1 if row["Label"] == "Anomaly" else 0 for _, row in blk_df.iterrows()}
    
    seq = pd.read_csv(hdfs_sequence_file)
    seq["Label"] = seq["BlockId"].apply(lambda x: blk_label_dict.get(x))
    
    normal_seq = seq[seq["Label"] == 0]["Features"].sample(frac=1, random_state=20)
    abnormal_seq = seq[seq["Label"] == 1]["Features"]

    train_len = n or int(len(normal_seq) * ratio)
    print(f"Normal size: {len(normal_seq)}, Abnormal size: {len(abnormal_seq)}, Training size: {train_len}")

    train = normal_seq.iloc[:train_len]
    test_normal = normal_seq.iloc[train_len:]
    test_abnormal = abnormal_seq

    df_to_file(train, os.path.join(output_dir, "train"))
    df_to_file(test_normal, os.path.join(output_dir, "test_normal"))
    df_to_file(test_abnormal, os.path.join(output_dir, "test_abnormal"))
    print("Train-test data generation completed.")

def df_to_file(df, file_name):
    with open(file_name, 'w') as f:
        for row in df:
            f.write(' '.join([str(ele) for ele in eval(row)]) + '\n')

if __name__ == "__main__":
    # event_map = mapping()
    # convert_log_structured_file()
    # label_dict = load_anomaly_labels(blk_label_file)
    # hdfs_sampling(log_structured_file, json_template_file, log_sequence_file) #, event_map)
    generate_train_test(log_sequence_file)
