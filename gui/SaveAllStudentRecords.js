// 
//  OpenAndSaveStudentRecords.js
//  Console JavaScript
//  
//  Created by Rick Nagy on 2014-01-27.
// 
//  This will go down the student list in the Students module and click and save each student
//
//	set TRIGGER_KEYUP to true to also trigger the keyUp() method in the name field
//		this is useful for triggering the name parser, which is useful
//		for refactoring student names - Rick Nagy can go to Nagy, Rick
//

TRIGGER_KEYUP = false;
COLUMN_COUNT = document.getElementsByClassName("dataTableContentRow")[0].children.length

i = 1 - COLUMN_COUNT;

var startRow = prompt('Start at which row?', '1');
if (startRow === null) throw new Error('Aborted JS');
buttonNum = parseInt(startRow) - COLUMN_COUNT

studentRows = document.getElementsByClassName('dttd')

function openNextProfile() {
	i += COLUMN_COUNT;
	if ((i - 1) % (COLUMN_COUNT * 100) == 0) {
		if (!confirm("continue?")) throw new Error('Aborted JS');
	} else if (i > studentRows.length) {
		throw new Error('Complete. Saved ' + (i + 3) / COLUMN_COUNT + ' profiles')
	}
	
	studentRows[i].click();
	if (TRIGGER_KEYUP) afterLoad(triggerKeyup)
	else afterLoad(closeProfile);
}

function triggerKeyup() {
	var input = document.getElementsByClassName('inputFieldWidget inputBox')[0].children[0]
	$('input').keyup();
	closeProfile();
}

function closeProfile() {
	document.getElementsByClassName("emphasizedButtonWidget allButtons")[0].click();
	console.log("saving row " + (i + 3) / COLUMN_COUNT )
	afterLoad(openNextProfile);
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

openNextProfile();
