import os
import sys
from subprocess import PIPE, Popen, STDOUT
from info_path_sys import path_to_project

env = 'test'
marker = 'smoke'
test_path = path_to_project + '/tests/'
threads = '-n 2'
count = '1'  # '--count=100'


def console_output():
    # PYTHONHASHSEED=0# python -u -m pytest -v -m "fast" --env=test tests/ -n 2 --count 1 --dist=loadgroup --strict-markers --alluredir=allure-results/ --junitxml=report.xml
    command = [
        # f'PYTHONHASHSEED=0',
        f'python',
        f'-u',
        f'-m',
        'pytest',
        '-v',
        # # '-m',
        # # f'{marker}',
        # f'--env={env}',
        # f'{test_path}',
        # f'{threads}',
        # f'--count', f'{count}',
        f'--dist=loadgroup',
        f'--strict-markers',
        f'--alluredir={path_to_project}/allure-results',
        f'--junitxml={path_to_project}/report.xml',
    ]
    cmd = Popen(command, stdout=PIPE, stderr=STDOUT, shell=True)
    while True:
        out = cmd.stdout.read()
        if out == '' and cmd.poll() != None:
            break
        if out != '':
            sys.stdout.write(str(out.decode()))
            sys.stdout.flush()
            break


if __name__ == '__main__':
    console_output()
    os.system(f'allure generate {path_to_project}/allure-results')
