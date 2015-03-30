/**
 * Import inquiries or applicants from QSImporter.
 * QSImporter should have a JSON Array that contains objects with fields
 * matching the Add Inquiry/Add Applicant page.
 *
 * See sample at examples/importInquiriesOrApplicants.sample.json
 */

var importIterator = new QSImporter.iterator(function() {
    var inquiryOrApplicant = this.item;
    this.click("Add");
    this.afterLoad(function(){
        for(var key in this.item) {
            var val = inquiryOrApplicant[key];
            QSIterator.setQPVal(key, val);
        }
        this.click(["Save & Close", "Save"]);
        this.afterLoad(this.next);
    });
});

importIterator.start();
