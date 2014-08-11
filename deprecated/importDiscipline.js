/** 
 * Import discipline data into the Discipline module.
 * 
 * Like other imports, the data passed to QSImporter should be formatted in an
 * array of incidents where the keys map to field names in the GUI, like so:
 * 
 *  [
 *      {
 *          "Incident Date": "05/19/2014",
 *          "Student": "Alvin DeSilva",
 *          "Reported By": "Mr. Teacher",
 *          "Incident Detail": "Was talking back.",
 *          "Response": "Detention",
 *          "Demerit Points": 1,
 *          "Action taken": "No action.",
 *      },
 *      {
 *          ...
 *      },
 *      ...
 *  ]
 */


new QSImporter.iterator(function() {
    this.click("Add Incident");
    var incident = this.item;
    $(".item .delete").click();
    for (var fieldName in incident) {
        QSIterator.setQPVal(fieldName, incident[fieldName]);
    }
    this.click("Add");
    this.afterLoad(this.next);
}).start();
