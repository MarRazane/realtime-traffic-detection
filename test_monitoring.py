from data_collection.scheduler import TrafficMonitor

monitor = TrafficMonitor()

print("Running monitoring cycle...")
monitor.monitoring_cycle()
print("Monitoring cycle completed.")