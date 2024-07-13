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

# Check if the project directory already exists
if [ -d "$FULL_PATH" ]; then
  echo "Directory $FULL_PATH already exists. Aborted."
  exit 1
fi

# Create the project directory
echo "Creating directory $FULL_PATH..."
mkdir "$FULL_PATH"
echo "Directory $FULL_PATH created."
echo

# Navigate into the project directory
cd "$FULL_PATH"

# Create a Python virtual environment
echo "Creating virtual environment..."
python3.10 -m venv .venv
source ".venv/bin/activate"
python3.10 -m pip install --upgrade pip
pip3.10 install ipykernel jupyter
pip3.10 freeze > requirements.txt
echo "Virtual environment created."
echo

echo "Adding virtual environment to jupyter..."
python -m ipykernel install --user --name="$PROJECT_NAME"
echo "Added virtual environment to jupyter."

# Create project structure
echo "Creating project structure..."
mkdir src
mkdir data
cat > main.py <<EOF
def main():
    print("Hello, world!")


if __name__ == '__main__':
    main()
EOF
echo "Project structure created."