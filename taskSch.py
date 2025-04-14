import subprocess
import csv
import sys
import os

# Python 3/2 compatibility check
PY2 = sys.version_info[0] == 2

if PY2:
    from StringIO import StringIO
else:
    from io import StringIO

def b(text):
    if PY2:
        return text.encode('utf-8') if isinstance(text, unicode) else text
    else:
        return text

def get_task_scheduler_details():
    process = subprocess.Popen(['schtasks', '/query', '/fo', 'CSV', '/v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if PY2:
        try:
            stdout = stdout.decode('utf-8')
        except UnicodeDecodeError:
            stdout = stdout.decode('latin1')  # fallback
    else:
        stdout = stdout.decode('utf-8')

    reader = csv.reader(StringIO(stdout))
    all_rows = list(reader)
    
    if not all_rows:
        return [], []

    # Get the actual header
    header = all_rows[0]

    # Filter out any duplicate header rows
    tasks = [row for row in all_rows[1:] if row != header]

    return header, tasks

# === File path on NAS ===
file_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\taskSch.csv'

# Check if file exists
file_exists = os.path.exists(file_path)

# Open differently based on Python version
if PY2:
    f = open(file_path, "ab")  # binary mode in Python 2
else:
    f = open(file_path, "a", newline='', encoding='utf-8')  # text mode in Python 3

with f:
    writer = csv.writer(f)
    header, tasks = get_task_scheduler_details()
    
    if not file_exists:
        writer.writerow([b(i) for i in header])
    
    for ta in tasks:
        writer.writerow([b(j) for j in ta])
