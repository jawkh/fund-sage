#!/bin/bash

# Copyright (c) 2024 by Jonathan AW

# Source your bash profile (if needed)
source ~/.bashrc

# Print current working directory
pwd

# Navigate to the project root directory
cd "$(dirname "$0")/.." || exit

# Print current working directory after changing directories
echo "Changed directory to project root: $(pwd)"

# Get the current directory after navigating to project root
currentDirectory=$(pwd)
timestamp=$(date +"%Y%m%d_%H%M%S")
rpt_fileName="logs/bl-pytest-${timestamp}-RPT.log"
rpt_errFileName="logs/bl-pytest-${timestamp}-ERROR.log"

rpt_logFilePath="$currentDirectory/$rpt_fileName"
rpt_errorLogFilePath="$currentDirectory/$rpt_errFileName"

# Create the logs directory if it doesn't exist
mkdir -p logs

# Run BL tests using pytest with coverage, and redirect logs
"$(which poetry)" run pytest --cov=bl tests/bl_tests 2> "$rpt_errorLogFilePath" | tee -a "$rpt_logFilePath"
