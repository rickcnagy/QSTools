function replace(elem, oldText, newText) {
    var html = $(elem).html();
    if (html.indexOf(oldText) > -1) {
        $(elem).html(html.replace(oldText, newText));
    }
}


$("#main_panes span,a").each(function() { 
    replace(this, "Open Tickets older than 60 days", "Cold Cases");
    replace(this, "Tickets", "Mysteries");
    replace(this, "Ticket", "Mystery");
    replace(this, "tickets", "mysteries");
    replace(this, "ticket", "mystery");
})
