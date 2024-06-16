#!/bin/bash

# Set environment variables
export DATABASE_URL='sqlite:///app.db'
export port=5000

# Step 1: Create the database schema
echo "Creating database schema..."
python -c "
from sqlalchemy import create_engine
from models import Base
engine = create_engine('$DATABASE_URL')
Base.metadata.create_all(engine)
"
echo "Database schema created."

# Step 2: Ingest weather data
echo "Ingesting weather data..."
python ingest_weather_data.py
echo "Weather data ingested."

# Step 3: Calculate and store weather statistics
echo "Calculating and storing weather statistics..."
python calculate_weather_stats.py
echo "Weather statistics calculated and stored."

# Step 4: Run test API
echo "Starting test API..."
pytest tests.py

# Step 5: Run the Flask API
echo "Starting Flask API..."
export FLASK_APP=app.py
flask run --port $port
