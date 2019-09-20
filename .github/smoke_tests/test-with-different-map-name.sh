#!/bin/bash

echo "------------------ Testing with image names ------------------"

python main.py -n amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2 -k AMILinux --map-name RegionMap --aws-access-key-id=${AWS_ACCESS_KEY_ID} --aws-secret-access-key=${AWS_SECRET_ACCESS_KEY} -q
if [ $? == 0 ]; then 
    echo "[+] Test Passed"
else
    echo "[-] Test Failed"
fi

echo "--------------------------------------------------------------"