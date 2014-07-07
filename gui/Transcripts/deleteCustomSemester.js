/**
 * Delete custom semesters on transcripts with a specific string in the year header box.
 * For instance, to delete all the subjects in 2014, set `deleteString` to 2014.
 */

deleteString = '2014'

var yearBoxSel = "td[style='width: 286px; padding: 0px;']:contains(" + deleteString + ")";
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
