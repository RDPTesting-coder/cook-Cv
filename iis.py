import subprocess
import csv
import sys
import os

# Python 3/2 compatibility
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

# Path to appcmd
appcmd_path = r"C:\Windows\System32\inetsrv\appcmd.exe"

def get_apppools():
    cmd = [appcmd_path, 'list', 'apppool', '/text:name,processModel.identityType,processModel.userName']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')

    apppools = []
    for line in stdout.strip().splitlines():
        parts = line.strip().split(',')
        if len(parts) >= 3:
            apppools.append({
                'APPPOOL_NAME': parts[0].strip(),
                'IDENTITY_TYPE': parts[1].strip(),
                'USER_NAME': parts[2].strip()
            })
    return apppools

def get_sites():
    cmd = [appcmd_path, 'list', 'site', '/text:name,id,state,bindings']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')

    sites = []
    for line in stdout.strip().splitlines():
        parts = line.strip().split(',')
        if len(parts) >= 4:
            sites.append({
                'SITE_NAME': parts[0].strip(),
                'SITE_ID': parts[1].strip(),
                'STATE': parts[2].strip(),
                'BINDINGS': parts[3].strip()
            })
    return sites

# === Output Files ===
apppool_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_apppools.csv'
site_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_sites.csv'

# === Write AppPools CSV ===
apppools = get_apppools()
file_exists = os.path.exists(apppool_csv_path)

if PY2:
    f = open(apppool_csv_path, "ab")
else:
    f = open(apppool_csv_path, "a", newline='', encoding='utf-8')

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b('APPPOOL_NAME'), b('IDENTITY_TYPE'), b('USER_NAME')])
    for apppool in apppools:
        writer.writerow([b(apppool['APPPOOL_NAME']), b(apppool['IDENTITY_TYPE']), b(apppool['USER_NAME'])])

# === Write Sites CSV ===
sites = get_sites()
file_exists = os.path.exists(site_csv_path)

if PY2:
    f = open(site_csv_path, "ab")
else:
    f = open(site_csv_path, "a", newline='', encoding='utf-8')

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b('SITE_NAME'), b('SITE_ID'), b('STATE'), b('BINDINGS')])
    for site in sites:
        writer.writerow([b(site['SITE_NAME']), b(site['SITE_ID']), b(site['STATE']), b(site['BINDINGS'])])
