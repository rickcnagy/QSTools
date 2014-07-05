/*
 * Check that all the subjects have been hidden correctly - by number.
 */

var yearHeaderBoxSel = "td[style='width: 286px; padding: 0px;']:last div:first";
var students = QSImporter.data();

correctCount = 0;
new QSIterator("*", function() {
    var student = students[this.currentIndex];
    $(".dttd:contains(" + student.Name + ")").click();
    this.afterLoad(function() {
        var subjects = student.Subjects;
        $(yearHeaderBoxSel).click();
        $(".item:contains(Show hidden subjects)").click();

        var hiddenCount = $(".dialogContent .linkWidget").length;
        if (hiddenCount !== subjects.length) {
            alert("Problem!")
            console.error("Incorrect hidden subject length", student)
        } else {
            correctCount ++;
            console.log("Student correct", student);
        }
        console.log("Correct count", correctCount)

        this.click("Done");
        this.click("Close");
        this.afterLoad(function() {
            this.next();
        });
    });
}, true, students.length).start();
