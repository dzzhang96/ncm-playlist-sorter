"""
    File:           './createnv.ps1'
    Author:         'yuxiqian' <akaza_akari@sjtu.edu.cn>
    Description:    Creates an virtual python environment
                    and executes the playlist sorter. 
    Last ModTime:   2019/4/24
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