/**
 * Create a final grade formula in each gradebook.
 *
 * The final grade formula is simply 100% assignment.
 */

new QSGradebookIterator(function() {
    if ($(".formulaColumn").length) {
        this.next();
        return;
    }

    this.click("Edit it anyways");
    this.click("Add Formula");
    $("tr.category:contains(Assignment) input").click();
    this.click("Add");
    this.click("Save");

    this.afterLoad(this.next);
}).start();
