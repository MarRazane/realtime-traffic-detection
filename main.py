import sys
import argparse
from data_collection.scheduler import TrafficMonitor
from database.db_manager import DatabaseManager
import threading


def run_montoring():
    print("Starting traffic monitoring...")
    monitor = TrafficMonitor()
    monitor.start_monitoring()

def initialize_database():
    print("Initializing database...")
    db = DatabaseManager()

def main():
    parser = argparse.ArgumentParser(description="Real-Time Traffic Detection System")
    parser.add_argument('command', choices=['init-db', 'monitor'], help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'minitor':
        run_montoring()
    elif args.command == 'init-db':
        initialize_database()

if __name__ == "__main__":
    main()