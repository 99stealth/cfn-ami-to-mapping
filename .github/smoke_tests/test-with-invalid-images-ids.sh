#!/bin/bash

echo "------------------ Testing with image names ------------------"

python cfn_ami_to_mapping.run -i ami-xxx -k AMILinux -i ami-yyy -k AMILinux2 -q
if [ $? != 0 ]; then 
    echo "[+] Test Passed"
else
    echo "[-] Test Failed"
    exit 1
fi

echo "--------------------------------------------------------------"