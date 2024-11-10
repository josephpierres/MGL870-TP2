# MGL870-TP2
1. Take HDFS raw log dataset as an example, I first need to transform it into a structured log dataset using the LogParser. And I will ended up getting this two files _structured.csv and _template.csv
2. And to get the training data and test data that look like the hdfs_train, hdfs_test_normal and hdfs_test_abnormal from the structured log dataset that I got from step 1, I will need to first do the sampling to generate the sequence of number as you stated in the example of how to sample your own log. Then after having the event sequences, I will need to do the train test split mannually to get the three datsasets that listed above.
3. After having the datasets, we can perform the model (e.g. deeplog.py) training on the hdfs_train file that uses the sliding window sampling methods to generate sequence vector, count vector and semantic vector to train the deep learning model. And we can choose our own combination of the feature vectors that we wanna use.
4. Lastly, use the saved model to do inference on the test dataset.

https://github.com/d0ng1ee/logdeep/issues/3

Utilisation de l’apprentissage machine pour la détection des anomalies
## apres avoir installer python, installer l'enviromment virtuel
pip install virtualenv
python3 -m pip install --upgrade pip
python3 -m venv .venv

## pour activer l'environnement de python
source .venv/bin/activate

## installation du log parser
pip install logparser3

## Note that regex matching in Python is brittle, so we recommend fixing the regex library to version 2022.3.2.
## pour ce faire on va faire 
pip freeze > requirements.txt
## pour fixer les exigences et ajouter les exigences suivantes
python 3.6+
regex 2022.3.2
numpy
pandas
scipy
scikit-learn


pip install -r requirements.txt

 error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools": https://visualstudio.microsoft.com/visual-cpp-build-tools/

I've gone through your code, I get your idea as (I am putting minute details so that it could be helpful to someone in future.)

First gather all the logs which was obtained from normal execution of application, i.e., logs without errors.
Combine these logs and convert to _structured.csv and _template.csv file using drain from logpai.
Train the model using obtained _structured.csv from step 2.
After successful training and saved model, it's time to test the model' s accuracy using a abnormal log file (log file with anomaly) and normal log file followed by inference of the model for the new logs files.
To implement step 4, since log files will be different in the sequence of events, so obtaining _structured.csv and _template.csv file using drain will not make any sense as randomly generated event_id will be completely different for an event from generated event_id for same event from the log file used for training. So, you proposed structure_bgl.py, using which I can generate event_id for completely new logs based on the event_id of the logs used for training using the generated event_template. Further, sample_bgl.py will convert the structured log into sequence of event_id which can further be replaced by its equivalent integer and thus testing can be performed.
Further to inference the model, new log line or logs lines in particular time window can be mapped with training file's event_template to obtain event_id.
