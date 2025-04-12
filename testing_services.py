import os
import csv
import ctypes
import sys

# ==== Config: Change this path to your NAS location ====
csv_path = r"\\NAS\your\folder\services_output.csv"  # use raw string for UNC paths

# ==== Admin Check ====
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("❌ This script must be run as Administrator.")
    sys.exit(1)

# ==== Get Services (same as before) ====
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
        parts = line.split(":")[1].strip().split()
        service['STATE'] = parts[1] if len(parts) > 1 else parts[0]

if service:
    services.append(service)

# ==== Add START_NAME and START_TYPE ====
for svc in services:
    name = svc['SERVICE_NAME']
    qc_output = os.popen('sc qc "%s"' % name).read()
    svc['START_NAME'] = "Unknown"
    svc['START_TYPE'] = "Unknown"
    for line in qc_output.splitlines():
        if "SERVICE_START_NAME" in line:
            svc['START_NAME'] = line.split(":", 1)[1].strip()
        elif "START_TYPE" in line:
            start_type_code = line.split(":")[1].strip()
            if "2" in start_type_code:
                svc['START_TYPE'] = "Automatic"
            elif "3" in start_type_code:
                svc['START_TYPE'] = "Manual"
            elif "4" in start_type_code:
                svc['START_TYPE'] = "Disabled"
            elif "delayed-auto" in start_type_code.lower():
                svc['START_TYPE'] = "Automatic (Delayed Start)"

# ==== Write to CSV (create if not exist) ====
file_exists = os.path.isfile(csv_path)

# Open in append mode
with open(csv_path, "ab") as f:  # 'ab' for binary append in Python 2
    writer = csv.writer(f)
    if not file_exists:
        writer.writerow(["SYSTEM_NAME", "DISPLAY_NAME", "STATE", "START_NAME", "START_TYPE"])
    system_name = os.environ['COMPUTERNAME']
    for svc in services:
        writer.writerow([
            system_name,
            svc.get('DISPLAY_NAME', ''),
            svc.get('STATE', ''),
            svc.get('START_NAME', ''),
            svc.get('START_TYPE', '')
        ])
