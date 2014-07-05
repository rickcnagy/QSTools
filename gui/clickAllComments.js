new QSIterator(".dataTableContentRow > :nth-child(2)", function() {
    this.elem.click();
    
    this.afterLoad(function() {
        $("div").filter(function() {
            return $(this).css("padding") == "0px 5px";
        }).children("div").click().blur();
        
        this.click("Save & Close");
        this.next();
    })
}).start();