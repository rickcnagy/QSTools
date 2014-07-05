new QSZeusIterator(function() {
    this.setCloseButton("Close");
    if ($("div.pre-wrap:visible").text().indexOf("*Couldn't find all CJSF eligible subjects, please contact support.*") > -1) {
         this.pause("Found one");   
         alert("Found one");
    }
}).start();

