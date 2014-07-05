// 
//  importApplicants.js
//  Rick Nagy
//  2014-04-14
// 

// run via js console

function main() {
    stopAsap = false;
    $(window).keypress(function(e) {
        if (e.which === 3) {
            stopAsap = true;
        }
    });
    addNextApplicant(getApplicants());
}

function addNextApplicant(applicants) {
    $( ".quickAddButtonWidget:contains('Add Student Application')" ).first().click();
    afterLoad(setInputValues, applicants);
}

function setInputValues(applicants) {
    applicant = applicants[0];
    setInputVal("Student Full Name", applicant.Name);
    setInputVal("Father's Name", applicant['Fathers Name']);
    setInputVal("Residential address", applicant.Address);
    setInputVal("City", applicant.City);
    setInputVal("State", applicant.State);
    setInputVal("ZIP code", applicant.Zip);
    setInputVal("Home Phone", applicant.Home);
    setInputVal("Cell phone", applicant.Cell);
    setInputVal("Email", applicant.Email);
    setInputVal("Language", applicant.Language);
    setInputVal("Note", applicant.Note);
    setInputVal("Application remarks", applicant.Decision);
    setInputVal("Misc Note", applicant['Misc Note']);
    setInputVal("Misc Note 2", applicant['Misc Notes 2']);
    setInputVal("Application Date", applicant['Application Date'])
    setInputVal("Birth date", applicant['D O B']);
    setDropdownVal("Category", applicant.Category);
    setDropdownVal("Application Status", "Waiting List")
    clickSave(applicants);
}

function clickSave(applicants) {
    $( ".emphasizedButtonWidget:contains('Save'):first" ).click();
    applicants.shift();
    afterLoad(addNextApplicant, applicants);
}

function getApplicants() {
    if (typeof applicantsJSON === 'undefined') {
        applicantsJSON = JSON.parse(prompt('Applicants JSON?'));
    }
    return applicantsJSON.slice(0);
}

function setInputVal(labelText, value) {
    var input = getInput(labelText);
    input.val(value);
    input.change();
}

function setDropdownVal(labelText, value) {
    var dropdown = getDropdown(labelText);
    dropdown.val(value);
    dropdown.change();
}

function getDropdown(labelText) {
    return tableValue(labelText)
        .children()
        .andSelf()
        .filter( ".dropDownWidget" )
        .children();
}

function getInput(labelText) {
    return tableValue(labelText)
        .children()
        .andSelf()
        .filter( ".inputBox" )
        .children()
}

function tableValue(labelText) {
    return $( ".tableLabel:contains('" + labelText + "')" )
        .next(); 
}

function quit() {
    while ($( "*:contains('Close')" ).length > 0) {
        $( "*:contains('Close'):last" ).click();
    }
    throw new Error("Aborted JS");
}

function afterLoad(callback, param) {
    if (stopAsap) quit();
    else {
        var loading = setInterval(function() {
            if ($( "*[class^='load']:not('.ribbonSelectorWidget *'):visible" ).length === 0) {
                clearInterval(loading);
                callback(param);
            }
        }, 10, param);
    }
}

main();