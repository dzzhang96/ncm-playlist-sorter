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
python src/sorter.py

# Deactivate
deactivate

# Remove environment
rmdir ../venv