//
//  intvlaTranscriptExport.js
//  Rick Nagy
//  2014-05-22
//

var iterator = new QSTableIterator(function() {
    studentName = $(".recordHeaderWidget h1").text();
    iterator = this;

    var yearBoxSel = ".paperWidget td[style='width: 555px; padding: 0px;']";
    var classNameSel = "td[style='width: 475.7142857142857px; padding: 2px 10px; border-left-width: 1px; border-left-style: solid; border-left-color: rgb(0, 0, 0); border-top-width: 1px; border-top-style: solid; border-top-color: rgb(0, 0, 0); border-bottom-width: 1px; border-bottom-style: solid; border-bottom-color: rgb(0, 0, 0); background: rgb(200, 200, 200);']";
    var yearNameSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Verdana; font-size: 9px; color: rgb(0, 0, 0); text-align: right; min-height: 1em;']:eq(1)";
    var subjectNameSel = "td[style='width: 317.14285714285717px; padding: 0px; border-left-width: 1px; border-left-style: solid; border-left-color: rgb(0, 0, 0);']";

    $(yearBoxSel).each(function() {
        var className = $(this).find(classNameSel).text();
        // for 5th Grade --> 5th Grade
        className = (/for (.+)/g).exec(className)
        if (!className) return false;

        className = className[1]
        var yearName = $(this).find(yearNameSel).text();

        $(this).find(subjectNameSel).each(function() {
            var subjectName = $(this);
            var gradeName = $(this).next();
            var credits = gradeName.next();
            var earned = credits.next();

            iterator.scraper.add({
                "Student Name": studentName,
                "Year Name": yearName,
                "Class Name": className,
                "Subject Name": subjectName.text(),
                "Letter Grade": gradeName.text(),
                "Credits": credits.text(),
                "Earned": earned.text()
            });
        });
    });
    this.next();
});
iterator.scraper = new QSScraper();
iterator.scraper.setExportKeys([
    "Student Name",
    "Year Name",
    "Class Name",
    "Subject Name",
    "Letter Grade",
    "Credits",
    "Earned"
]);
iterator.onComplete(function() {
    this.scraper.export("INTVLA Transcripts")
});
iterator.setCloseButton("Close");
iterator.start();
