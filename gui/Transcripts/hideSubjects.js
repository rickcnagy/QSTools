/**
 * Hide a specific subjects on transcripts by subject name.
 * QSImporter's data should be like so:
 * `[{name: Rick, subjects: [subjectName1, subjectName2]}]`
 */

var yearBoxSel = "td[style='width: 286px; padding: 0px;']";
var subjectSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Verdana; font-size: 8px; color: rgb(0, 0, 0);']";

var students = QSImporter.data();

new QSIterator("*", function() {
    var student = students[this.currentIndex];
    $(".dttd:contains(" + student.Name + ")").click();
    this.afterLoad(function() {
        var subjects = student.subjects;
        var subjectIter = new QSIterator("*", function() {
            var subjectName = subjects[this.currentIndex];
            var yearBox = $(yearBoxSel).eq(-2);
            yearBox.find(subjectMatch(subjectName)).click();
            $(".item:contains('Hide subject (for just this student)')").click();
            this.afterLoad(function() {
                this.next();
            });
        }, true, subjects.length);
        this.afterChildIterator(function() {
            this.click("Close");
            this.afterLoad(function() {
                this.next();
            });
        }, subjectIter);
    });
}, true, students.length).start();

function subjectMatch(subjectName) {
    return subjectSel + ":contains(" + subjectName + ")";
}
