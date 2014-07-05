var averageBoxesSel = "tr:contains(AVERAGE) div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']:visible";
var otherBoxSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']:first";

var iterator = new QSZeusIterator(function() {
    this.setDefaultVal($(averageBoxesSel).eq(0), function() {
        this.setDefaultVal($(averageBoxesSel).eq(1), function() {
            this.setDefaultVal($(otherBoxSel), function() {
                this.afterLoad();
            })
        });
    });
});
iterator.onComplete(function() {
    new Notification("Iterator Complete");
})
iterator.start();
