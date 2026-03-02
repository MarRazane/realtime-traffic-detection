from data_collection.data_collector import DataCollector

collector = DataCollector()

location = {
    'name': 'Paris, France', 'lat': 48.8566, 'lon': 2.3522, 'radius': 2000
    
}   

print("Testing traffic flow collection...")
flow_count = collector.collect_traffic_flow(location)
print(f"Collected {flow_count} traffic flow records for {location['name']}.")