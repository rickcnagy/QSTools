var iter = new QSZeusIterator(function() {
    var studentName = $(".recordHeaderWidget h1").text();
    var iter = this;
    $("td[style='width: 811.9999999999999px; padding: 0px;']").each(function() {
        var subjectName = $(this).find("div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 11px; color: rgb(0, 0, 0); font-weight: bold;']").text();
        $(this).find("div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 11px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']:even").each(function() {
            iter.scraper.add({
                "Student Name": studentName,
                "Subject Name": subjectName,
                "Final Year Grade": $(this).text()
            });
        });
    });
    this.next();
});
iter.scraper = new QSScraper([
    "Student Name",
    "Subject Name",
    "Final Year Grade"
]);
iter.onComplete(function() {
    this.scraper.export("ISOM Final Grades 2014");
});
iter.start();
