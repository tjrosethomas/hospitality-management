// Copyright (c) 2024, service and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Building", {
// 	refresh(frm) {

// 	},
// });
frappe.ui.form.on('Building', {
    refresh: function(frm) {
        // Make the building name field read-only after saving the document
        if (!frm.is_new()) {
            frm.set_df_property('building_name', 'read_only', 1);
            frappe.msgprint('Building Name is uneditable for existing records.');
        }
    },   
     
    before_delete: function(frm) {
        // Show a confirmation dialog before deletion
        frappe.confirm(
            __('Are you sure you want to delete this building?'),
            function() {
                // User confirmed deletion, proceed server-side
                frm.save('Delete');
            },
            function() {
                // User canceled deletion
                frappe.show_alert(__('Deletion canceled'));
                return false; // Prevent deletion
            }
        );
        return false; // Prevent automatic deletion to await user confirmation
    }
});


