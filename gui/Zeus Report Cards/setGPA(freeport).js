new QSZeusIterator(function() {
    var gpaBox = $("div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 8px; color: rgb(0, 0, 0); font-weight: bold; text-align: center; min-height: 1em;']:visible:eq(1)");
    this.setDefaultVal(gpaBox, function() {
        this.next();
    });
}).start();
