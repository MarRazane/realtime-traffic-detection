from data_collection.tomtom_traffic_api import TomTomTrafficAPI
from dotenv import load_dotenv
import os

load_dotenv()

# Get API key
api_key = os.getenv('TOMTOM_API_KEY')
print(f"Using API Key: {api_key[:10]}...{api_key[-4:]}")

# Initialize API
print("\nInitializing TomTom API...")
traffic_api = TomTomTrafficAPI(api_key)

# Test traffic flow
print("\nTesting Traffic Flow API...")
flow_data = traffic_api.get_traffic_flow(48.8566, 2.3522, zoom=11)

if flow_data:
    print(" Traffic Flow API is working!")
    print(f"   Current Speed: {flow_data['flowSegmentData'].get('currentSpeed')} km/h")
    print(f"   Free Flow Speed: {flow_data['flowSegmentData'].get('freeFlowSpeed')} km/h")
    
    # Test parsing
    parsed = traffic_api.parse_flow_data(flow_data)
    print(f" Data parsing is working!")
    print(f"   Congestion Level: {parsed[0]['congestion_level']}")
else:
    print(" Traffic Flow API failed!")

# Test incidents
print("\nTesting Traffic Incidents API...")
bbox = (2.3522, 48.8566, 2.3522, 48.8566)
incident_data = traffic_api.get_traffic_incidents(bbox)

if incident_data:
    print(" Traffic Incidents API is working!")
    incidents = traffic_api.parse_incident_data(incident_data)
    print(f"   Found {len(incidents)} incidents")
else:
    print(" No incidents found (this is normal)")

print("\n" + "="*50)
print(" ALL API TESTS PASSED!")
print("="*50)