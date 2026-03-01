from database.db_manager import DatabaseManager
from datetime import datetime

print("Initializing database ...")
db = DatabaseManager()
print("Database created Successfully")

test_flow = {
    'timestamp': datetime.now(),
    'location_name': 'Test Location',
    'latitude': 40.7580,
    'longitude': -73.9855,
    'road_name': 'Test Road',
    'current_speed': 50,
    'free_flow_speed': 60,
    'current_travel_time': 120,
    'free_flow_travel_time': 100,
    'congestion_level': 'light',
    'confidence': 0.95,
    'road_closure': False
}

flow_id = db.save_traffic_flow(test_flow)
print(f"Inserted traffic flow with ID: {flow_id}")

stats = db.get_statistics(hours=24)
print(f"Statistics: {stats}")