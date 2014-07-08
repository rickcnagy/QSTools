/**
 * Convert all dropdowns for a criteria to likert.
 * This maintains the value in each criteria, but makes what was a dropdown
 * into a likert.
 * This uses the grading scale from the first dropdown, so if there are multiple
 * grading scales in use that could be confusing.
 * First written for lapazschool (#32905).
 */


var scaleSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";
var currentScaleSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']:visible";
var likertScaleSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(153, 0, 0); text-align: center; min-height: 1em;']";
var criterionSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";

var iter = new QSIterator(".dataTableWidget:first .dttd:visible", function() {
    this.elem.click();
    this.afterLoad(function() {
        var optionVal = scale();
        var criteria = getCriteria();

        debugger;
        $(criterionSel).each(function() {
            QSIterator.clickHoverDelete($(criterionSel).eq(0));
        });

        criteria.forEach(function(criterion) {
            this.click("Add Likert");
            $(criterionSel).last().click()
                .text(criterion)
                .blur();
        }, this);

        $(likertScaleSel).click();
        this.afterLoad(function() {
            debugger;
            QSIterator.qpInputByLabel("Options").val(optionVal);
            this.click("Ok");
            this.click("Ok");
            this.afterLoad(this.next);
        });
    });
}).start();

function scale() {
    return $(currentScaleSel).first().text();
}

function getCriteria() {
    criteria = []
    $(criterionSel).each(function() {
        criteria.push($(this).text());
    });
    return criteria;
}
