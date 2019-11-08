from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='cfn-ami-to-mapping',
    version='0.7.2',
    description='Get AMI IDs per region automatically for your CloudFormation template',
    long_description=readme(),
    long_description_content_type="text/markdown",
    url='https://github.com/99stealth/cfn-ami-to-mapping',
    author='Roman Banakh',
    author_email='banakh.ri@gmail.com',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=['cfn_ami_to_mapping.helper']),
    include_package_data=True,
    install_requires=['argparse', 'boto3', 'pyjson', 'pyyaml', 'more-itertools', 'futures'],
    entry_points={
        'console_scripts': [
            'cfn-ami-to-mapping=cfn_ami_to_mapping.run:main'
        ]
    }
)
