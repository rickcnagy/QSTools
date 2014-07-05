// javascript:var%20iter%20=%20new%20QSIterator(%22.dttd%20.linkWidget%22,%20function()%20{debugger;if%20(this.elem.text()%20!==%20%220%22)%20{this.elem.click();this.afterLoad(function()%20{this.clickAll(%22X%22);this.click(%22Save%22);});}});iter.onComplete(function()%20{open(%22https://www.youtube.com/watch?v=iNpXCzaWW1s%22);});iter.start();
var iter = new QSIterator(".dttd .linkWidget", function() {
    debugger;
    if (this.elem.text() !== "0") {
        this.elem.click();
        this.afterLoad(function() {
            this.clickAll("X");
            this.click("Save");
        });
    }
});
iter.onComplete(function() {
    open("https://www.youtube.com/watch?v=iNpXCzaWW1s");
});
iter.start();
