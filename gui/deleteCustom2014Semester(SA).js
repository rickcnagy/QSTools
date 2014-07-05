/*
 * Check that all the subjects have been hidden correctly - by number.
 */

var yearBoxSel = "td[style='width: 286px; padding: 0px;']:contains(2014)";
var students = QSImporter.data();

var iter = new QSIterator("*", function() {
    var student = students[this.currentIndex];
    console.log("Starting student", student);
    $(".dttd:contains(" + student.name + ")").click();
    this.afterLoad(function() {
        if ($(yearBoxSel).length > 2) {
            $(yearBoxSel).eq(1).find("div").first().click();
            $(".items:contains(Delete custom semester)").click();
            this.afterLoad(function() {
                this.click("Save & Close");
                this.afterLoad(this.next);
            });
        }
    });
}, true, students.length);
iter.start();
