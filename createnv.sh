#!/usr/bin/env bash 

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
python3 src/sorter.py

# Deactivate
deactivate

# Remove environment
rm -rf venv