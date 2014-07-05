var links = document.getElementsByClassName('linkWidget');

var total = 0;
for (var i = 0; i < links.length; i++) {
	total += parseInt(links[i].innerText);
}

alert(total);