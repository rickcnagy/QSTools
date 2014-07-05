new QSGradebookIterator(function() {
    if ($(".formulaColumn").length) return;
    debugger;
    this.click("Edit it anyways")
    this.click("Add Formula");
    this.click("Assignment")
    $("tr.category:contains(Assignment) input").click()
    this.click("Add");
    this.click("Save");
}).start();
