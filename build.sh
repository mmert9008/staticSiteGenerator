#!/bin/bash

# Execute the main Python script to build the site for production
# Pass the repository name as the basepath argument
python3 src/main.py "/staticSiteGenerator/"

echo "Production build finished."
