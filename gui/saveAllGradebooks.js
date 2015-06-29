/**
 * Save all Gradebooks visible in the Gradebook module.
 */

var startingTeacher = "";

var iter = new QSGradebookIterator(function() {
    this.click("Edit it anyways");
    this.click("Save");
    this.next();
}, startingTeacher).start();

iter.onComplete(function() {
    new Notification("Saved all gradebooks.");
});

iter.start();
