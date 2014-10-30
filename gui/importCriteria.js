/** 
 * Import criteria into the Report Cards module.
 * 
 * Relies on the current template being Super Basic.
 * 
 * If a subject template is found with the same name as the one being imported:
 *      - the criteria for that template will be added to the matched one.
 *      - The alternative subject section name will be updated to the one from
 *          the import.
 *      - If individual criteria are found that have the same value as the one
 *          being imported, those will be deleted and re-added if the type is
 *          different (i.e. one is adropdown and one is a field).
 * 
 * QSImporter should have an object like this:
 * [
 *     {
 *         "Template Name": "Reading 3-5",
 *         "Alternative Subject Section Name": "Reading",
 *         "Criteria": [
 *             {"Criteria Name": "A,B,C,D,F"}, // dropdown
 *             "Criteria Name", // field
 *             ...
 *         ]
 *     },
 *     ...
 * ]
 */

var criteriaNameSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";
var criteriaValSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";


new QSImporter.iterator(function() {
    var rowSel = ".dataTableWidget:first .dttd:last-child:visible:contains(" + this.item["Template Name"] + ")";
    
    if($(rowSel).length) {
        $(rowSel).first().click();
    } else {
        this.click("Add Subject Template");
    }

    this.afterLoad(function() {
        var alt = "Alternative Subject Section Name";
        QSIterator.setQPVal("Template Name", this.item["Template Name"]);
        QSIterator.setQPVal(alt, this.item[alt]);
        
        var criteriaIter = new QSImporter.iterator(function() {
            var isDropdown = typeof this.item !== "string";
            var criteriaName = this.item;
            if(isDropdown) {
                criteriaName = Object.keys(this.item)[0];
                var dropdownVal = this.item[criteriaName];    
            }
            
            var existingCriteria = $(criteriaNameSel + ":contains(" + criteriaName + ")");
            if(existingCriteria.length) {
                QSIterator.clickHoverDelete(existingCriteria);
            }
            addCriteria.call(this, criteriaName, isDropdown, dropdownVal)
        }, this.item.Criteria);
        
        this.afterChildIterator(function() {
            this.click("Ok");
            this.next();
        }, criteriaIter);
    });
}).start();


function addCriteria(criteriaName, isDropdown, dropdownVal) {
    this.click(isDropdown ? "Add Drop Down" : "Add Field");
    
    var emptyName = $(criteriaNameSel + ":contains(Subject-Specific Criteria)");
    if(emptyName.length !== 1) {
        console.error("too many 'empty' criteria vals found", emptyCriteriaVal);
        this.quit();
        return;
    }
    
    emptyName.text(criteriaName).blur();
    
    if(isDropdown) {
        emptyName.closest("tr").find(criteriaValSel).click();
        this.afterLoad(function() {
            $("select").val(dropdownVal);
            this.click("Ok");
            this.next();
        });
    } else {
        this.next();
    }
}
