#!/bin/bash

# Update packages
sudo apt update

# Install specific Python version
sudo apt install python3.10

# Install python3.10-venv to resolve the absence of ensurepip
sudo apt install python3.10-venv

# Create a Python virtual environment
python3.10 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install other requirements
pip install -r requirements.txt

# Add Python path to .bashrc
echo "export PYTHONPATH=\"${PYTHONPATH}:/home/theia/.local/lib/python3.11/site-packages\"" >> ~/.bashrc
echo "export PATH=\$PATH:/path/to/python" >> ~/.bashrc

# Source .bashrc
source ~/.bashrc

# Show Django version
pip show django

# Run entrypoint.sh
./entrypoint.sh
