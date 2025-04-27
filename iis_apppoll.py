import subprocess
import os
import socket
import csv
import sys

def get_iis_app_pools():
    try:
        # Set the IIS directory
        iis_directory = r"C:\Windows\System32\inetsrv"
        os.chdir(iis_directory)

        # Get server name
        server_name = socket.gethostname()

        # Define the commands to run
        commands = {
            'name': ['appcmd', 'list', 'apppool', '/text:name'],
            'status': ['appcmd', 'list', 'apppool', '/text:state'],
            'version': ['appcmd', 'list', 'apppool', '/text:RuntimeVersion'],
            'identity': ['appcmd', 'list', 'apppool', '/text:processModel.identityType'],
            'userName': ['appcmd', 'list', 'apppool', '/text:processModel.userName']
        }

        # Run the commands and collect the output
        results = {}
        for key, command in commands.items():
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise Exception("Error running command {}: {}".format(command, stderr.strip()))
            if sys.version_info[0] == 2:
                results[key] = stdout.decode('utf-8', 'ignore').split("\r\n")
            else:
                results[key] = stdout.decode('utf-8', 'ignore').split("\r\n")

        # Output CSV path
        output_csv = r'\\FXQA03-NAS2\geomartqa-fs01\data\GeoMart_Code\job\old\iis_apppools.csv'
        file_exists = os.path.exists(output_csv)

        # Write to CSV
        if sys.version_info[0] == 2:
            f = open(output_csv, "ab")
        else:
            f = open(output_csv, "a", newline='', encoding='utf-8')

        with f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["SERVER_NAME", "APPPOOL_NAME", "STATE", "RUNTIME_VERSION", "IDENTITY_TYPE", "USERNAME"])

            for i, j, k, l, m in zip(results['name'], results['status'], results['version'], results['identity'], results['userName']):
                if i.strip() == "":
                    continue
                username = m if l == "SpecificUser" else ""
                writer.writerow([server_name, i.strip(), j.strip(), k.strip(), l.strip(), username.strip()])

        print("AppPool information successfully saved to CSV!")

    except Exception as e:
        print("An error occurred: {}".format(e))

get_iis_app_pools()
