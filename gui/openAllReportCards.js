/**
 * Opens all report cards, but doesn't save.
 *
 * This can be useful to recalculate JavaSnippets.
 */

var iter = new QSTableIterator(function(){
	this.next();
});

iter.setCloseButton(["Close", "Back to list"]);
iter.start();
