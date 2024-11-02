#!/usr/bin/env python

from logparser.Drain import LogParser

# Répertoire d'entrée et de sortie
input_dir = './Openstack/'  # Répertoire d'entrée du fichier de log
output_dir = './result/'  # Répertoire de sortie pour les résultats du parsing
log_file = 'openstack_normal1.log'  # Nom du fichier de log d'entrée

# Format de log pour correspondre à la structure du log Openstack
log_format = '<LogFile> <Date> <Time> <PID> <Level> <Component> [<Request_ID> <User_ID> <Project_ID> - - -] <IP_Address> "<Method> <URL> <HTTP_Version>" status: <Status> len: <Length> time: <ResponseTime>'

# Liste d'expressions régulières pour le prétraitement
regex = [
    r'((\d{1,3}\.){3}\d{1,3})',  # IP
    r'\[.*?\]',  # Enlève les contenus entre crochets []
    r'\".*?\"'   # Enlève les contenus entre guillemets doubles
]

# Paramètres de configuration pour le parser
st = 0.5  # Seuil de similarité
depth = 4  # Profondeur de tous les nœuds

# Initialisation et exécution du parser
parser = LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
parser.parse(log_file)
