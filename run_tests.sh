#!/bin/bash

# Test runner script for Media-to-Knowledge Pipeline
# This script runs all tests and provides a summary

set -e  # Exit on error

echo "=========================================="
echo "Media-to-Knowledge Pipeline Test Suite"
echo "=========================================="
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "❌ pytest is not installed. Installing..."
    pip install pytest pytest-mock
    echo ""
fi

# Run tests with coverage if available
if command -v pytest-cov &> /dev/null; then
    echo "Running tests with coverage..."
    pytest --cov=. --cov-report=term-missing --cov-report=html
    echo ""
    echo "Coverage report generated in htmlcov/index.html"
else
    echo "Running tests..."
    pytest -v
fi

echo ""
echo "=========================================="
echo "Test run completed!"
echo "=========================================="