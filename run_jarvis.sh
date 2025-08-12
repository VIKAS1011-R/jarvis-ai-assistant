#!/bin/bash
echo "Starting J.A.R.V.I.S..."
echo

# Check if virtual environment exists
if [ ! -d "jarvis_env" ]; then
    echo "Virtual environment not found. Running setup first..."
    python3 setup.py
    echo
fi

# Activate virtual environment and run J.A.R.V.I.S
echo "Activating virtual environment..."
source jarvis_env/bin/activate
echo "Running J.A.R.V.I.S..."
python jarvis.py

# Deactivate when done
deactivate
echo
echo "J.A.R.V.I.S has been shut down."