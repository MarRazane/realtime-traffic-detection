from config.config import Config

config = Config()

print("Testing configuration...")
print(f" API Key: {config.TOMTOM_API_KEY[:10]}...{config.TOMTOM_API_KEY[-4:]}")
print(f" Database Path: {config.SQLITE_DB_PATH}")
print(f" Monitoring Interval: {config.MONITORING_INTERVAL} seconds")
print(f" Locations to Monitor: {len(config.LOCATIONS_TO_MONITOR)}")
print(f" Dashboard Port: {config.DASHBOARD_PORT}")

print("\n Configuration is working!")