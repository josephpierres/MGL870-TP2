import os
import gc
import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm


tqdm.pandas()
pd.options.mode.chained_assignment = None

# Chemin du répertoire contenant les fichiers CSV
csv_directory = './result'
output_dir = "./BGL/output/"
# data_dir = os.path.expanduser("~/.dataset/bgl")
data_dir = './BGL/'  
log_file = "BGL.log"

# Chargement des fichiers CSV
log_structured_path = os.path.join(csv_directory, 'BGL.log_structured.csv')
log_templates_path = os.path.join(csv_directory, 'BGL.log_templates.csv')


def sliding_window(raw_data, para):
    """
    split logs into sliding windows/session
    :param raw_data: dataframe columns=[timestamp, label, eventid, time duration]
    :param para:{window_size: seconds, step_size: seconds}
    :return: dataframe columns=[eventids, time durations, label]
    """
    log_size = raw_data.shape[0]
    label_data, time_data = raw_data.iloc[:, 1], raw_data.iloc[:, 0]
    logkey_data, deltaT_data = raw_data.iloc[:, 2], raw_data.iloc[:, 3]
    new_data = []
    start_end_index_pair = set()

    start_time = time_data[0]
    end_time = start_time + para["window_size"]
    start_index = 0
    end_index = 0

    # get the first start, end index, end time
    for cur_time in time_data:
        if cur_time < end_time:
            end_index += 1
        else:
            break

    start_end_index_pair.add(tuple([start_index, end_index]))

    # move the start and end index until next sliding window
    num_session = 1
    while end_index < log_size:
        start_time = start_time + para['step_size']
        end_time = start_time + para["window_size"]
        for i in range(start_index, log_size):
            if time_data[i] < start_time:
                i += 1
            else:
                break
        for j in range(end_index, log_size):
            if time_data[j] < end_time:
                j += 1
            else:
                break
        start_index = i
        end_index = j

        # when start_index == end_index, there is no value in the window
        if start_index != end_index:
            start_end_index_pair.add(tuple([start_index, end_index]))

        num_session += 1
        if num_session % 1000 == 0:
            print("process {} time window".format(num_session), end='\r')

    for (start_index, end_index) in start_end_index_pair:
        dt = deltaT_data[start_index: end_index].values
        dt[0] = 0
        new_data.append([
            time_data[start_index: end_index].values,
            max(label_data[start_index:end_index]),
            logkey_data[start_index: end_index].values,
            dt
        ])

    assert len(start_end_index_pair) == len(new_data)
    print('there are %d instances (sliding windows) in this dataset\n' % len(start_end_index_pair))
    return pd.DataFrame(new_data, columns=raw_data.columns)

def deeplog_file_generator(filename, df, features):
    with open(filename, 'w') as f:
        for _, row in df.iterrows():
            for val in zip(*row[features]):
                f.write(','.join([str(v) for v in val]) + ' ')
            f.write('\n')

# In the first column of the log, "-" indicates non-alert messages while others are alert messages.
def count_anomaly():
    total_size = 0
    normal_size = 0
    with open(data_dir + log_file, encoding="utf8") as f:
        for line in f:
            total_size += 1
            if line.split(' ',1)[0] == '-':
                normal_size += 1
    print("total size {}, abnormal size {}".format(total_size, total_size - normal_size))



if __name__ == "__main__":

    # Lecture des fichiers CSV
    log_structured = pd.read_csv(log_structured_path)
    log_templates = pd.read_csv(log_templates_path)

    #########
    # Count #
    #########
    count_anomaly()

    ##################
    # Transformation #
    ##################
    # mins
    window_size = 5
    step_size = 1
    train_ratio = 0.4


    # data preprocess
    log_structured['datetime'] = pd.to_datetime(log_structured['Time'], format='%Y-%m-%d-%H.%M.%S.%f')
    log_structured["Label"] = log_structured["Label"].apply(lambda x: int(x != "-"))
    log_structured['timestamp'] = log_structured["datetime"].values.astype(np.int64) // 10 ** 9
    log_structured['deltaT'] = log_structured['datetime'].diff() / np.timedelta64(1, 's')
    log_structured['deltaT'].fillna(0)

    # sampling with sliding window
    deeplog_df = sliding_window(log_structured[["timestamp", "Label", "EventId", "deltaT"]],
                                para={"window_size": int(window_size)*60, "step_size": int(step_size) * 60}
                                )

    #########
    # Train #
    #########
    df_normal =deeplog_df[deeplog_df["Label"] == 0]
    df_normal = df_normal.sample(frac=1, random_state=12).reset_index(drop=True) #shuffle
    normal_len = len(df_normal)
    train_len = int(normal_len * train_ratio)

    train = df_normal[:train_len]
    # deeplog_file_generator(os.path.join(output_dir,'train'), train, ["EventId", "deltaT"])
    deeplog_file_generator(os.path.join(output_dir,'train'), train, ["EventId"])

    print("training size {}".format(train_len))

    ###############
    # Test Normal #
    ###############
    test_normal = df_normal[train_len:]
    deeplog_file_generator(os.path.join(output_dir, 'test_normal'), test_normal, ["EventId"])
    print("test normal size {}".format(normal_len - train_len))

    del df_normal
    del train
    del test_normal
    gc.collect()

    #################
    # Test Abnormal #
    #################
    df_abnormal = deeplog_df[deeplog_df["Label"] == 1]
    #df_abnormal["EventId"] = df_abnormal["EventId"].progress_apply(lambda e: event_index_map[e] if event_index_map.get(e) else UNK)
    deeplog_file_generator(os.path.join(output_dir,'test_abnormal'), df_abnormal, ["EventId"])
    print('test abnormal size {}'.format(len(df_abnormal)))