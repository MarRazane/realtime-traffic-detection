import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time

class TomTomTrafficAPI:
    
    
    def __init__(self, api_key: str):
       
        self.api_key = api_key
        self.base_url = "https://api.tomtom.com/traffic"
        self.session = requests.Session()
        
    def get_traffic_flow(self, 
                        latitude: float, 
                        longitude: float, 
                        zoom: int = 10) -> Optional[Dict]:
        
        endpoint = f"{self.base_url}/services/4/flowSegmentData/absolute/{zoom}/json"
        
        params = {
            'key': self.api_key,
            'point': f"{latitude},{longitude}"
        }
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching traffic flow: {e}")
            return None
    
    def get_traffic_incidents(self, 
                             bbox: Tuple[float, float, float, float],
                             category_filter: Optional[List[int]] = None) -> Optional[Dict]:
        
        endpoint = f"{self.base_url}/services/5/incidentDetails"
        
        min_lon, min_lat, max_lon, max_lat = bbox
        
        params = {
            'key': self.api_key,
            'bbox': f"{min_lon},{min_lat},{max_lon},{max_lat}",
            'fields': '{incidents{type,geometry{type,coordinates},properties{id,iconCategory,magnitudeOfDelay,events{description,code,iconCategory},startTime,endTime,from,to,length,delay,roadNumbers,timeValidity}}}'
        }
        
        if category_filter:
            params['categoryFilter'] = ','.join(map(str, category_filter))
        
        try:
            response = self.session.get(endpoint, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching traffic incidents: {e}")
            return None
    
    def parse_flow_data(self, flow_data: Dict) -> List[Dict]:
      
        parsed_records = []
        
        if not flow_data or 'flowSegmentData' not in flow_data:
            return parsed_records
        
        data = flow_data['flowSegmentData']
        
        record = {
            'timestamp': datetime.now().isoformat(),
            'road_name': data.get('frc', 'Unknown'),
            'latitude': data.get('coordinates', {}).get('coordinate', [{}])[0].get('latitude'),
            'longitude': data.get('coordinates', {}).get('coordinate', [{}])[0].get('longitude'),
            'current_speed': data.get('currentSpeed', 0),
            'free_flow_speed': data.get('freeFlowSpeed', 0),
            'current_travel_time': data.get('currentTravelTime', 0),
            'free_flow_travel_time': data.get('freeFlowTravelTime', 0),
            'confidence': data.get('confidence', 0),
            'road_closure': data.get('roadClosure', False),
            'congestion_level': self._calculate_congestion_level(
                data.get('currentSpeed', 0),
                data.get('freeFlowSpeed', 1)
            )
        }
        
        parsed_records.append(record)
        
        return parsed_records
    
    def parse_incident_data(self, incident_data: Dict) -> List[Dict]:
       
        parsed_incidents = []
        
        if not incident_data or 'incidents' not in incident_data:
            return parsed_incidents
        
        for incident in incident_data.get('incidents', []):
            properties = incident.get('properties', {})
            geometry = incident.get('geometry', {})
            coordinates = geometry.get('coordinates', [])
            
            events = properties.get('events', [])
            description = events[0].get('description', 'No description') if events else 'No description'
            event_code = events[0].get('code', 'unknown') if events else 'unknown'
            
            parsed_incident = {
                'timestamp': datetime.now().isoformat(),
                'incident_id': properties.get('id', 'unknown'),
                'icon_category': properties.get('iconCategory', 'unknown'),
                'magnitude_of_delay': properties.get('magnitudeOfDelay', 0),
                'description': description,
                'event_code': event_code,
                'start_time': properties.get('startTime', None),
                'end_time': properties.get('endTime', None),
                'from_location': properties.get('from', 'Unknown'),
                'to_location': properties.get('to', 'Unknown'),
                'length': properties.get('length', 0),
                'delay': properties.get('delay', 0),
                'road_numbers': properties.get('roadNumbers', []),
                'latitude': coordinates[1] if len(coordinates) >= 2 else None,
                'longitude': coordinates[0] if len(coordinates) >= 2 else None,
                'severity': self._calculate_severity(properties.get('magnitudeOfDelay', 0))
            }
            
            parsed_incidents.append(parsed_incident)
        
        return parsed_incidents
    
    def _calculate_congestion_level(self, current_speed: float, free_flow_speed: float) -> str:
       
        if free_flow_speed == 0:
            return "unknown"
        
        ratio = current_speed / free_flow_speed
        
        if ratio > 0.85:
            return "free_flow"
        elif ratio > 0.65:
            return "light"
        elif ratio > 0.45:
            return "moderate"
        elif ratio > 0.25:
            return "heavy"
        else:
            return "severe"
    
    def _calculate_severity(self, magnitude: int) -> str:
        
        severity_map = {
            0: "unknown",
            1: "minor",
            2: "moderate",
            3: "major",
            4: "critical"
        }
        return severity_map.get(magnitude, "unknown")
