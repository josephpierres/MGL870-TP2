#!/usr/bin/env python

from logparser.Drain import LogParser

input_dir = './BGL/'  
output_dir = './result' 
log_file = 'BGL.log' 

log_format = '<Label> <Id> <Date> <Code1> <Time> <Code2> <Component1> <Component2> <Level> <Content>'
regex = [
        r'(0x)[0-9a-fA-F]+', #hexadecimal
        r'\d+.\d+.\d+.\d+',
        # r'/\w+( )$'
        r'\d+'
    ]


st = 0.5  # Similarity threshold
depth = 4  # Depth of all leaf nodes

parser = LogParser(log_format, indir=input_dir, outdir=output_dir, depth=depth, st=st, rex=regex)
parser.parse(log_file)
