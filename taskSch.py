import subprocess
#import pandas as pd
import csv
import sys
from io import StringIO
import os

# Python 3/2 compatibility check
PY2 = sys.version_info[0] == 2

def u(text):
    if PY2:
        return text.decode('utf-8') if isinstance(text, str) else text
    else:
        return text

def b(text):
    if PY2:
        return text.encode('utf-8') if isinstance(text, unicode) else text
    else:
        return text



def get_task_scheduler_details():
    process = subprocess.Popen(['schtasks', '/query', '/fo', 'CSV', '/v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    stdout = stdout.decode('utf-8')
    
    reader = csv.reader(StringIO(stdout))
    
    header = next(reader)
    tasks = list(reader)
    # print(type(header), type(tasks))
    # print(header, tasks)
    
    return header, tasks

header, tasks = get_task_scheduler_details()
file_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\taskSch.csv'

# Ensure the directory exists
##directory = os.path.dirname(file_path)
##if not os.path.exists(directory):
##    os.makedirs(directory)

# Check if the file already exists
file_exists = os.path.exists(file_path)



# Open differently based on Python version
if PY2:
    f = open(file_path, "ab")  # binary mode in Py2
else:
    f = open(file_path, "a", newline='', encoding='utf-8')  # text mode in Py3

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b(i) for i in header])
    
    for ta in tasks:
        writer.writerow([b(j) for j in ta]) 
