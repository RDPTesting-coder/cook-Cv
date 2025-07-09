from arcgis.gis import GIS
from datetime import datetime

# Connect to ArcGIS Online (use your admin credentials)
gis = GIS("https://www.arcgis.com", "your_admin_username", "your_password")

# Item IDs of the two items you want to track
item_ids = ["<item_id_1>", "<item_id_2>"]

# Start date from 2021
start_date = datetime(2021, 1, 1)

# Collect users who edited
edited_users = set()

# Loop through items
for item_id in item_ids:
    logs = gis.admin.logs.query(
        start_time=start_date,
        query=f'itemid:"{item_id}" AND (operation:"update" OR operation:"edit")',
        filter='operations',
        level='verbose',
        max_records=1000
    )
    print(f"Item: {item_id}")
    for log in logs['logMessages']:
        user = log.get('user')
        if user:
            edited_users.add(user)
            print(f"User: {user} | Action: {log['operation']} | Time: {log['created']}")

print("\n✅ Users who edited the items since 2021:")
for user in edited_users:
    print(user)
