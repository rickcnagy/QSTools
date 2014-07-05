var DELIMETER = '/-/';

var input = prompt().split(DELIMETER);
var table = document.getElementsByClassName('dataTable alternating no-footer')[0];
var rows = table.children[1].children;
var names = [];
for (var i = 0; i < rows.length; i++) {
    names.push(rows[i].innerText.trim());
}

if (input.length === 1) {
    prompt('', names.join(DELIMETER));
} else {
    alert(equal(input, names));
}

function equal(input, current) {
    console.log(input);
    console.log(current);
    if (input.length !== current.length) return false;
    
    for (var i = 0; i < current.length; i++) {
        if (current[i] !== input[i]) return false;
    }
    
    return true;
}
