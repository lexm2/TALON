#!/bin/bash

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    source .venv/Scripts/activate
else
    # Linux/macOS
    source .venv/bin/activate
fi

# Install the required packages
pip install torch gym numpy matplotlib tqdm