
from flask import Flask, render_template, jsonify, request
from database.db_manager import DatabaseManager
from config.config import Config
from datetime import datetime, timedelta
import json

app = Flask(__name__)
config = Config()
db = DatabaseManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/traffic/recent')
def get_recent_traffic():
    hours = request.args.get('hours', 1, type=int)
    flows = db.get_recent_traffic_flow(hours=hours)
    
    data = []
    for flow in flows:
        data.append({
            'timestamp': flow.timestamp.isoformat(),
            'location': flow.location_name,
            'latitude': flow.latitude,
            'longitude': flow.longitude,
            'current_speed': flow.current_speed,
            'free_flow_speed': flow.free_flow_speed,
            'congestion_level': flow.congestion_level,
            'road_closure': flow.road_closure
        })
    
    return jsonify(data)

@app.route('/api/incidents/active')
def get_active_incidents():
    incidents = db.get_active_incidents()
    
    data = []
    for incident in incidents:
        data.append({
            'id': incident.id,
            'incident_id': incident.incident_id,
            'timestamp': incident.timestamp.isoformat(),
            'location': incident.location_name,
            'latitude': incident.latitude,
            'longitude': incident.longitude,
            'type': incident.icon_category,
            'description': incident.description,
            'severity': incident.severity,
            'delay': incident.delay
        })
    
    return jsonify(data)

@app.route('/api/alerts/active')
def get_active_alerts():
    alerts = db.get_active_alerts()
    
    data = []
    for alert in alerts:
        data.append({
            'id': alert.id,
            'timestamp': alert.timestamp.isoformat(),
            'type': alert.alert_type,
            'location': alert.location_name,
            'latitude': alert.latitude,
            'longitude': alert.longitude,
            'severity': alert.severity,
            'message': alert.message
        })
    
    return jsonify(data)

@app.route('/api/statistics')
def get_statistics():
    hours = request.args.get('hours', 24, type=int)
    stats = db.get_statistics(hours=hours)
    
    avg_speed = 0
    if stats['avg_speed']:
        speeds = [s[0] for s in stats['avg_speed'] if s[0] is not None]
        avg_speed = sum(speeds) / len(speeds) if speeds else 0
    
    return jsonify({
        'total_records': stats['total_records'],
        'total_incidents': stats['total_incidents'],
        'active_alerts': stats['active_alerts'],
        'average_speed': round(avg_speed, 2)
    })

@app.route('/api/congestion/distribution')
def get_congestion_distribution():
    hours = request.args.get('hours', 24, type=int)
    flows = db.get_recent_traffic_flow(hours=hours)
    
    distribution = {
        'free_flow': 0,
        'light': 0,
        'moderate': 0,
        'heavy': 0,
        'severe': 0
    }
    
    for flow in flows:
        if flow.congestion_level in distribution:
            distribution[flow.congestion_level] += 1
    
    return jsonify(distribution)

def run_dashboard():
    app.run(
        host=config.DASHBOARD_HOST,
        port=config.DASHBOARD_PORT,
        debug=config.DEBUG_MODE
    )
