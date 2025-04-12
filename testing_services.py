import os
import sys
import csv
import ctypes

# === CONFIG: Set your NAS path here ===
csv_path = r"\\NAS\your\folder\services_output.csv"  # Update to your real path

# === Helper: Python 2/3 compatibility ===
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

# === Check if script is run as Administrator ===
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("❌ This script must be run as Administrator.")
    sys.exit(1)

# === Get Services Info ===
output = os.popen('sc queryex type= service state= all').read().splitlines()

services = []
service = {}

for line in output:
    line = line.strip()
    if line.startswith("SERVICE_NAME:"):
        if service:
            services.append(service)
            service = {}
        service['SERVICE_NAME'] = line.split(":", 1)[1].strip()
    elif line.startswith("DISPLAY_NAME:"):
        service['DISPLAY_NAME'] = line.split(":", 1)[1].strip()
    elif line.startswith("STATE"):
        parts = line.split(":", 1)[1].strip().split()
        service['STATE'] = parts[1] if len(parts) > 1 else parts[0]

if service:
    services.append(service)

# === Get START_NAME and START_TYPE ===
for svc in services:
    name = svc['SERVICE_NAME']
    qc_output = os.popen('sc qc "%s"' % name).read()
    svc['START_NAME'] = "Unknown"
    svc['START_TYPE'] = "Unknown"
    for line in qc_output.splitlines():
        if "SERVICE_START_NAME" in line:
            svc['START_NAME'] = line.split(":", 1)[1].strip()
        elif "START_TYPE" in line:
            val = line.split(":", 1)[1].strip().lower()
            if "2" in val:
                svc['START_TYPE'] = "Automatic"
            elif "3" in val:
                svc['START_TYPE'] = "Manual"
            elif "4" in val:
                svc['START_TYPE'] = "Disabled"
            elif "delayed-auto" in val:
                svc['START_TYPE'] = "Automatic (Delayed Start)"

# === Write to CSV on NAS ===
file_exists = os.path.isfile(csv_path)
system_name = os.environ.get('COMPUTERNAME', 'Unknown')

# Open differently based on Python version
if PY2:
    f = open(csv_path, "ab")  # binary mode in Py2
else:
    f = open(csv_path, "a", newline='', encoding='utf-8')  # text mode in Py3

with f:
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow([
            b("SYSTEM_NAME"),
            b("DISPLAY_NAME"),
            b("STATE"),
            b("START_NAME"),
            b("START_TYPE")
        ])
    for svc in services:
        writer.writerow([
            b(system_name),
            b(svc.get('DISPLAY_NAME', '')),
            b(svc.get('STATE', '')),
            b(svc.get('START_NAME', '')),
            b(svc.get('START_TYPE', ''))
        ])
