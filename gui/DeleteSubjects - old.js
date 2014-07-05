// 
//  DeleteSubjects.js
//  Rick Nagy
//  2014-03-04
// 

// Run via js console

javascript: buttons = document.getElementsByClassName('buttonWidget allButtons');
i = 0;

function deleteSubject() {
	i++;
	if (i % 100  == 0) if (!confirm("continue?")) return;
	
	if (buttons[i].innerText === 'Delete') {
		buttons[i].click();
		
		var bottomButtons = document.getElementsByClassName('ui-button-text');
		bottomButtons[0].click();
		
		var loadingInterval = setInterval(function() {
			if (!isLoading()) {
				clearInterval(loadingInterval);
				deleteSubject();
			}
		}, 100);
	} else deleteSubject();
}

function isLoading() {
	if (document.getElementsByClassName('loadingWidget').length !== 0) return true;
	else return false;
}

deleteSubject();
