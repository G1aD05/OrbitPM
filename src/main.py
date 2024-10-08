import requests
import sys
import os
import shutil
import datetime


class Main:
    def __init__(self):
        self.argv = sys.argv
        self.command()

    def command(self):
        if self.argv[1] == 'install':
            url = f'https://raw.githubusercontent.com/G1aD05/OrbitPM/refs/heads/main/pkg/{self.argv[2]}/main.py'
            requirements = requests.get(f'https://raw.githubusercontent.com/G1aD05/OrbitPM/refs/heads/main/pkg/{self.argv[2]}/requirements.txt')
            response = requests.get(url)
            if os.path.isdir(self.argv[2]):
                print('Package already installed!')
                exit()
            else:
                print(f'Collecting {self.argv[2]}...')
                print('Creating package directory...')
                os.mkdir(self.argv[2])
                os.chdir(self.argv[2])
                print('Writing to files...')
                with open('main.py', 'wb') as file:
                    file.write(response.content)
                with open('.opmpack', 'w') as file:
                    file.write(f'{self.argv[2]}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{requirements.text.replace('\n', ', ')}')
                    file.close()
                if requirements.text == '':
                    print("No requirements found!")
                else:
                    list_requirements = []
                    for i in requirements.text.split('\n'):
                        list_requirements.append(i)
                    list_requirements.pop(-1)
                    print(list_requirements)
                    self.install_requirements(list_requirements)

                print(f'Successfully installed {self.argv[2]}')

        if self.argv[1] == 'uninstall':
            os.chdir(self.argv[2])
            contents = os.listdir()
            if '.opmpack' in contents:
                os.chdir('..')
                shutil.rmtree(self.argv[2])
            else:
                print('Not an OrbitPM Package!')

        if self.argv[1] == 'info':
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            os.chdir(self.argv[2])
            contents = os.listdir()
            lines = []
            if '.opmpack' in contents:
                for i in open('.opmpack', 'r').read().split('\n'):
                    lines.append(i)
                print(f'Name: {lines[0]}')
                print(f'Date installed: {lines[1]}')
                print(f'Requirements: {lines[2]}')
            else:
                print('Not an OrbitPM Package!')

    def install_requirements(self, requirements: list):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        for i in requirements:
            if i in os.listdir():
                print('Package already installed!')
            else:
                response = requests.get(f'https://raw.githubusercontent.com/G1aD05/OrbitPM/refs/heads/main/pkg/{i}/main.py')
                print(i)
                os.mkdir(i)
                os.chdir(i)
                with open('main.py', 'wb') as file:
                    file.write(response.content)
                with open('.opmpack', 'w') as file:
                    file.write(f'{i}\n{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nNULL')
                    file.close()


if __name__ == '__main__':
    Main()
