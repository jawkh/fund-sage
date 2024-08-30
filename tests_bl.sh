#!/bin/bash

# Copyright (c) 2024 by Jonathan AW

source ~/.bashrc

pwd

# Get the current directory
currentDirectory=$(pwd)
timestamp=$(date +"%Y%m%d_%H%M%S")
rpt_fileName="logs/bl-pytest-${timestamp}-RPT.log"
rpt_errFileName="logs/bl-pytest-${timestamp}-ERROR.log"

rpt_logFilePath="$currentDirectory/$rpt_fileName"
rpt_errorLogFilePath="$currentDirectory/$rpt_errFileName"

mkdir -p logs


# Run DAL tests
"$(which poetry)" run pytest --cov=bl tests/bl_tests 2> "$rpt_errorLogFilePath" | tee -a "$rpt_logFilePath"

