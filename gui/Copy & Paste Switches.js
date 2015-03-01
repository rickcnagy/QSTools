/**
 * Copy & Paste switches between Zeus templates.
 * #TODO: move to qs-supporttools
 */

var switches = [];
$(".easySelectorWidget span").each(function() {
    switches.push($(this).text());
});

$(".resultsHolder li").each(function() {
    if (switches.indexOf($(this).text()) > -1) {
        $(this).click();
    }
});
