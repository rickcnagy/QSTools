/**
 * Convert Likerts to dropdowns.
 * This maintains the value in each criteria, but makes what was a likert value
 * into a drop down.
 * This requires that ALL criteria in each criteria set is a Likert.
 * First written for lapazschool (#32879).
 */

var criteriaSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";
var scaleSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); text-align: center; min-height: 1em;']";
var currentScaleSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(153, 0, 0); text-align: center; min-height: 1em;']:visible";
var criterionSel = "div[style='padding-bottom: 0px; line-height: normal; font-family: Arial; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']";

var iter = new QSIterator(".dataTableWidget:first .dttd:visible", function() {
    this.elem.click();
    this.afterLoad(function() {
        var optionVal = scale();
        var criteria = getCriteria();

        debugger;
        $(criteriaSel).each(function(i) {
            QSIterator.clickHoverDelete($(criteriaSel).eq(0));
        });

        var criteriaIter = new QSIterator("*", function() {
            criterion = criteria[this.currentIndex];
            this.click("Add Drop Down");
            debugger;
            $(criteriaSel).last().click()
                .text(criterion)
                .blur();
            $(scaleSel).last().click();
            this.afterLoad(function() {
                QSIterator.qpInputByLabel("Options").val(optionVal);
                this.click("Ok");
                this.next();
            });
        }, true, criteria.length);

        this.afterChildIterator(function() {
            this.click("Ok");
            this.afterLoad(this.next);
        }, criteriaIter);
    });
}).start();

function scale() {
    return $(currentScaleSel).text();
}

function getCriteria() {
    criteria = []
    $(criterionSel).each(function() {
        criteria.push($(this).text());
    });
    return criteria;
}
