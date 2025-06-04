#!/bin/bash

# Generate the site
echo "Generating static site..."
python3 src/main.py

# Start a simple web server
echo "Starting web server at http://localhost:8888"
echo "Press Ctrl+C to stop the server"
cd public && python3 -m http.server 8888