from detection.congestion_detector import CongestionDetector
from database.db_manager import DatabaseManager
from data_collection.data_collector import DataCollector

print("Collection traffic data...")
collector = DataCollector()
location = {
    'name': 'paris',
    'lat': 40.7580,
    'lon': -73.9855,
    'radius': 2000
}

collector.collect_traffic_flow(location)

print("\nDetecting congestion...")
detector = CongestionDetector()
db = DatabaseManager()

flows = db.get_recent_traffic_flow(hours=1)
print(f"Found {len(flows)} recent flows")

for flow in flows:
    result = detector.detect_congestion(flow)
    if result:
        print(f"Congestion detected: {result}")