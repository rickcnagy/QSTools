/** 
 * Download all report cards from an old (pre-HTML5 session)
 * 
 * Any RC sessions from before HTML5 don't show up except through the student
 * profile. This allows for a mass export of rc's from a given session.
 * 
 * Be sure to "Allow site to download multiple files" when prompted.
 * 
 * To download from all sessions visible in the student profile, set
 * SECTION_NAME to null, otherwise set it to a string of the section name.
 */

SESSION_NAME = null;


new QSTableIterator(function() {
    this.click("Reports");
    this.afterLoad(function() {
        if(SESSION_NAME != null) {
            var rows = $("span:contains(" + SESSION_NAME + ")").
                closest("tr");
        } else {
            var rows = $(".dataTable:contains(Grading Cycle) .dataTableContentRow");
        }
        rows.find(".smallDemotedButtonWidget:contains(View PDF)").
            click();
        this.click("Ok");   // for unfinalized RC session popup
        this.next();
    });
}).setCloseButton("Close").start()
