from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database.models import Base, TrafficFlow, TrafficIncident, DetectionAlert
from config.config import Config
from datetime import datetime, timedelta, timezone
import os


class DatabaseManager:
    
    def __init__(self):
        self.config = Config()
        self.engine = self._create_engine()
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def _create_engine(self):
        """Create database engine"""
        if self.config.DATABASE_TYPE == 'sqlite':
            os.makedirs('data', exist_ok=True)
            return create_engine(f'sqlite:///{self.config.SQLITE_DB_PATH}')
        else:
            return create_engine(self.config.POSTGRES_URI)
    
    def save_traffic_flow(self, flow_data):
        """Save traffic flow data to database"""
        session = self.Session()
        try:
            traffic_flow = TrafficFlow(**flow_data)
            session.add(traffic_flow)
            session.commit()
            return traffic_flow.id
        except Exception as e:
            session.rollback()
            print(f"Error saving traffic flow: {e}")
            return None
        finally:
            session.close()
    
    def save_traffic_incident(self, incident_data):
        """Save traffic incident to database"""
        session = self.Session()
        try:
            # Check if incident already exists
            existing = session.query(TrafficIncident).filter_by(
                incident_id=incident_data['incident_id']
            ).first()
            
            if existing:
                # Update existing incident
                for key, value in incident_data.items():
                    setattr(existing, key, value)
                session.commit()
                return existing.id
            else:
                # Create new incident
                incident = TrafficIncident(**incident_data)
                session.add(incident)
                session.commit()
                return incident.id
        except Exception as e:
            session.rollback()
            print(f"Error saving incident: {e}")
            return None
        finally:
            session.close()
    
    def save_alert(self, alert_data):
        """Save detection alert to database"""
        session = self.Session()
        try:
            alert = DetectionAlert(**alert_data)
            session.add(alert)
            session.commit()
            return alert.id
        except Exception as e:
            session.rollback()
            print(f"Error saving alert: {e}")
            return None
        finally:
            session.close()
    
    def get_recent_traffic_flow(self, hours=1, location=None):
        """Get recent traffic flow data"""
        session = self.Session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            query = session.query(TrafficFlow).filter(
                TrafficFlow.timestamp >= cutoff_time
            )
            
            if location:
                query = query.filter(TrafficFlow.location_name == location)
            
            return query.order_by(desc(TrafficFlow.timestamp)).all()
        finally:
            session.close()
    
    def get_active_incidents(self):
        """Get all active incidents"""
        session = self.Session()
        try:
            return session.query(TrafficIncident).filter_by(is_active=True).all()
        finally:
            session.close()
    
    def get_active_alerts(self):
        """Get all active alerts"""
        session = self.Session()
        try:
            return session.query(DetectionAlert).filter_by(is_active=True).all()
        finally:
            session.close()
    
    def resolve_alert(self, alert_id):
        """Mark alert as resolved"""
        session = self.Session()
        try:
            alert = session.query(DetectionAlert).filter_by(id=alert_id).first()
            if alert:
                alert.is_active = False
                alert.resolved_at = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_statistics(self, hours=24):
        """Get traffic statistics"""
        session = self.Session()
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            stats = {
                'total_records': session.query(TrafficFlow).filter(
                    TrafficFlow.timestamp >= cutoff_time
                ).count(),
                'total_incidents': session.query(TrafficIncident).filter(
                    TrafficIncident.timestamp >= cutoff_time
                ).count(),
                'active_alerts': session.query(DetectionAlert).filter_by(is_active=True).count(),
                'avg_speed': session.query(TrafficFlow).filter(
                    TrafficFlow.timestamp >= cutoff_time
                ).with_entities(TrafficFlow.current_speed).all()
            }
            
            return stats
        finally:
            session.close()
