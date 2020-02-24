#!/bin/bash
cd /root
/usr/bin/screen -d -m python3 main.py
/usr/sbin/sshd -D