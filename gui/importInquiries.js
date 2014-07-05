//
//  importInquiries.js
//  Rick Nagy (@br1ckb0t)
//  2014-07-03
//

/* Import inquiries from QSImporter
 * QSImoprter should have a JSONArray, each with an object with fields
 * matching the Add Inquiry Page
 */

inquiries = QSImporter.getData();

new QSIterator("*", function() {
    inquiry = inquiries[this.currentIndex];
    this.click("Add Student Inquiry");
    this.afterLoad(function() {
        for(var key in inquiry) {
            var val = inquiry[key];
            QSIterator.setQPVal(key, val);
        }
        this.click("Save And Close");
        this.afterLoad(this.next);
    });
}, true, inquiries.length).start()
