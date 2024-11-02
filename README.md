# MGL870-TP2
Utilisation de l’apprentissage machine pour la détection des anomalies
## apres avoir installer python, installer l'enviromment virtuel
pip install virtualenv
python.exe -m pip install --upgrade pip
python -m venv .venv

## pour activer l'environnement de python
.\.venv\Scripts\activate

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
