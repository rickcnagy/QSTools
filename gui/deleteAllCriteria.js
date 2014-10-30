/**
 * Delete all criteria in the subject-specific criteria screen.
 */


new QSIterator("*", function() {
    $(".dataTableWidget:first .dttd:first").click();
    this.afterLoad(function() {
        this.click("Delete");
        this.next();
    });
}, true, $(".dataTableWidget:first .dttd").length).start();
