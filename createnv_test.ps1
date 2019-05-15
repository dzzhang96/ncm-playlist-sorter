"""
    File:           './createnv_test.ps1'
    Author:         'yuetsin'
    Description:    For CI tests only. Creates an virtual python environment
                    and executes the playlist sorter. 
    Last ModTime:   2019/5/12
"""

$Env:PY_PYTHON = 3

# Install virtualenv package
pip install virtualenv

# Create venv folder
mkdir venv
Set-Location venv

# Create environment
virtualenv --no-site-packages venv

# Activate environment
./venv/Scripts/activate

# Run Script
Set-Location ../
pip install -r requirements.txt

# Get resp.rb

Get-Content resp.rb | & python src/sorter.py

# Deactivate
deactivate

# Remove environment
rmdir ./venv