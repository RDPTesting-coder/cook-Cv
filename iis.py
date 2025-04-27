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

# Path to appcmd
appcmd = r"C:\Windows\System32\inetsrv\appcmd.exe"

def get_apppools():
    cmd = [appcmd, 'list', 'apppool', '/xml']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')
    tree = ET.parse(StringIO(stdout))
    root = tree.getroot()

    apppools = []
    for apppool in root.findall('.//APPPOOL'):
        name = apppool.attrib.get('APPPOOL.NAME', '')
        identityType = apppool.find('processModel').attrib.get('identityType', '')
        userName = apppool.find('processModel').attrib.get('userName', '')
        apppools.append({
            'APPPOOL_NAME': name,
            'IDENTITY_TYPE': identityType,
            'USER_NAME': userName
        })
    return apppools

def get_sites():
    cmd = [appcmd, 'list', 'site', '/xml']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if PY2:
        stdout = stdout.decode('utf-8', 'ignore')
    else:
        stdout = stdout.decode('utf-8', 'ignore')
    tree = ET.parse(StringIO(stdout))
    root = tree.getroot()

    sites = []
    for site in root.findall('.//SITE'):
        name = site.attrib.get('SITE.NAME', '')
        id = site.attrib.get('id', '')
        state = site.attrib.get('state', '')
        bindings = []
        for binding in site.findall('bindings/binding'):
            binding_info = binding.attrib.get('bindingInformation', '')
            protocol = binding.attrib.get('protocol', '')
            bindings.append(protocol + "://" + binding_info)
        sites.append({
            'SITE_NAME': name,
            'SITE_ID': id,
            'STATE': state,
            'BINDINGS': ";".join(bindings)
        })
    return sites

# === Output CSV paths ===
apppool_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_apppools.csv'
site_csv_path = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_sites.csv'

# === Write AppPools ===
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

# === Write Sites ===
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
