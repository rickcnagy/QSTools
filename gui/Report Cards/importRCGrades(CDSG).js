var MARKS_SEL = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";
var GRADE_SEL = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); font-weight: bold; text-align: center; min-height: 1em;']";
var AVG_SEL = "td[style='width: 185px; padding: 0px; border: 1px solid rgb(0, 0, 0); background: rgb(215, 223, 238);'] div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";

var tree = QSImporter.data();
var students = Object.keys(tree);

new QSZeusIterator(function() {
    var topChild = new QSIterator("div", function() {
        var studentName = students[this.currentIndex];
        $(".dataTableContentRow:contains(" + studentName + ") .dttd:eq(1)").click();
        this.afterLoad(function() {
            var subjects = Object.keys(tree[studentName]);
            var headerRow = $("table[style='width: 100%;']:contains(Mark):first");

            var child = new QSIterator("div", function() {
                // debugger;
                var subjectName = subjects[this.currentIndex];
                var marks = tree[studentName][subjectName];
                var mark = marks["Q1"];

                var subjectRow = headerRow.siblings("table:contains(" + subjectName + ")");
                var marksBox = subjectRow.find(MARKS_SEL);
                marksBox.text(mark).blur();
                var iter = this;
                setTimeout(function() {
                    var gradeBox = subjectRow.find(GRADE_SEL);
                    gradeBox.text(gradeFromMarks(mark)).blur();
                    setTimeout(function() {
                        iter.next();
                    }, 1000);
                }, 1000)
            }, true, subjects.length);
            this.afterChildIterator(function() {
                QSZeusIterator.prototype.setDefaultVal.call(this, $(AVG_SEL), function() {
                    this.click("Save & Close");
                    this.afterLoad(function() {
                        this.next();
                    });
                })
            }, child);
        });
    }, true, students.length);
    topChild.isChild = false;
    this.afterChildIterator(function() {
        this.quit();
    }, topChild);
}).start();

function gradeFromMarks(marks) {
    grade = "I";
    if (marks >= 90) {
        grade = "A";
    } else if (marks >= 80) {
        grade = "B";
    } else if (marks >= 70) {
        grade = "C";
    } else if (marks >= 60) {
        grade = "D";
    } else if (marks > 0) {
        grade = "F";
    }
    return grade;
}
