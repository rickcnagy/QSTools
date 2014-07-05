new QSIterator("button:contains(Edit):visible", function() {
    this.elem.click();
    this.afterLoad(function() {
        var inputBox = $("tr:contains(Subject name) input");
        inputBox.val(inputBox.val().replace(/\[.*\]/g, ""));
        this.click("Ok");
    })    
}).start();
