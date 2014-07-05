// 
//  SaveAllGradebooks.js
//  Rick Nagy
//  2014-03-06
// 

// run via js console

currentTeacher = 0;
currentSection = 0;

validSections = "Rolling"

function nextTeacher() {
    findElements();
    if (currentTeacher >= teacherDropdown.prop("length")) {
        throw new Error("All done!");
    } else {
        teacherDropdown.prop("selectedIndex", currentTeacher);
        teacherDropdown.change();
    
        afterLoad(function() {
            currentSection = 0;
            currentTeacher++;
            nextSection();
        });
    }
}

function nextSection() {
    editAnyways();    
    findElements();
    if (currentSection >= sectionDropdown.prop("length")) {
        nextTeacher();
    } else {        
        if (nextIsValidSection()) {
            sectionDropdown.prop("selectedIndex", currentSection);
            sectionDropdown.change();
            afterLoad(function() {
                currentSection++;
                save(nextSection);
            });
        } else {
            currentSection++;
            nextSection();
        }
    }
}

function nextIsValidSection() {
    var nextText = sectionDropdown.children()[currentSection].innerText;
    return (validSections === "" || nextText.indexOf(validSections) > -1);
}

// for when editing from a nonactive semester
function editAnyways() {
    if ($(".linkWidget").first().prop("innerText") === "Edit it anyways.") {
        $(".linkWidget").first().click();
    }
}

function findElements() {
    teacherDropdown = $(".dropDownWidget").first().children()
    sectionDropdown = $(".dropDownWidget").last().children()
    saveButton = document.getElementsByClassName("emphasizedButtonWidget allButtons")[0]
}

function save(callback) {
    findElements();
    saveButton.click();
    
    if (callback !== undefined) {
        afterLoad(function() {
            callback();
        });
    }
}


function afterLoad(callback) {
	var waitingForLoad = setInterval(function() {
		if (!isLoading()) {
			clearInterval(waitingForLoad);
			callback();
		}
	}, 100, callback);
}

function isLoading() {
	if (document.getElementsByClassName('loadingWidget').length !== 0
		|| document.getElementsByClassName('loadingMessage centerText').length !== 0) {
		return true;
	} else return false;
}

nextTeacher();