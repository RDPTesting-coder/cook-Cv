import subprocess
import os
import socket
import csv
import sys

def get_iis_applications():
    try:
        iis_directory = r"C:\Windows\System32\inetsrv"
        os.chdir(iis_directory)

        server_name = socket.gethostname()

        cmd = ['appcmd', 'list', 'app', '/text:*']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode != 0:
            raise Exception("Error running appcmd list app: {}".format(stderr.strip()))
        
        if sys.version_info[0] == 2:
            stdout = stdout.decode('utf-8', 'ignore')
        else:
            stdout = stdout.decode('utf-8', 'ignore')

        apps = []
        current_app = {}

        for line in stdout.splitlines():
            line = line.strip()
            if not line:
                continue

            if line.startswith('APP.NAME:'):
                if current_app:
                    apps.append(current_app)
                    current_app = {}
                current_app['APP_NAME'] = line.split(':', 1)[1].strip()
            elif line.startswith('APPPOOL.NAME:'):
                current_app['APPPOOL_NAME'] = line.split(':', 1)[1].strip()
            elif line.startswith('physicalPath:'):
                current_app['PHYSICAL_PATH'] = line.split(':', 1)[1].strip()
        
        if current_app:
            apps.append(current_app)

        # Output path
        output_csv = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_applications.csv'
        file_exists = os.path.exists(output_csv)

        if sys.version_info[0] == 2:
            f = open(output_csv, "ab")
        else:
            f = open(output_csv, "a", newline='', encoding='utf-8')

        with f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["SERVER_NAME", "SITE_NAME", "APP_PATH", "PHYSICAL_PATH", "APPPOOL_NAME"])

            for app in apps:
                full_name = app.get('APP_NAME', '')   # eg: Default Web Site/VirtualDirectory
                if '/' in full_name:
                    site_name, app_path = full_name.split('/', 1)
                    app_path = '/' + app_path
                else:
                    site_name = full_name
                    app_path = '/'
                
                writer.writerow([
                    server_name,
                    site_name,
                    app_path,
                    app.get('PHYSICAL_PATH', ''),
                    app.get('APPPOOL_NAME', '')
                ])

        print("IIS Application information successfully saved to CSV!")

    except Exception as e:
        print("An error occurred: {}".format(e))

get_iis_applications()
