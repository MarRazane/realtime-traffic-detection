import os
import sqlite3

print("="*60)
print("FORCING DATABASE RESET")
print("="*60)

# Step 1: Delete database file
db_path = 'data/traffic_data.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print(f" Deleted {db_path}")
else:
    print(f"  {db_path} doesn't exist")

# Step 2: Recreate from scratch
print("\nRecreating database...")
from database.db_manager import DatabaseManager
db = DatabaseManager()
print("✅ Database recreated!")

# Step 3: Verify the schema
print("\nVerifying schema...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get column info
cursor.execute("PRAGMA table_info(traffic_incidents);")
columns = cursor.fetchall()

print("\nColumns in traffic_incidents table:")
for col in columns:
    print(f"  - {col[1]} ({col[2]})")

# Check for road_numbers
column_names = [col[1] for col in columns]
if 'road_numbers' in column_names:
    print("\n SUCCESS! 'road_numbers' column exists in database!")
else:
    print("\n FAILED! 'road_numbers' column still missing!")
    print("\nYour database/models.py might have the wrong column name.")
    print("Make sure it says: road_numbers = Column(String(255))")

conn.close()

print("\n" + "="*60)
print("Database reset complete!")
print("="*60)