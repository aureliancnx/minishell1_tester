import json
import subprocess
import sys

def exec_process(test):
    try:
        cmds = test['commands']
        cmds.insert(0, sys.argv[1])
        proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        proc.wait(10)
        ot = process.stdout.read()
        return proc.returncode, ot
    except:
        return -1, None

def start_test(test):
    rcode, ot = exec_process(test)
    if rcode == -1:
        print("Test [{0}]: Test failed.".format(test['name']))

def main():
    tests = None

    try:
        fl = open("tests.json")
        cnt = fl.read()
        tests = json.loads(cnt)
    except IOError as e:
        print("Unable to open tests.json: no such file or permission denied.")
        return 1
    if tests is None:
        print("Unable to load tests from tests.json.")
        return 1
    [start_test(q) for q in tests]
    return 0

if __name__ == "__main__":
    exit(main())
