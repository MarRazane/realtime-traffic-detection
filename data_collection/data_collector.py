
from data_collection.tomtom_traffic_api import TomTomTrafficAPI
from database.db_manager import DatabaseManager
from config.config import Config
from datetime import datetime
import time

class DataCollector:
    
    def __init__(self):
        self.config = Config()
        self.api = TomTomTrafficAPI(self.config.TOMTOM_API_KEY)
        self.db = DatabaseManager()
    
    def collect_traffic_flow(self, location):
        print(f"Collecting traffic flow for {location['name']}...")
        
        flow_data = self.api.get_traffic_flow(
            latitude=location['lat'],
            longitude=location['lon'],
            zoom=10
        )
        
        if flow_data:
            parsed_flows = self.api.parse_flow_data(flow_data)
            
            for flow in parsed_flows:
                flow['location_name'] = location['name']
                flow_id = self.db.save_traffic_flow(flow)
                
                if flow_id:
                    print(f" Saved flow data (ID: {flow_id})")
                    print(f" Speed: {flow['current_speed']} km/h, Congestion: {flow['congestion_level']}")
            
            return len(parsed_flows)
        return 0
    
    def collect_traffic_incidents(self, bbox):
        print(f"Collecting traffic incidents...")
        
        incident_data = self.api.get_traffic_incidents(bbox)
        
        if incident_data:
            parsed_incidents = self.api.parse_incident_data(incident_data)
            
            for incident in parsed_incidents:
                incident_id = self.db.save_traffic_incident(incident)
                
                if incident_id:
                    print(f"  Saved incident (ID: {incident_id})")
                    print(f"  Type: {incident['icon_category']}, Severity: {incident['severity']}")
            
            return len(parsed_incidents)
        return 0
    
    def collect_all(self):
        print(f"\n{'='*60}")
        print(f"Data Collection Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        total_flows = 0
        total_incidents = 0
        
        for location in self.config.LOCATIONS_TO_MONITOR:
            flows = self.collect_traffic_flow(location)
            total_flows += flows
            time.sleep(1)  
        
        for location in self.config.LOCATIONS_TO_MONITOR:
            lat = location['lat']
            lon = location['lon']
            bbox = (lon - 0.25, lat - 0.25, lon + 0.25, lat + 0.25)  
            incidents = self.collect_traffic_incidents(bbox)
            total_incidents += incidents
            time.sleep(1)
            
        print(f"\n{'='*60}")
        print(f"Collection Complete!")
        print(f"  Total Flow Records: {total_flows}")
        print(f"  Total Incidents: {total_incidents}")
        print(f"{'='*60}\n")
        
        return total_flows, total_incidents