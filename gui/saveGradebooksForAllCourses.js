/** 
 * Save all student records visible in the Students module and trigger the
 * blur() event on the full name field to update the name separation. For more
 * fine-grain control over the parsing, see ./manuallyParseStudentNames.js.
 */


new QSTableIterator(function() {
    this.click("Save");
    this.next();
}).start();