var schoolRows = document.getElementsByClassName('dataTableContentRow')
var correctRow = null;

for (var index = 0; index < schoolRows.length; index++) {
	var text = schoolRows[index].children[1].children[0].children[0].textContent
	var codeStart = text.indexOf('[');
	var codeEnd = text.indexOf(']');
	var code = text.substr(codeStart + 1, codeEnd - codeStart - 1);
	if (code.toLowerCase() === 'ricknagy3'.toLowerCase()) correctRow = schoolRows[index];
	
	schoolCode = code;
}

var checkForDialog = function() {
	var length = document.getElementsByClassName('dialogContent')[0].children.length
	if (length != 0) {
		openSchool();
		return true;
	}
	else setTimeout(checkForDialog, 1000);
}

if (correctRow != null) {
	
	var superUserLink = correctRow.children[3].children[2].children[0];
	superUserLink.click();
	
	checkForDialog();
}

var openSchool = function() {
	var dialogContent = document.getElementsByClassName('dialogContent')[0].children
	var adminLink = dialogContent[8];
	adminLink.click();
	
	var adminEmail = dialogContent[17].children[0].textContent;
	
	adminEmailString = adminEmail.split(' - ')[1];
}