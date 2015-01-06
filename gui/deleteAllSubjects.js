/**
 * Delete all subjects visible on the Global Subject Setup screen.
 *
 * TODO: handle non-zero enrollment
 */

var qsIterator = new QSIterator(".buttonWidget:contains(Delete)", function() {
    this.elem.click();
    this.click("Yes, delete");
    this.afterLoad(this.next);
}, true);

qsIterator.start();
