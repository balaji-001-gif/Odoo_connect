# Odoo Server Action Scripts
# These scripts are intended to be used in Odoo's "Server Actions" or "Automated Actions".
# Trigger: On Creation or Update of the respective model.

import requests
import json

# Configuration
FRAPPE_URL = "https://your-frappe-site.com"
API_KEY = "your_api_key" # If authentication is needed, though endpoints are allow_guest=True currently

# ---------------------------------------------------------
# 1. Sync Course
# Model: op.course (OpenEducat) or equivalent in Smart School
# ---------------------------------------------------------
def sync_course(record):
    url = f"{FRAPPE_URL}/api/method/odoo_connect.odoo_connect.api.sync_course"
    data = {
        "course_name": record.name,
        "course_code": record.code,
        "description": record.description or ""
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        # log(f"Synced Course {record.name}: {response.json()}")
    except Exception as e:
        # log(f"Error syncing Course {record.name}: {str(e)}")
        pass

# ---------------------------------------------------------
# 2. Sync Batch
# Model: op.batch (OpenEducat) or equivalent
# ---------------------------------------------------------
def sync_batch(record):
    url = f"{FRAPPE_URL}/api/method/odoo_connect.odoo_connect.api.sync_batch"
    # Assuming batch has a link to course
    course_name = record.course_id.name if record.course_id else None
    data = {
        "batch_name": record.name,
        "course_name": course_name
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        pass

# ---------------------------------------------------------
# 3. Sync Room
# Model: op.classroom (OpenEducat) or equivalent
# ---------------------------------------------------------
def sync_room(record):
    url = f"{FRAPPE_URL}/api/method/odoo_connect.odoo_connect.api.sync_room"
    data = {
        "room_name": record.name,
        "capacity": record.capacity
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
    except Exception as e:
        pass
