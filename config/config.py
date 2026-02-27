import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOMTOM_API_KEY = os.getenv('TOMTOM_API_KEY')
    #database config
    DATABASE_TYPE = 'sqlite'
    SQLITE_DB_PATH = 'data/traffic_data.db'
    POSTGRES_URI = os.getenv('DATABASE_URL','postgresql://user:password@localhost/traffic_db')

    #monitoring config

    MONITORING_INTERVAL = 300
    LOCATIONS_TO_MONITOR = [
        {'name': 'Times Square, NYC', 'lat': 40.7580, 'lon': -73.9855, 'radius': 2000},
        {'name': 'Downtown LA', 'lat': 34.0522, 'lon': -118.2437, 'radius': 2000},
        {'name': 'Central London', 'lat': 51.5074, 'lon': -0.1278, 'radius': 2000},
    ]

    #detection config
    CONGESTION_THRESHOLDS = {
        'free_flow': 0.85,
        'light': 0.65,
        'moderate':0.45,
        'heavy':0.25
    }

    #Alert Config
    ENABLE_EMAIL_ALERTS =False
    EMAIL_FROM = os.getenv('EMAIL_FROM','razane.marref07@gmail.com')
    EMAIL_TO = os.getenv('EMAIL_TO','recipient@gmail.com')
    SMTP_SERVER = os.getenv('SMTP_SERVER','smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT','587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME','')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')

    #Dashboard CConfig
    DASHBOARD_HOST = '0.0.0.0'
    DASHBOARD_PORT = 5000
    DEBUG_MODE = True