#!/usr/bin/env bash 

# File:           './createnv_test.sh'
# Author:         'yuetsin'
# Description:    For CI tests only. Creates an virtual python environment
#                 and executes the playlist sorter. 
# Last ModTime:   2019/5/12


# Install virtualenv package
pip3 install virtualenv

# Create venv folder
mkdir venv
cd venv

# Create environment
virtualenv --no-site-packages venv

# Activate environment
source venv/bin/activate

# Run Script
cd ../
pip3 install -r requirements.txt
python3 src/sorter.py < resp.rb

# Deactivate
deactivate

# Remove environment
rm -rf ./venv