/** 
 * Export criteria from the Report Cards module.
 * 
 * Relies on the current template being Super Basic.
 * 
 * Data is exported in the import format from ./importCriteria.js, so an
 * export from here can be  imported back in using ./importCriteria.js
 */

var criteriaNameSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";
var criteriaValSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";
var dropdownStyle = "padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;";

var criteriaExport = new QSScraper();


new QSTableIterator(function() {    
    var altName = QSIterator.getQPVal("Alternative Subject Section Name");
    var criteriaTemplate = {
        "Template Name": QSIterator.getQPVal("Template Name"),
        "Alternative Subject Section Name": altName,
        "Criteria": []
    };
    
    $(criteriaNameSel).closest("tr").each(function() {
        var criteriaName = $(this).find(criteriaNameSel);
        var criteriaVal = $(this).find(criteriaValSel);
        if(isDropdown(criteriaVal)) {
            var dropdownDict = {};
            dropdownDict[criteriaName.text()] = criteriaVal.text();
            criteriaTemplate.Criteria.push(dropdownDict);
        } else {
            criteriaTemplate.Criteria.push(criteriaName.text());
        }
    });
    
    criteriaExport.add(criteriaTemplate);
    
    this.next(false);
}).onComplete(function() {
    criteriaExport.exportJSON("Criteria Export");
}).start();

function isDropdown(valDiv) {
    return valDiv.is("[style='" + dropdownStyle + "']");
}
