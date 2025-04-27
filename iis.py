import os
import sys
import csv
import subprocess

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

# === Function to fetch Application Pools ===
def get_app_pools():
    pools = []
    cmd = 'cscript //Nologo %windir%\\system32\\inetsrv\\appcmd.vbs list apppool /text:name,processModel.identityType,processModel.userName'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    
    if PY2:
        try:
            stdout = stdout.decode('utf-8')
        except:
            stdout = stdout.decode('latin1')
    else:
        stdout = stdout.decode('utf-8')

    lines = stdout.strip().splitlines()
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 3:
            pools.append({
                'AppPoolName': parts[0],
                'IdentityType': parts[1],
                'UserName': parts[2]
            })
    return pools

# === Function to fetch Sites ===
def get_sites():
    sites = []
    cmd = 'cscript //Nologo %windir%\\system32\\inetsrv\\appcmd.vbs list site /text:name,id,state,bindings,applications'
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    
    if PY2:
        try:
            stdout = stdout.decode('utf-8')
        except:
            stdout = stdout.decode('latin1')
    else:
        stdout = stdout.decode('utf-8')

    lines = stdout.strip().splitlines()
    for line in lines:
        parts = [p.strip() for p in line.split(',')]
        if len(parts) >= 5:
            sites.append({
                'SiteName': parts[0],
                'SiteID': parts[1],
                'State': parts[2],
                'Bindings': parts[3],
                'Applications': parts[4]
            })
    return sites

# === Main execution ===
app_pools = get_app_pools()
sites = get_sites()

# === Write output to CSV ===
file_path_pools = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_app_pools.csv'
file_path_sites = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_sites.csv'

# Write App Pools
file_exists = os.path.exists(file_path_pools)
if PY2:
    f = open(file_path_pools, "ab")
else:
    f = open(file_path_pools, "a", newline='', encoding='utf-8')

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b("AppPoolName"), b("IdentityType"), b("UserName")])
    for app in app_pools:
        writer.writerow([b(app['AppPoolName']), b(app['IdentityType']), b(app['UserName'])])

# Write Sites
file_exists = os.path.exists(file_path_sites)
if PY2:
    f = open(file_path_sites, "ab")
else:
    f = open(file_path_sites, "a", newline='', encoding='utf-8')

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([b("SiteName"), b("SiteID"), b("State"), b("Bindings"), b("Applications")])
    for site in sites:
        writer.writerow([
            b(site['SiteName']),
            b(site['SiteID']),
            b(site['State']),
            b(site['Bindings']),
            b(site['Applications'])
        ])
