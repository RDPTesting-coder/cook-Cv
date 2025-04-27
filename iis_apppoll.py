import subprocess
import sys
import csv
import os

if sys.version_info[0] == 2:
    from StringIO import StringIO
    import xml.etree.ElementTree as ET
else:
    from io import StringIO
    import xml.etree.ElementTree as ET

PY2 = sys.version_info[0] == 2

def b(text):
    if PY2:
        return text.encode('utf-8') if isinstance(text, unicode) else text
    else:
        return text

appcmd = r"C:\Windows\System32\inetsrv\appcmd.exe"

def list_apppool_names():
    cmd = [appcmd, 'list', 'apppool', '/text:name']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')
    apppool_names = stdout.strip().splitlines()
    return apppool_names

def get_apppool_details(name):
    cmd = [appcmd, 'list', 'apppool', name, '/xml']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')

    tree = ET.parse(StringIO(stdout))
    root = tree.getroot()

    pm = root.find('.//processModel')
    if pm is not None:
        identityType = pm.attrib.get('identityType', '')
        userName = pm.attrib.get('userName', '')
    else:
        identityType = ''
        userName = ''
    return identityType, userName

def get_apppools_full():
    apppools = []
    apppool_names = list_apppool_names()
    for name in apppool_names:
        identityType, userName = get_apppool_details(name)
        apppools.append({
            'APPPOOL_NAME': name,
            'IDENTITY_TYPE': identityType,
            'USER_NAME': userName
        })
    return apppools

# === Save to CSV ===
apppool_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_apppools.csv'
file_exists = os.path.exists(apppool_csv_path)

apppools = get_apppools_full()

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
