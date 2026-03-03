from database.db_manager import DatabaseManager
from datetime import datetime

class IncidentDetector:

    def __init__(self):
        self.db = DatabaseManager()

    def process_incident(self, incident_data):
        severity = incident_data.get('severity', 'unknown')

        incident_id = self.db.save_traffic_incident(incident_data)

        if severity in ['major', 'critical']:
            alert_data = {
                'alert_type': 'incident',
                'location_name': incident_data.get('from_location', 'Unknown'),
                'latitude': incident_data.get('latitude'),
                'longitude': incident_data.get('longitude'),
                'severity': 'high' if severity == 'critical' else 'medium',
                'message': f"{incident_data.get('icon_category', 'Incident')} detected: "
                          f"{incident_data.get('description', 'No description')}. "
                          f"Expected delay: {incident_data.get('delay', 0)} seconds",
                'is_active': True
            }
            alert_id = self.db.save_alert(alert_data)
            return {
                'incident_id': incident_id,
                'alert_created': True,
                'severity': severity,
                'alert_id': alert_id
            }
        
        return {
            'incident_id': incident_id,
            'alert_created': False,
            'severity': severity
        }
    
    def get_active_incidents(self):
        return self.db.get_active_incidents()