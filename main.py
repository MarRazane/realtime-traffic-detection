import sys
import argparse
from data_collection.scheduler import TrafficMonitor
from database.db_manager import DatabaseManager
from visualization.dashboard import run_dashboard
from database.db_manager import DatabaseManager
import threading


def run_montoring():
    print("Starting traffic monitoring...")
    monitor = TrafficMonitor()
    monitor.start_monitoring()

def run_dashboard_server():
    print("Starting dashboard server...")
    run_dashboard()


def initialize_database():
    print("Initializing database...")
    db = DatabaseManager()

def run_all():
    initialize_database()
    monitoring_thread = threading.Thread(target=run_montoring, daemon=True)
    monitoring_thread.start()

    run_dashboard_server()

def main():
    parser = argparse.ArgumentParser(description="Real-Time Traffic Detection System",
                                     epilog="Example usage: python main.py monitor")
    parser.add_argument('command', 
                        choices=['init-db', 'monitor', 'dashboard', 'all'], 
                        help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'minitor':
        run_montoring()
    elif args.command == 'dashboard':
        run_dashboard_server()
    elif args.command == 'all':
        run_all()    
    elif args.command == 'init-db':
        initialize_database()

if __name__ == "__main__":
    main()