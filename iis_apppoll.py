import subprocess
import sys
import csv
import os
import re

PY2 = sys.version_info[0] == 2

def b(text):
    if PY2:
        return text.encode('utf-8') if isinstance(text, unicode) else text
    else:
        return text

appcmd = r"C:\Windows\System32\inetsrv\appcmd.exe"

def get_apppools():
    cmd = [appcmd, 'list', 'apppool', '/text:*']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')
    
    apppools = []
    current_pool = {}

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith('APPPOOL.NAME:'):
            # save previous
            if current_pool:
                apppools.append(current_pool)
                current_pool = {}
            current_pool['APPPOOL_NAME'] = line.split(':', 1)[1].strip()
        elif line.startswith('processModel.identityType:'):
            current_pool['IDENTITY_TYPE'] = line.split(':', 1)[1].strip()
        elif line.startswith('processModel.userName:'):
            current_pool['USER_NAME'] = line.split(':', 1)[1].strip()
    
    # append last one
    if current_pool:
        apppools.append(current_pool)
    
    return apppools

# === Output file
apppool_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_apppools.csv'
file_exists = os.path.exists(apppool_csv_path)

apppools = get_apppools()

# === Save to CSV
if PY2:
    f = open(apppool_csv_path, "ab")
else:
    f = open(apppool_csv_path, "a", newline='', encoding='utf-8')

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b('APPPOOL_NAME'), b('IDENTITY_TYPE'), b('USER_NAME')])
    for apppool in apppools:
        writer.writerow([
            b(apppool.get('APPPOOL_NAME', '')),
            b(apppool.get('IDENTITY_TYPE', '')),
            b(apppool.get('USER_NAME', ''))
        ])
