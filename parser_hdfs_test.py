#!/usr/bin/env python

from logparser.Drain import LogParser


input_dir = './HDFS_v1/'  
output_dir = './result/test' 
log_file = 'test.log' 

log_format = '<Timestamp> <Thread_ID> <Level> <Logger> <Content>'
regex = [
    r'((\d{1,3}\.){3}\d{1,3})',  # IP
    r'blk_-?\d+',  # Identifiant de bloc
    r'src:.*?dest:'  # En-têtes source et destination
]
st = 0.5 
depth = 4  

parser = LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
parser.parse(log_file)
