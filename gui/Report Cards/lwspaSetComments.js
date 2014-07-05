var commentsBoxSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: TimewNewRoman; font-size: 12px; color: rgb(0, 0, 1); min-height: 1em;'],div[style='padding-bottom: 0px; line-height: normal; font-family: TimewNewRoman; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";

new QSZeusIterator(function() {
    var zIter = this;
    var commentIter = new QSIterator(commentsBoxSel, function() {
        this.elem.click();
        this.elem.blur();
        zIter.registerZeusChange();
        zIter.afterZeusLoad(function() {
            commentIter.next();
        })
    });
    this.afterChildIterator(this.next, commentIter);
}).start();
