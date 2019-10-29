from setuptools import setup, find_packages

setup(
    name='cfn-ami-to-mapping',
    version='0.7.0',
    description='Get AMI IDs per region automatically for your CloudFormation template',
    author='Roman Banakh',
    author_email='banakh.ri@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['cfn_ami_to_mapping.helper']),
    install_requires=['argparse', 'boto3', 'pyjson', 'pyyaml', 'more-itertools', 'futures'],
    entry_points={
        'console_scripts': [
            'cfn-ami-to-mapping=cfn_ami_to_mapping.run:main'
        ]
    }
)
