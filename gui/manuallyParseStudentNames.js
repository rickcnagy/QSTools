/** 
 * Parse full names on the Students module and manually set First, MI, Last.
 * This is an alternative to simply triggering the blur() event on the name
 * field, when for some reason that isn't working.
 * 
 * This parses full names like "Jobs, Steve P.", but the regex could be adapted
 * to fit whatever format the full name is currently in.
 */


var nameRegex = /([\w' -]+)[,|.]* ([\w'-]+)( ([\w' -]+).*)*/;

new QSTableIterator(function() {
    var studentName = $(".recordHeaderWidget").find("h1").text();
    var match = nameRegex.exec(studentName);
    console.log(match);

    function setText(elem, text) {
        elem.val(text).change().blur();
    }

    if (match) {     
        var nameBoxes = QSIterator.qpInputByLabel("Name", null, true);
        setText(nameBoxes.eq(0), match[1]);
        //setText(nameBoxes.eq(1), match[4]);
        setText(nameBoxes.eq(2), match[2]);
    }
    this.click("Save");
    if (this.click("Ok")) {
        this.click("Close");
        this.click("Navigate away");
    }
    this.next();
}).start();
