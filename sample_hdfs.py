import os
import re
import numpy as np
import pandas as pd
from collections import OrderedDict
from tqdm import tqdm

def hdfs_sampling(log_file, window='session', window_size=0):
    assert window == 'session', "Only window=session is supported for HDFS dataset."
    print("Loading", log_file)
    
    # Charger le fichier structuré
    struct_log = pd.read_csv(log_file, engine='c', na_filter=False, memory_map=True)

    # Initialiser les dictionnaires
    data_dict = OrderedDict()
    time_dict = OrderedDict()
    type_count = OrderedDict()

    for idx, row in tqdm(struct_log.iterrows(), total=struct_log.shape[0]):
        blkId_list = re.findall(r'(blk_-?\d+)', row['Content'])
        blkId_set = set(blkId_list)

        for blk_Id in blkId_set:
            if blk_Id not in data_dict:
                data_dict[blk_Id] = []
                time_dict[blk_Id] = []
                type_count[blk_Id] = 0  # Compteur pour "Fail"

            data_dict[blk_Id].append(row['EventId'])
            time_dict[blk_Id].append(str(row['Time']).zfill(6))  # Convertir en chaîne et ajouter des zéros
            # Compter le nombre de fois où le label est "Fail"
            if row['Label'] == 'Fail':
                type_count[blk_Id] += 1

    # Construire le DataFrame final
    rows = []
    for block_id, events in tqdm(data_dict.items(), total=len(data_dict)):
        features = [event for event in events if pd.notnull(event)]
        
        try:
            times = pd.to_datetime(time_dict[block_id], format='%H%M%S', errors='coerce').dropna()
            time_intervals = [(times[i] - times[i - 1]).total_seconds() for i in range(1, len(times))]
            latency = (times[-1] - times[0]).total_seconds() if len(times) > 1 else 0
        except ValueError as e:
            print(f"Error parsing times for BlockId {block_id}: {e}")
            time_intervals = []
            latency = 0

        # Utiliser la première occurrence de `Label` pour chaque `BlockId`
        label = struct_log[struct_log['BlockId'] == block_id]['Label'].iloc[0] if not struct_log[struct_log['BlockId'] == block_id].empty else 'Unknown'

        rows.append({
            "BlockId": block_id,
            "Label": label,
            "Type": type_count[block_id],
            "Features": str(features),
            "TimeInterval": str(time_intervals),
            "Latency": latency
        })

    data_df = pd.DataFrame(rows, columns=['BlockId', 'Label', 'Type', 'Features', 'TimeInterval', 'Latency'])
    output_path = "result/HDFS_sequence.csv"
    data_df.to_csv(output_path, index=None)
    print(f"HDFS sampling completed. Output saved to {output_path}")

# Appeler la fonction avec le fichier approprié
hdfs_sampling('result/HDFS.log_structured_blk.csv')
