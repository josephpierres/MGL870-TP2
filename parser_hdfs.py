#!/usr/bin/env python

from logparser.Drain import LogParser
import re

input_dir = './HDFS_v1/'  
output_dir = './result' 
log_file = 'HDFS.log' 

log_format = '<date> <Time> <Pid> <Level> <Component>: <Content>'
regex      = [
    r'blk_(|-)[0-9]+' , # block id
    r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
    r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]

st = 0.5 
depth = 4  

parser = LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
parser.parse(log_file)
