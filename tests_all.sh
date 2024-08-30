#!/bin/bash

# Copyright (c) 2024 by Jonathan AW
echo "### Running all tests ..."
echo "."
echo "."
echo "."
echo "."
echo "."
echo "### Running Utils tests ..."
echo "."
echo "."
./tests_utils.sh 
echo "."
echo "."
echo "."
echo "."
echo "."
echo "========================================"
echo "### Running DAL tests ..."
echo "."
echo "."
./tests_dal.sh
echo "."
echo "."
echo "."
echo "."
echo "."
echo "========================================"
echo "### Running BL tests ..."
echo "."
echo "."
./tests_bl.sh

