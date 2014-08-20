//
//  importInquiries.js

//  2014-07-03
//

/**
 * Import inquiries or applicants from QSImporter.
 * QSImporter should have a JSONArray, each with an object with fields
 * matching the Add Inquiry/Add Applicant page.
 */

var inquiries = QSImporter.getData();

new QSIterator("*", function() {
    var inquiry = inquiries[this.currentIndex];
    this.click("Add");
    this.afterLoad(function() {
        for(var key in inquiry) {
            var val = inquiry[key];
            QSIterator.setQPVal(key, val);
        }
        this.click(["Save & Close", "Save"]);
        this.afterLoad(this.next);
    });
}, true, inquiries.length).start()
