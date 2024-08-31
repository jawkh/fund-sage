#!/bin/bash

# Copyright (c) 2024 by Jonathan AW

echo "### Running all tests ..."
echo "."
echo "."
echo "."
echo "."
echo "."
# Navigate to the project root directory
cd "$(dirname "$0")/.." || exit

echo "### Running Utils tests ..."
echo "."
echo "."
echo "."
echo "."
echo "."
./bin/tests_utils.sh 
echo "."
echo "."
echo "."
echo "."
echo "."
echo "========================================"
echo "### Running DAL tests ..."
echo "."
echo "."
echo "."
echo "."
echo "."
./bin/tests_dal.sh
echo "."
echo "."
echo "."
echo "."
echo "."
echo "========================================"
echo "### Running BL tests ..."
echo "."
echo "."
echo "."
echo "."
echo "."
./bin/tests_bl.sh
