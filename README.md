# MGL870-TP2
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
