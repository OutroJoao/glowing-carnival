#!/bin/bash

echo "========================================"
echo "Condominium Agent - Test Suite"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Running tests..."
echo "========================================"

# Run pytest with coverage
pytest tests/ -v --cov=src --cov-report=html --cov-report=term-missing

echo ""
echo "========================================"
echo "Test run complete!"
echo "Coverage report: htmlcov/index.html"
echo "========================================"
