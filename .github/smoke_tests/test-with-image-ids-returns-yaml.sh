#!/bin/bash

echo "------------------- Testing with image ids -------------------"

python -m cfn_ami_to_mapping.run -i ami-035b3c7efe6d061d5 -k AMILinux -i ami-0b898040803850657 -k AMILinux2 --aws-access-key-id=${AWS_ACCESS_KEY_ID} --aws-secret-access-key=${AWS_SECRET_ACCESS_KEY} -q

if [ $? == 0 ]; then 
    echo "[+] Test Passed"
else
    echo "[-] Test Failed"
    exit 1
fi

echo "--------------------------------------------------------------"