__author__ = 'mohamed'
import subprocess,sys


def run(command,Wait=True):
    out = ""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        sys.stdout.write(nextline)
        out += nextline
        sys.stdout.flush()

    return [process.returncode,out]
