noCreditSubjects = ['Music', 'Bible', 'Large Muscle Coordination', 'Math', 'Penmanship', 'Readiness in the Arts/Music', 'Reading/ Language Readiness', 'Small Muscle Coordination', 'Social Development', 'Work & Study Habits', 'Archery', 'US Chapel/Convocatio', 'Archery', 'US Chapel/Convocatio', 'Music', 'Music', 'Music', 'Study Hall', 'Archery', 'Study Hall', 'US Chapel/Convocatio', 'Music', 'Archery', 'US Chapel/Convocatio', 'Archery', 'Arrowsmith Program']

// find all the delete buttons
buttons = document.getElementsByClassName('buttonWidget allButtons');
buttonNum = -1;

var startRow = prompt('Start at which row?', '1');
if (startRow === null) throw new Error('Aborted JS');
buttonNum = parseInt(startRow) - 1

function editCreditHours() {
	buttonNum++;
	if (buttonNum % 20  == 0) if (!confirm("continue?")) throw new Error('Aborted JS');
	console.log(buttonNum)
	if (buttons[buttonNum].innerText === 'Edit') {
		buttons[buttonNum].click();
		
		var openEditDialog = setInterval(function() {
			console.log(isLoading());
			if (isLoading() === false) {
				clearInterval(openEditDialog);
				editSubjectDialog();
			}
		}, 500);
	} else editCreditHours();
}

function editSubjectDialog() {
	console.log('editSubjectDialog')
	// input widgets
	var creditField;
	var rows = document.getElementsByClassName('qpwRow')
	newCredits = .5;
	
	
	subjectName = rows[0].children[1].children[0].children[0].value;
	// check that it's not a 
	for (var i = 0; i < noCreditSubjects.length; i++) {
		if (subjectName.indexOf(noCreditSubjects[i]) >= 0) {
			newCredits = 0;
		}
	}
	
	// check the subject name
	if (subjectName.indexOf('Humanities') >= 0) {
		newCredits = 1;
	}
	
	
	// change the credits
	creditField = rows[2].children[1].children[0].children[0];
	creditField.value = newCredits.toString();
	
	setTimeout(function() {closeDialog()}, 200);
}

function closeDialog() {
	var bottomButtons = document.getElementsByClassName('ui-button-text');
	bottomButtons[0].click();
	var loadingInterval = setInterval(function() {
		if (!isLoading()) {
			clearInterval(loadingInterval);
			editCreditHours();
		}
	}, 100);
}

function isLoading() {
	if (document.getElementsByClassName('loadingWidget').length !== 0 || document.getElementsByClassName('loadingMessage centerText').length !== 0) return true;
	else return false;
}

editCreditHours();
