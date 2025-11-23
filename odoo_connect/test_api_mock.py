import unittest
from unittest.mock import MagicMock, patch
import sys

# Mock frappe module
sys.modules["frappe"] = MagicMock()
import frappe

# Mock whitelist to be a pass-through decorator
def mock_whitelist(allow_guest=False):
    def decorator(func):
        return func
    return decorator

frappe.whitelist = mock_whitelist

# Import the api module
from odoo_connect.odoo_connect.api import sync_course, sync_batch, sync_room

class TestOdooConnect(unittest.TestCase):
    
    def setUp(self):
        frappe.db.exists.return_value = None
        frappe.db.exists.side_effect = None
        frappe.get_doc.return_value = MagicMock()

    def test_sync_course_create(self):
        frappe.db.exists.return_value = None
        response = sync_course("Mathematics", "MATH101", "Intro to Math")
        self.assertEqual(response["status"], "success")
        self.assertIn("created", response["message"])
        frappe.get_doc.assert_called()

    def test_sync_course_update(self):
        frappe.db.exists.return_value = "LMS Course/Mathematics"
        mock_doc = MagicMock()
        frappe.get_doc.return_value = mock_doc
        
        response = sync_course("Mathematics", "MATH101", "New Description")
        self.assertEqual(response["status"], "success")
        self.assertIn("updated", response["message"])
        # Verify description was updated
        self.assertEqual(mock_doc.description, "New Description")
        mock_doc.save.assert_called()

    def test_sync_batch_create(self):
        frappe.db.exists.side_effect = [None, "LMS Course/Mathematics"] # Batch doesn't exist, Course exists
        
        response = sync_batch("Batch A", "Mathematics")
        self.assertEqual(response["status"], "success")
        self.assertIn("created", response["message"])

    def test_sync_room_create(self):
        frappe.db.exists.return_value = None
        response = sync_room("Room 101", 30)
        self.assertEqual(response["status"], "success")
        self.assertIn("created", response["message"])

if __name__ == "__main__":
    unittest.main()
