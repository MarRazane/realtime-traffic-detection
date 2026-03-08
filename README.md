# Real-Time Traffic Detection System

This project collects **real-time traffic data** using the TomTom
Traffic API, detects congestion or incidents, and shows the results in a
simple web dashboard.

------------------------------------------------------------------------

## Main Features

-   Collect real-time traffic data
-   Detect traffic congestion
-   Detect traffic incidents
-   Store data in a database
-   View traffic data in a web dashboard

------------------------------------------------------------------------

## Project Structure

realtime_traffic/ ├── config/ \# Configuration settings ├──
data_collection/ \# Traffic API and data collection ├── database/ \#
Database models and manager ├── detection/ \# Congestion and anomaly
detection ├── visualization/ \# Flask dashboard ├── data/ \# SQLite
database ├── main.py \# Main program └── requirements.txt \# Python
dependencies

------------------------------------------------------------------------

## Installation

Install the required libraries:

pip install -r requirements.txt

Create a `.env` file and add your TomTom API key:

TOMTOM_API_KEY=your_api_key_here

Initialize the database:

python main.py init-db

------------------------------------------------------------------------

## Run the Project

Start traffic monitoring:

python main.py monitor

Start the dashboard:

python main.py dashboard

Open in your browser:

http://localhost:5000

Run everything together:

python main.py all

------------------------------------------------------------------------

## Dashboard

The dashboard allows you to:

-   View traffic conditions
-   See congestion levels
-   Monitor incidents
-   View traffic statistics

------------------------------------------------------------------------

## Database

Traffic data is stored in:

data/traffic_data.db
