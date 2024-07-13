#!/bin/bash

# Define the projects directory
PROJECTS_DIR="projects"

# Check if an argument is provided
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <project_dir_name>"
  exit 1
fi

PROJECT_NAME=$1
FULL_PATH="$PROJECTS_DIR/$PROJECT_NAME"

# Check if the project directory exists
if [ ! -d "$FULL_PATH" ]; then
  echo "Project directory $PROJECT_DIR does not exist. Please provide a valid project name."
  exit 1
fi

# Navigate into the project directory
cd "$FULL_PATH"

# Check for requirements.txt file
if [ ! -f "requirements.txt" ]; then
  echo "requirements.txt not found in $FULL_PATH. Please ensure it exists and try again."
  exit 1
fi

# Check if the venv directory exists
if [ -d ".venv" ]; then
  echo "Using existing virtual environment."
else
  # Create a Python virtual environment if it doesn't exist
  echo "Creating virtual environment and installing dependencies..."
  python3.10 -m venv .venv
  source .venv/bin/activate
  python3.10 -m pip install --upgrade pip
  pip3.10 install --no-cache-dir -r requirements.txt
  python -m ipykernel install --user --name="$PROJECT_NAME"
  echo "Environment ereated & dependencies installed."
fi

echo "Setup completed. Virtual environment is ready to use."