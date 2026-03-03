from database.db_manager import DatabaseManager
from datetime import datetime, timedelta
import statistics

class AnomalyDetector:

    def __init__(self):
        self.db = DatabaseManager()

    def detect_speed_anomaly(self, current_flow, historical_hours=24):
        historical_flows = self.db.get_recent_traffic_flow(
            hours=historical_hours,
            location_name=current_flow.location_name
        )

        if len(historical_flows) < 10:
            return {'detected': False, 'reason': 'Insufficient historical data'}
        
        speeds = [f.current_speed for f in historical_flows]
        mean_speed = statistics.mean(speeds)

        try:
            std_dev = statistics.stdev(speeds)
        except:
            return {'detected': False, 'reason': 'Unable to calculate std dev'}
        
        current_speed = current_flow.current_speed

        if std_dev == 0:
            z_score = 0
        else:
            z_score = (current_speed - mean_speed) / std_dev

        is_anomaly = abs(z_score) > 2

        if is_anomaly:
            alert_data = {
                'alert_type': 'anomaly',
                'location_name': current_flow.location_name,
                'latitude': current_flow.latitude,
                'longitude': current_flow.longitude,
                'severity': 'medium',
                'message': f"Traffic anomaly detected at {current_flow.location_name}. "
                          f"Current speed ({current_speed} km/h) is {abs(z_score):.1f} "
                          f"standard deviations from normal ({mean_speed:.1f} km/h)",
                'is_active': True
            }
            alert_id = self.db.save_alert(alert_data)
            return {
                'detected': True,
                'z_score': z_score,
                'current_speed': current_speed,
                'mean_speed': mean_speed,
                'std_dev': std_dev,
                'alert_id': alert_id
            }
        return {
            'detected': False,
            'z_score': z_score,
            'current_speed': current_speed,
            'mean_speed': mean_speed,
            'std_dev': std_dev
        }
