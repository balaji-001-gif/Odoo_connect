import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def sync_course(course_name, course_code=None, description=None):
    """
    Sync Course from Odoo to Frappe LMS Course
    """
    if not course_name:
        return {"status": "error", "message": "Course Name is required"}

    # Check if course exists
    course_exists = frappe.db.exists("LMS Course", {"course_name": course_name})
    
    if course_exists:
        doc = frappe.get_doc("LMS Course", course_exists)
        doc.description = description
        doc.save(ignore_permissions=True)
        return {"status": "success", "message": f"Course {course_name} updated", "name": doc.name}
    else:
        doc = frappe.get_doc({
            "doctype": "LMS Course",
            "title": course_name,
            "course_code": course_code,
            "description": description,
            "published": 1
        })
        doc.insert(ignore_permissions=True)
        return {"status": "success", "message": f"Course {course_name} created", "name": doc.name}

@frappe.whitelist(allow_guest=True)
def sync_batch(batch_name, course_name=None):
    """
    Sync Batch from Odoo to Frappe Student Group
    """
    if not batch_name:
        return {"status": "error", "message": "Batch Name is required"}

    # Check if Student Group exists
    group_exists = frappe.db.exists("Student Group", {"student_group_name": batch_name})
    
    if group_exists:
        return {"status": "success", "message": f"Batch {batch_name} already exists", "name": group_exists}
    else:
        # Find course if provided
        course = None
        if course_name:
            course = frappe.db.exists("LMS Course", {"title": course_name})
        
        doc = frappe.get_doc({
            "doctype": "Student Group",
            "student_group_name": batch_name,
            "group_based_on": "Course" if course else "Activity",
            "course": course
        })
        doc.insert(ignore_permissions=True)
        return {"status": "success", "message": f"Batch {batch_name} created", "name": doc.name}

@frappe.whitelist(allow_guest=True)
def sync_room(room_name, capacity=None):
    """
    Sync Room from Odoo to Frappe Room
    """
    if not room_name:
        return {"status": "error", "message": "Room Name is required"}

    # Check if Room exists
    # Note: Assuming 'Room' doctype exists in ERPNext/Education or creating a custom one if needed.
    # Standard ERPNext Education uses 'Room'
    room_exists = frappe.db.exists("Room", {"room_name": room_name})
    
    if room_exists:
        doc = frappe.get_doc("Room", room_exists)
        if capacity:
            doc.seating_capacity = capacity
        doc.save(ignore_permissions=True)
        return {"status": "success", "message": f"Room {room_name} updated", "name": doc.name}
    else:
        doc = frappe.get_doc({
            "doctype": "Room",
            "room_name": room_name,
            "seating_capacity": capacity
        })
        doc.insert(ignore_permissions=True)
        return {"status": "success", "message": f"Room {room_name} created", "name": doc.name}
