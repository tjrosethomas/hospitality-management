# Copyright (c) 2024, service and contributors
# For license information, please see license.txt

# import frappe
# from frappe.model.document import Document



# import frappe
# from frappe.model.document import Document

# class ReservationRoom(Document):
#     # def after_insert(self):
#     #     frappe.msgprint("Inserting values for new reservation...")

#     def validate(self):
#         # frappe.msgprint("Validation started")
#         self.update_room_status()
#         # frappe.msgprint("Validation completed")

#     def update_room_status(self):
#         # frappe.msgprint("Updating room status...")

#         # Use try-except to handle the case where the Manage Room entry does not exist
#         try:
#             room = frappe.get_doc("Manage Room", self.selected_room)
#             # frappe.msgprint(f"Room found: {self.selected_room}")
#         except frappe.DoesNotExistError:
#             frappe.throw(f"Manage Room entry not found for room number {self.selected_room}")

#         # Prepare the room status entry
#         room_status_entry = {
#             "room_number": self.selected_room,
#             "from_date": self.expected_check_in_date,
#             "to_date": self.expected_check_out_date,
#             "status": self.status
#         }

#         # Append the room status to the child table in Manage Room
#         room.append("room_status_history", room_status_entry)
#         frappe.msgprint("Room status entry appended")

#         # Save the updated Manage Room document
#         room.save()
#         frappe.msgprint("Manage Room document saved")

#         # Commit the changes to the database
#         frappe.db.commit()
#         frappe.msgprint(f"Room status updated for {self.selected_room}")




# #######Avoi date overlapping for Block and also able to edit in manage room#########
# import frappe
# from frappe.model.document import Document

# class ReservationRoom(Document):
#     def validate(self):
#         self.validate_room_availability()
#         self.update_room_status()

#     def validate_room_availability(self):
#         # Check if the room is available
#         unavailable_statuses = ['Block', 'reserve', 'Check-In']
#         rooms = frappe.db.sql("""
#             SELECT room_number
#             FROM `tabRoom History`
#             WHERE parent=%s AND status IN %s
#             AND (%s BETWEEN from_date AND to_date OR %s BETWEEN from_date AND to_date)
#         """, (self.selected_room, tuple(unavailable_statuses), self.expected_check_in_date, self.expected_check_out_date), as_dict=1)

#         if rooms:
#             frappe.throw(f"The selected room {self.selected_room} is not available for the dates selected.")

#     def update_room_status(self):
#         try:
#             room = frappe.get_doc("Manage Room", self.selected_room)
#         except frappe.DoesNotExistError:
#             frappe.throw(f"Manage Room entry not found for room number {self.selected_room}")

#         room_status_entry = {
#             "room_number": self.selected_room,
#             "from_date": self.expected_check_in_date,
#             "to_date": self.expected_check_out_date,
#             "status": self.status
#         }
#         room.append("room_status_history", room_status_entry)
#         room.save()
#         frappe.db.commit()
#         frappe.msgprint(f"Room status updated for {self.selected_room}")






################Set actual time and status from reservation#####

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_datetime

class ReservationRoom(Document):
    def validate(self):
        self.validate_room_availability()
        self.update_room_status()

    def validate_room_availability(self):
        # Check availability only when necessary
        if not self.get('__islocal') and self.has_value_changed('status'):
            if self.has_value_changed('selected_room') or self.has_value_changed('expected_check_in_date') or self.has_value_changed('expected_check_out_date'):
                self.check_availability()
        elif self.get('__islocal'):
            self.check_availability()

    def check_availability(self):
        unavailable_statuses = ['Block', 'Reserve', 'Check-In']
        expected_check_in = get_datetime(self.expected_check_in_date)
        expected_check_out = get_datetime(self.expected_check_out_date)
        rooms = frappe.db.sql("""
            SELECT room_number
            FROM `tabRoom History`
            WHERE parent=%s AND status IN %s
            AND (%s BETWEEN from_date AND to_date OR %s BETWEEN from_date AND to_date)
            AND name != %s
        """, (self.selected_room, tuple(unavailable_statuses), expected_check_in, expected_check_out, self.name if self.name else '0'), as_dict=1)

        if rooms:
            frappe.throw(f"The selected room {self.selected_room} is not available for the dates selected.")

    def update_room_status(self):
        try:
            room = frappe.get_doc("Manage Room", self.selected_room)
        except frappe.DoesNotExistError:
            frappe.throw(f"Manage Room entry not found for room number {self.selected_room}")

        now = now_datetime()
        updated = False
        # Iterate over room status history to find an appropriate entry to update
        for entry in room.get('room_status_history'):
            from_date = get_datetime(entry.from_date)
            to_date = get_datetime(entry.to_date)
            # Tighten matching logic
            if entry.room_number == self.selected_room and self.expected_check_in_date == entry.from_date.strftime('%Y-%m-%d') and self.expected_check_out_date == entry.to_date.strftime('%Y-%m-%d'):
                # Found an entry, update it
                entry.status = self.status
                if self.status == 'Check-In':
                    entry.actual_check_in_time = now
                elif self.status == 'Check-Out':
                    entry.actual_check_out_time = now
                updated = True
                break

        if not updated:
            # No entry was suitable for update, append a new one
            room.append("room_status_history", self.create_room_status_entry(now))

        room.save()
        frappe.db.commit()
        frappe.msgprint(f"Room status updated for {self.selected_room}")

    def create_room_status_entry(self, now):
        return {
            "room_number": self.selected_room,
            "from_date": now if self.status == 'Check-In' else self.expected_check_in_date,
            "to_date": now if self.status == 'Check-Out' else self.expected_check_out_date,
            "status": self.status,
            "actual_check_in_time": now if self.status == 'Check-In' else None,
            "actual_check_out_time": now if self.status == 'Check-Out' else None
        }


