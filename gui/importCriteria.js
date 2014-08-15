/** 
 * Import criteria into the Report Cards module.
 * 
 * Relies on the current template being Super Basic.
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

var criteriaNameSel = "div:contains(Subject-Specific Criteria)[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";
var criteriaValSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";


new QSImporter.iterator(function() {
    this.click("Add Subject Template");
    this.afterLoad(function() {
        var alt = "Alternative Subject Section Name";
        QSIterator.setQPVal("Template Name", this.item["Template Name"]);
        QSIterator.setQPVal(alt, this.item[alt]);
        
        var criteriaIter = new QSImporter.iterator(function() {
            var isDropdown = typeof this.item !== "string";
            var criteriaName = this.item;
            if (isDropdown) {
                criteriaName = Object.keys(this.item)[0];
                var dropdownVal = this.item[criteriaName];    
            }

            this.click(isDropdown ? "Add Drop Down" : "Add Field");
            $(criteriaNameSel).text(criteriaName).blur();

            if (isDropdown) {
                var emptyCriteriaVal = $(criteriaValSel).filter(function() {
                    return $.trim($(this).text()) === "";
                });
                if (emptyCriteriaVal.length !== 1) {
                    console.error("too many 'empty' criteria vals found", emptyCriteriaVal)
                    this.quit();
                } else {
                    emptyCriteriaVal.click();
                    this.afterLoad(function() {
                        $("select").val(dropdownVal);
                        this.click("Ok");
                        this.next();
                    });
                }
            }
        }, this.item["Criteria"]);
        
        this.afterChildIterator(function() {
            this.click("Ok");
            this.next();
        }, criteriaIter);
    });
}).start();
