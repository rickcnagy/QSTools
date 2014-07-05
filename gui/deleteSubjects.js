/**
 * Delete all subjects visible on the screen. Includes clearing enrollment.
 */

var iter = new QSIterator(".dttd .linkWidget", function() {
    if (this.elem.text() !== "0") {
        this.elem.click();
        this.afterLoad(function() {
            this.clickAll("X");
            this.click("Save");
        });
    }
});
iter.onComplete(function() {
    new QSIterator(".dttd .buttonWidget:contains(Delete)", function() {
        this.elem.click();
        this.click("Yes, delete");
    }, true).start();
})
iter.start();
