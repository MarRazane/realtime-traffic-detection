from database.db_manager import DatabaseManager
from config.config import Config
from datetime import datetime

class CongestionDetector:
    def __init__(self):
        self.config = Config()
        self.db = DatabaseManager()
    
    def detect_congestion(self, flow_data):
        
        current_speed = flow_data.current_speed
        free_flow_speed = flow_data.free_flow_speed

        if free_flow_speed == 0:
            return None
        
        speed_ratio = current_speed / free_flow_speed
        congestion_level = flow_data.congestion_level

        alert_needed = False
        severity = 'low'

        if congestion_level in ['heavy', 'severe']:
            alert_needed = True
            severity = 'high' if congestion_level == 'severe' else 'medium'
        
        if alert_needed:
            alert_data = {
                'alert_type': 'congestion',
                'location_name': flow_data.location_name,
                'latitude': flow_data.latitude,
                'longitude': flow_data.longitude,
                'severity': severity,
                'message' : f"Heavy congestion detected at {flow_data.location_name} with speed {current_speed} km/h (free flow: {free_flow_speed} km/h).",
                'is_active': True
            }

            alert_id = self.db.save_alert(alert_data)

            return {
                'detected': False,
                'congestion_level': congestion_level,
                'speed_ratio': speed_ratio,
            }
        return {
            'detected': False,
            'congestion_level': congestion_level,
            'speed_ratio': speed_ratio,
        }
    
    def analyze_recent_trends(self, location_name, hours=1):
        flows = self.db.get_recent_traffic_flow(hours=hours, location_name=location_name)

        if not flows:
            return None
        
        congestion_counts = {
            'free_flow': 0,
            'light': 0,
            'moderate': 0,
            'heavy': 0,
            'severe': 0
        }

        total_speed = 0

        for flow in flows:
            congestion_counts[flow.congestion_level] += 1
            total_speed += flow.current_speed
        
        average_speed = total_speed / len(flows)

        return {
            'location': location_name,
            'period_hours': hours,
            'total_records': len(flows),
            'avg_speed': average_speed,
            'congestion_distribution': congestion_counts,
            'most_common': max(congestion_counts, key=congestion_counts.get)
        }