from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class TrafficFlow(Base):
    """Traffic flow data model"""
    __tablename__ = 'traffic_flow'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    location_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    road_name = Column(String(255))
    current_speed = Column(Integer)
    free_flow_speed = Column(Integer)
    current_travel_time = Column(Integer)
    free_flow_travel_time = Column(Integer)
    congestion_level = Column(String(50), index=True)
    confidence = Column(Float)
    road_closure = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<TrafficFlow(location='{self.location_name}', speed={self.current_speed}, congestion='{self.congestion_level}')>"


class TrafficIncident(Base):
    """Traffic incident data model"""
    __tablename__ = 'traffic_incidents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    incident_id = Column(String(100), unique=True)
    location_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    incident_type = Column(String(50))
    description = Column(Text)
    severity = Column(String(50), index=True)
    delay = Column(Integer)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    from_location = Column(String(255))
    to_location = Column(String(255))
    
    def __repr__(self):
        return f"<TrafficIncident(type='{self.incident_type}', severity='{self.severity}', active={self.is_active})>"


class DetectionAlert(Base):
    """Detection alert model"""
    __tablename__ = 'detection_alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    alert_type = Column(String(50), index=True)
    location_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    severity = Column(String(50), index=True)
    message = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    resolved_at = Column(DateTime, nullable=True)
    
    def __repr__(self):
        return f"<DetectionAlert(type='{self.alert_type}', severity='{self.severity}', active={self.is_active})>"
