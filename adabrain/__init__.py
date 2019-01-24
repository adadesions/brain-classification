'''
    AdaBrain
    Initilization
'''
from pathlib import Path

dcm_path = Path('./adabrain/dcm_list.txt')
dcm_list = []

with dcm_path.open() as dcm:
    text = dcm.readlines()
    dcm_list = [p.replace('\n', '') for p in text]