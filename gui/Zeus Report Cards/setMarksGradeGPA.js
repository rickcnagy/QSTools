var finalMarksSel = "td[style='width: 33.3px; padding: 0px; border: 1px solid rgb(0, 129, 16); background: rgb(214, 248, 112);'] div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']:visible";
var finalGradeSel = "td:nth-last-child(1) div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(0, 0, 0); font-weight: bold; text-align: center; min-height: 1em;']";
var gpaSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 9px; color: rgb(8, 108, 162); font-weight: bold; text-align: center; min-height: 1em;']";

new QSZeusIterator(function() {
    var iter = this;
    var marksIter = new QSIterator(finalMarksSel, function() {
        iter.setZeusDefaultVal(this.elem, function() {
            marksIter.next();
        });
    });
    this.afterChildIterator(function() {
        var gradeIter = new QSIterator(finalGradeSel, function() {
            iter.setZeusDefaultVal(this.elem, function() {
                gradeIter.next();
            });
        })
        this.afterChildIterator(function() {
            var gpaIter = new QSIterator(gpaSel, function() {
                iter.setZeusDefaultVal(this.elem, function() {
                    gpaIter.next();
                })
            });
            this.afterChildIterator(function() {
                this.next();
            }, gpaIter);
        }, gradeIter);
    }, marksIter);
}).start();
