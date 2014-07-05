// get all the edit buttons
links = document.getElementsByClassName('linkWidget')

i = -1;
function clickEdit() {
	i++;
	if (i % 20  == 0) if (!confirm("continue?")) return;
	
	if (links[i].innerText !== '0') {
		// click edit buttons
		links[i].click();
		// wait until the loadingWidget disappears, then click all the x buttons
		var loadingInterval = setInterval(function() {
			if (!isLoading()) {
				clearInterval(loadingInterval)
				clearEnrollments();
			};
		}, 100);

		// save and do the next one
	} else clickEdit();
}

function isLoading() {
	if (document.getElementsByClassName('loadingWidget').length !== 0) return true;
	else return false;
}

function clearEnrollments() {
	var allButtons = document.getElementsByClassName('buttonWidget allButtons');
	var unenrollButtons = [];
	for (var i = 0; i < allButtons.length; i++) {
		if (allButtons[i].innerText === 'X')
			unenrollButtons.push(allButtons[i]);
	}
	if (unenrollButtons.length > 0) {
		unenrollButtons[0].click();
		clearEnrollments();
	} else {
		var bottomButtons = document.getElementsByClassName('ui-button-text');
		bottomButtons[0].click();
		var loadingInterval = setInterval(function() {
			if (!isLoading()) {
				clearInterval(loadingInterval)
				clickEdit();
			};
		}, 100);
	}
}

clickEdit();