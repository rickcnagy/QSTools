/**
 * Create a final grade formula in each gradebook that DOESN'T HAVE ANY FORMULA
 * COLUMNS.
 *
 * This spans all semesters, so it'll create final grades in all gradebooks in
 * all semesters that don't have formulas.
 *
 * The formulas is a final grade formula, simply 100% assignment.
 *
 * If you don't want to start on a particular teacher, leave startingTeacher
 * blank.
 */

var startingTeacher = "Zahir";

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
}, startingTeacher).start();
