#!/bin/bash

# Install requirements from the unzipped additional-files
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Start the inference server (Example using a generic python call)
python inference.py
