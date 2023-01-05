frappe.listview_settings['Work Log'] = {
    has_indicator_for_draft: false,
    get_indicator(doc) {
        // customize indicator color
        if (doc.docstatus == 0) {
            return [__("Start"), "orange", "docstatus,=,0"];
        } else if (doc.docstatus == 1) {
            return [__("Complete"), "green", "docstatus,=,1"];
        } else {
            return [__("Cancelled"), "red", "docstatus,=,2"];
        }
    }
}
