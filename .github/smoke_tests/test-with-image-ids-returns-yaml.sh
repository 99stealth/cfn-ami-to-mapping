#!/bin/bash

echo "------------------- Testing with image ids -------------------"

python main.py -i ami-xxx -k AMILinux -i ami-yyy -k AMILinux2 -q
if [ $? != 0 ]; then 
    echo "[+] Test Passed"
else
    echo "[-] Test Failed"
fi

echo "--------------------------------------------------------------"