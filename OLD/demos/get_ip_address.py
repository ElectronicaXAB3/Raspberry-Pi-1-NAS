import sys
from subprocess import Popen, PIPE

INTERFACE="eth0"

def ip_address():
    ip_parse = run_cmd(
        "ip addr show %s" % INTERFACE
    )
    print(ip_parse.splitlines())

    ip = ""
    for line in ip_parse.splitlines():
        if "inet " in line:
            ip = line.split(' ')[5]
            ip = ip.split('/')[0]

    return ip

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.decode('ascii')


# Start the main
if __name__ == '__main__':
    print("IP " + ip_address(), file = sys.stdout)
