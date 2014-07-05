/*
 * Check that all the subjects have been hidden correctly - by number.
 */

var yearBoxSel = "td[style='width: 286px; padding: 0px;']";
var subjectNameSel = "td[style='width: 190.66666666666666px; padding: 0px 10px; border-right-width: 1px; border-right-style: solid; border-right-color: rgb(161, 0, 0);'] div";
var gradeSel = "td:nth-child(2)[style='width: 47.666666666666664px; padding: 0px; border-left-width: 1px; border-left-style: solid; border-left-color: rgb(161, 0, 0); border-right-width: 1px; border-right-style: solid; border-right-color: rgb(161, 0, 0);'] div";
var creditSel = "td:nth-child(3)[style='width: 47.666666666666664px; padding: 0px; border-left-width: 1px; border-left-style: solid; border-left-color: rgb(161, 0, 0); border-right-width: 1px; border-right-style: solid; border-right-color: rgb(161, 0, 0);'] div";
var students = QSImporter.data();

var iter = new QSIterator("*", function() {
    var student = students[this.currentIndex];
    console.log("Starting student", student);
    $(".dttd:contains(" + student.name + ")").click();
    this.afterLoad(function() {
        var yearBox = $(yearBoxSel).eq(-2);


        yearBox.find(subjectNameSel).filter(isBlank).each(function(i) {
            subjectName = student.subjects[i]["subject-name"];
            $(this).click();
            $(".item:contains(Edit subject name)").click();
            $(".dialogContent input").val(subjectName);
            iter.click("Ok");
        });

        /*
        yearBox.find(gradeSel).filter(isDash).each(function(i) {
            fillVal($(this), student.subjects[i]["letter-grade"]);
        });

        yearBox.find(creditSel).filter(isBlank).each(function(i) {
            fillVal($(this), student.subjects[i]["credit-earned"]);
        });
        */

        this.click("Save & Close");
        this.afterLoad(this.next);
    });
}, true, students.length);
iter.start();

function isBlank() {
    return $.trim(this.innerHTML) === "";
}

function isDash() {
    return $.trim(this.innerHTML) === "-";
}

function fillVal(elem, val) {
    elem.click();
    elem.text(val);
    elem.blur();
}

function enterSpace() {
    $(this).click();
    $(".item:contains(Edit subject name)").click();
    $(".dialogContent input").val(" ");
    iter.click("Ok");
}
