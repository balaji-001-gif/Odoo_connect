# Odoo Connect

**Odoo Connect** is a Frappe application designed to facilitate real-time data synchronization from Odoo (specifically Smart School / OpenEducat) to Frappe LMS / ERPNext Education.

It provides API endpoints that Odoo can push data to, ensuring that Courses, Batches (Student Groups), and Rooms are kept in sync.

## Features

- **Sync Courses**: Automatically creates or updates `LMS Course` in Frappe when a Course is created/updated in Odoo.
- **Sync Batches**: Creates `Student Group` in Frappe linked to the corresponding Course.
- **Sync Rooms**: Creates or updates `Room` in Frappe with capacity details.

## Installation

1.  **Get the App**:
    ```bash
    bench get-app odoo_connect https://github.com/balaji-001-gif/Odoo_connect.git
    ```

2.  **Install the App**:
    ```bash
    bench --site [your-site-name] install-app odoo_connect
    ```

3.  **Migrate**:
    ```bash
    bench migrate
    ```

## Configuration (Odoo Side)

You need to set up "Automated Actions" or "Server Actions" in your Odoo instance to push data to Frappe.

### Prerequisites
- Ensure your Frappe site is accessible from the Odoo server.
- If your Frappe site is private, you may need to implement authentication (API Key/Secret) in the scripts. Currently, the endpoints are open (`allow_guest=True`) for simplicity but can be secured.

### Setup Steps

1.  **Enable Developer Mode** in Odoo.
2.  **Navigate to Server Actions** (Settings -> Technical -> Actions -> Server Actions).
3.  **Create a New Action** for each model you want to sync (Course, Batch, Room).
4.  **Action To Do**: Select "Execute Python Code".
5.  **Python Code**: Use the scripts provided in the `odoo_scripts` folder of this repository.

#### Example Script (Sync Course)

```python
import requests

# Replace with your Frappe Site URL
FRAPPE_URL = "https://your-frappe-site.com"

def sync_course(record):
    url = f"{FRAPPE_URL}/api/method/odoo_connect.odoo_connect.api.sync_course"
    data = {
        "course_name": record.name,
        "course_code": record.code,
        "description": record.description or ""
    }
    try:
        requests.post(url, data=data)
    except Exception:
        pass

sync_course(record)
```

*Refer to `odoo_scripts/odoo_push_scripts.py` for the full set of scripts.*

## API Endpoints

-   `POST /api/method/odoo_connect.odoo_connect.api.sync_course`
    -   Params: `course_name`, `course_code`, `description`
-   `POST /api/method/odoo_connect.odoo_connect.api.sync_batch`
    -   Params: `batch_name`, `course_name`
-   `POST /api/method/odoo_connect.odoo_connect.api.sync_room`
    -   Params: `room_name`, `capacity`

## License

MIT
