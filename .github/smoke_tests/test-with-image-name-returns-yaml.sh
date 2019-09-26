#!/bin/bash

echo "------------------ Testing with image names ------------------"

python cfn_ami_to_mapping.run -n amzn-ami-hvm-2018.03.0.20190611-x86_64-gp2 -k AMILinux -n amzn2-ami-hvm-2.0.20190618-x86_64-gp2 -k AMILinux2 --aws-access-key-id=${AWS_ACCESS_KEY_ID} --aws-secret-access-key=${AWS_SECRET_ACCESS_KEY} -q

if [ $? == 0 ]; then 
    echo "[+] Test Passed"
else
    echo "[-] Test Failed"
    exit 1
fi

echo "--------------------------------------------------------------"