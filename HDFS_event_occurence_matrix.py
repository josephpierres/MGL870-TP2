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

log_sequence_file = os.path.join(input_dir, "preprocessed/Event_traces.csv")
blk_label_file = os.path.join(input_dir, "preprocessed/anomaly_label.csv")


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
