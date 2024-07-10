#!/bin/bash

# Function to display help message
display_help() {
    echo "Usage: $0 [-p PYTHON_VERSION] [-r REQUIREMENTS_FILE]"
    echo
    echo "   -p PYTHON_VERSION    Specify the Python version to use (e.g., 3.8)"
    echo "   -r REQUIREMENTS_FILE Specify the path to the requirements.txt file"
    echo
    exit 1
}

# Default values
PYTHON_VERSION="python3.11"
REQUIREMENTS_FILE="requirements.txt"

# Parse command-line arguments
while getopts ":p:r:h" opt; do
    case $opt in
        p)
            PYTHON_VERSION=$OPTARG
            ;;
        r)
            REQUIREMENTS_FILE=$OPTARG
            ;;
        h)
            display_help
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            display_help
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            display_help
            ;;
    esac
done

# Create a virtual environment with the specified Python version
echo "Creating virtual environment with $PYTHON_VERSION..."
$PYTHON_VERSION -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install the libraries from the requirements.txt file
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing libraries from $REQUIREMENTS_FILE..."
    pip install -r $REQUIREMENTS_FILE
else
    echo "Requirements file $REQUIREMENTS_FILE not found."
fi

echo "Virtual environment setup complete."

