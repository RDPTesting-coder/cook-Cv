def get_iis_app_pools():
    try:
        # Set the IIS directory
        iis_directory = r"C:\Windows\System32\inetsrv"
        os.chdir(iis_directory)

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
            results[key] = stdout.split("\r\n")

        # Print the results
        for i, j, k, l, m in zip(results['name'], results['status'], results['version'], results['identity'], results['userName']):
            print(i, j, k, l, m if l == "SpecificUser" else "")

    except Exception as e:
        print("An error occurred: {}".format(e))
get_iis_app_pools()
