from database.db_manager import DatabaseManager

db = DatabaseManager()  

print("Database Check")
print("=" * 60)

flows = db.get_recent_traffic_flow(hours=1)

print(f"Recent Traffic Flows : {len(flows)} ")

if flows:
    print("\n Latest record:")
    for flow in flows[:5]:  
        print(f" {flow.location_name}")
        print(f" Timestamp: {flow.timestamp}")
        print(f" speed: {flow.current_speed} KM/H")
        print(f" Congestion: {flow.congestion_level}")
        print(" Road : {flow.road_name}")
else:
    print(" No traffic flow records found in the last hour.")


stats = db.get_statistics(hours=24)
print(f" \nStatistics for 24 hours:")
print(f" Total records: {stats['total_records']}")
print(f" Total incidents: {stats['total_incidents']}")
print(f" Active alerts: {stats['active_alerts']}")

print('Done')