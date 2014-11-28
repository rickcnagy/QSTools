/** 
 * Download all report cards from an old (pre-HTML5 session)
 * 
 * Any RC sessions from before HTML5 don't show up except through the student
 * profile. This allows for a mass export of rc's from a given session.
 * 
 * Be sure to "Allow site to download multiple files" when prompted.
 */

SESSION_NAME = "2010/2011 End-Of-Year (Grades 1-6)";


new QSTableIterator(function() {
    this.click("Reports");
    this.afterLoad(function() {
        $("span:contains(" + SESSION_NAME + ")")
            .closest("tr")
            .find(".smallDemotedButtonWidget:contains(View PDF)")
            .click();
        this.click("Ok");   // for unfinalized RC session popup
        this.next();
    });
}).setCloseButton("Close").start()
