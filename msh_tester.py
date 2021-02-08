import json
import subprocess
import sys

def exec_process(test, md):
    try:
        cmds = test['commands']
        cmds.insert(0, sys.argv[1])
        bf = ""
        for cmd in cmds:
            bf += "echo -e '{0}'\n".format(cmd)
            if test['sleeptime'] > 0:
                bf += "sleep {0}\n".format(test['sleeptime'])
        tst_file = open("tmp", "w")
        tst_file.write(bf)
        tst_file.close()
        eproc = subprocess.Popen(("/bin/bash", "-C", "tmp"), stdout=subprocess.PIPE)
        exc = sys.argv[1] if not md else "tcsh"
        proc = subprocess.Popen((exc), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=eproc.stdout)
        proc.wait(10)
        ot = proc.stdout.read()
        print(ot)
        return proc.returncode, ot
    except Exception as e:
        print(e)
        return -1, None

def start_test(test):
    rcode, ot = exec_process(test, False)
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
