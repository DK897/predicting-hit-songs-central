#!/bin/bash

# Hit Song Prediction Project - Environment Setup

echo "🚀 Setting up Hit Song Prediction Project Environment"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Set Python path
echo "🔗 Setting Python path..."
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo "export PYTHONPATH=\"\$PYTHONPATH:$(pwd)\"" >> venv/bin/activate

echo "🎉 Environment setup complete!"
echo "📝 To activate the environment, run: source venv/bin/activate"
echo "📝 To run the project, start with: python notebooks/exploratory/01_data_exploration.py"