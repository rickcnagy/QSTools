var links = document.getElementsByClassName('linkWidget');

var all = [];
for (var i = 0; i < links.length; i++) {
	all.push(parseInt(links[i].innerText));
}

open().document.write(all.join("<br>"));