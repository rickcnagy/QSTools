var iter = new QSGradebookIterator(function()
    this.click("Edit it anyways");
    this.click("Save");
});

iter.onComplete(function() {
    new Notification("Saved all gradebooks.");
});

iter.start();