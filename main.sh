#!/bin/bash

# Execute the main Python script to generate the site
python3 src/main.py

# Check if the public directory was created
if [ -d "public" ]; then
    echo "Starting local web server at http://localhost:8888"
    # Change directory to public and start the server
    cd public && python3 -m http.server 8888
else
    echo "Public directory not found. Site generation failed."
    exit 1
fi

