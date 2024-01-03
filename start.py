import os
import requests
import base64
import subprocess
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def read_version():
    version_file = os.path.join(os.path.dirname(__file__), 'VERSION')
    with open(version_file) as f:
        return f.read().strip()

__version__ = read_version()
# __webversion__ = base64.b64decode(requests.get(url= 'https://api.github.com/repos/Unblockabl/test/contents/VERSION').json()['content']).decode('utf-8').strip()
githeaders = {'Authorization': 'token ' + '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'}
__webversion__ = requests.get(url='https://raw.githubusercontent.com/Unblockabl/test/main/VERSION', headers=githeaders).text.strip()

if __version__ != __webversion__:
    print('Version mismatch: %s != %s' % (__version__, __webversion__))
    print('Downloading new version...')

    directory_url = 'https://api.github.com/repos/Unblockabl/test/contents/run'
    local_folder = os.path.join(os.path.dirname(__file__), 'run')

    response = requests.get(url=directory_url, headers=githeaders)
    data = response.json()

    if response.status_code == 200:
        for file in data:
            file_name = os.path.join(local_folder, file['name'])

            if file['type'] == 'file':
                print('Downloading %s...' % file_name)
                download_url = file['download_url']
                r = requests.get(url=download_url, headers=githeaders)

                # Ensure the directory structure exists before writing the file
                os.makedirs(os.path.dirname(file_name), exist_ok=True)

                with open(file_name, 'wb') as f:
                    f.write(r.content)
            else:
                print('Creating %s (directory)...' % file_name)
                # Retrieve content for subdirectories
                subdirectory_url = file['url']
                subdirectory_response = requests.get(url=subdirectory_url, headers=githeaders)
                subdirectory_data = subdirectory_response.json()

                os.makedirs(file_name, exist_ok=True)

                for sub_file in subdirectory_data:
                    if sub_file['type'] == 'file':  # Check if it's a file
                        sub_file_name = os.path.join(file_name, sub_file['name'])
                        print('Downloading %s...' % sub_file_name)
                        sub_download_url = sub_file['download_url']
                        sub_r = requests.get(url=sub_download_url, headers=githeaders)

                        with open(sub_file_name, 'wb') as sub_f:
                            sub_f.write(sub_r.content)
                    elif sub_file['type'] == 'dir':  # It's a directory
                        sub_file_name = os.path.join(file_name, sub_file['name'])
                        print('Creating %s (directory)...' % sub_file_name)
                        # Ensure the directory structure exists before writing the directory path
                        os.makedirs(sub_file_name, exist_ok=True)

    else:
        # Handle the case where the request was not successful
        print(f"Failed to retrieve content from {directory_url}")

    # download VERSION file
    r = requests.get(url= 'https://api.github.com/repos/Unblockabl/test/contents/VERSION', headers=githeaders)
    print('Downloading VERSION...')
    with open('VERSION', 'wb') as f:
        f.write(base64.b64decode(r.json()['content']))
 
    print('\nSetting things up...')
    def setup():
        port = input('\nWhich port would you like to run on? (default: 5000) ')
        if port == '':
            port = '5000'

        try:
            port = int(port)
        except ValueError:
            print('Invalid port.')
            setup()
            return

        config['SERVER']['port'] = port
        with open('config.ini', 'w') as configfile:
            config.write(configfile)

            print('Done. Restarting...')   

            subprocess.Popen('python start.py', shell=True)
            exit(1)

    setup()
   

print('You are running the latest version: %s' % __version__)

input('Press Enter to continue...')
    
print('\nStarting server...')

subprocess.Popen('python run/main.py', shell=True)
exit(1)