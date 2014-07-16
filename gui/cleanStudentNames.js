/**
 * Open up all student records and clean the student name, then trigger the
 * .keyup() method on the student name input to get the display name to
 * recalculate.
 *
 * Originally used for SacPrep (7/16/14) - (no ticket yet)
 */

new QSTableIterator(function() {
    var nameInput = QSIterator.qpInputByLabel("Name", true);
    var dirtyName = nameInput.val();
    var cleaned = dirtyName.replace(/\s+/g, ' ').trim();
    nameInput.val(cleaned).keyup();
    this.next();
}).start();
