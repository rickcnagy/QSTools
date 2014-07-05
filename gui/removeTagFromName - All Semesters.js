new QSIterator("tr:contains(Semester) .dropDownWidget select option", function() {
     $("tr:contains(Semester) .dropDownWidget select")
         .val(this.elem.text())
         .change();
     this.afterLoad(function() {
         var innerDone = false;
         var innerIter = new QSIterator("button:contains(Edit):visible", function() {
             this.elem.click();
             this.afterLoad(function() {
                 var inputBox = $("tr:contains(Subject name) input");
                 inputBox.val(inputBox.val().replace(/\[.*\]/g, ""));
                 this.click("Ok");
             })    
         });
         innerIter.onComplete(function() {
             innerDone = true;
         });
         this.afterLoad(undefined, undefined, function() {
             return innerDone;
         });
         innerIter.start();  
     })
}).start();
