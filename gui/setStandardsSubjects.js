var standardsIter = new QSTableIterator(function() {
    $('box inputBox').each(function(){
        this.click();
            this.afterLoad(function(){
                this.click('2nd Grade');
            })
    })
    this.next();
});

standardsIter.setCloseButton("Update");
standardsIter.start();


/*
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
*/