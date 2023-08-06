import subprocess


def main():
    script = '''\
#!/bin/sh
source vendor/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
'''
    subprocess.Popen(['sh', '-c', script]).wait()
