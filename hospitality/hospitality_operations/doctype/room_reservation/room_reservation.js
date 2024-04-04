// Copyright (c) 2024, service and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Room Reservation", {
// 	refresh(frm) {

// 	},
// });


// frappe.ui.form.on('Room Reservation', {
//     refresh: function(frm) {
//         toggle_fields_based_on_status(frm);
//     },
//     status: function(frm) {
//         toggle_fields_based_on_status(frm);
//     },
//     onload: function(frm) {
//         // If the check-in or check-out time is not set, apply default values
//         if (!frm.doc.expected_check_in_time) {
//             frm.set_value('actual_check_in_time', '12:00');
//         }
//         if (!frm.doc.expected_check_out_time) {
//             frm.set_value('actual_check_out_time', '14:00');
//         }
//     }
// });

// function toggle_fields_based_on_status(frm) {
//     // Hide all fields initially
//     let fields_to_hide = ['expected_check_in_date', 'actual_check_in_time', 'expected_check_out_date', 'actual_check_out_time', 'selected_room', 'agency_name', 'room_rate'];
//     fields_to_hide.forEach(function(field) {
//         frm.set_df_property(field, 'hidden', true);
//     });
    
//     // Logic to show fields based on status
//     if (frm.doc.status === 'Block') {
//         // Show only check-in, check-out dates, and room details
//         frm.set_df_property('expected_check_in_date', 'hidden', false);
//         frm.set_df_property('expected_check_out_date', 'hidden', false);
//         frm.set_df_property('selected_room', 'hidden', false);
//     } else if (frm.doc.status === 'Reserve') {
//         // Show all fields for the 'Reserve' status
//         fields_to_hide.forEach(function(field) {
//             frm.set_df_property(field, 'hidden', false);
//         });
//     }
//     // Add other status conditions if necessary
// }






// frappe.ui.form.on('Room Reservation', {
//     refresh: function(frm) {
//         toggle_fields_based_on_status(frm);
//     },
//     status: function(frm) {
//         toggle_fields_based_on_status(frm);
//     },
//     onload: function(frm) {
//         // Set default values only if the fields are empty
//         if (!frm.doc.actual_check_in_time) {
//             frm.set_value('actual_check_in_time', '12:00');
//         }
//         if (!frm.doc.actual_check_out_time) {
//             frm.set_value('actual_check_out_time', '14:00');
//         }
//     }
// });

// function toggle_fields_based_on_status(frm) {
//     // Decide which fields to show or hide based on status
//     let fieldsToShow = [];
//     let fieldsToHide = ['actual_check_in_time', 'actual_check_out_time', 'agency_name', 'room_rate', 'selected_room', 'expected_check_in_date', 'expected_check_out_date'];

//     switch (frm.doc.status) {
//         case 'Block':
//             fieldsToShow = ['expected_check_in_date', 'expected_check_out_date', 'selected_room'];
//             break;
//         case 'Reserve':
//             fieldsToShow = ['agency_name','room_rate', 'selected_room', 'expected_check_in_date', 'expected_check_out_date'];
//             break;
//         case 'Check-In':
//             fieldsToShow = ['actual_check_in_time']; // Include other fields as needed
//             break;
//         case 'Check-Out':
//             fieldsToShow = ['actual_check_out_time']; // Include other fields as needed
//             break;
//         // Handle other statuses if necessary
//     }

//     // Hide all fields initially
//     fieldsToHide.forEach(function(field) {
//         frm.set_df_property(field, 'hidden', true);
//     });

//     // Show the fields required for the current status
//     fieldsToShow.forEach(function(field) {
//         frm.set_df_property(field, 'hidden', false);
//     });
// }

