from data_collection.data_collector import DataCollector
from detection.congestion_detector import CongestionDetector
from detection.incident_detector import IncidentDetector
from detection.anomaly_detector import AnomalyDetector
from database.db_manager import DatabaseManager
from config.config import Config
import schedule
import time
from datetime import datetime

class TrafficMonitor:

    def __init__(self):
        self.config = Config()
        self.collector = DataCollector()
        self.congestion_detector = CongestionDetector()
        self.incident_detector = IncidentDetector()
        self.anomaly_detector = AnomalyDetector()
        self.db = DatabaseManager()
    
    def run_detection_analysis(self):
        print("\n ... Running detection and analysis ...")

        recent_flows = self.db.get_recent_traffic_flow(hours=0.1)

        for flow in recent_flows:
            congestion_result = self.congestion_detector.detect_congestion(flow)
            if congestion_result and congestion_result['detected']:
                print(f"Congestion alert: {flow.location_name} - {congestion_result['severity']}")

            anomaly_result = self.anomaly_detector.detect_speed_anomaly(flow)
            if anomaly_result['detected']:
                print(f"Anomaly alert: {flow.location_name} - Z-score: {anomaly_result['z_score']:.2f}")
        
    def monitoring_cycle(self):
        print(f"\n")
        print(f"Monitoring Cycle Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        self.collector.collect_all()
        self.run_detection_analysis()

        active_alerts = self.db.get_active_alerts()
        print(f"\nActive Alerts: {len(active_alerts)}")
        for alert in active_alerts[:5]:
            print(f"  - [{alert.severity.upper()}] {alert.alert_type}: {alert.message[:80]}...")

    
    def start_monitoring(self):
        print("Starting traffic monitoring...")
        print(f"Monitoring Interval: {self.config.MONITORING_INTERVAL} seconds")
        print(f"Locations: {len(self.config.LOCATIONS_TO_MONITOR)}")
        print(f"{'='*60}\n")
        
        self.monitoring_cycle()
        
        interval_minutes = self.config.MONITORING_INTERVAL // 60
        schedule.every(interval_minutes).minutes.do(self.monitoring_cycle)

        while True:
            schedule.run_pending()
            time.sleep(1)