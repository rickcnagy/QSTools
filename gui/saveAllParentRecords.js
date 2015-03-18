/**
 * Open up all student records and then open all parents and save them.
 *
 * This doesn't actually resave the students, just the parents inside the
 * students.
 *
 * At this point, parents are saved once per siblings, so often many times.
 *
 * This requires parent cards be on.
 */

var studentIter = new QSTableIterator(function() {
    var parentIterForStudent = new QSIterator(".parentCardEdit", function() {
        this.elem.click();
        this.afterLoad(function() {
            this.click("Save");
            this.afterLoad(this.next);
        });
    });

    this.afterChildIterator(this.next, parentIterForStudent);
});

studentIter.setCloseButton("Close");
studentIter.start();
