String.prototype.alpha = function() {
    return this.replace(/\s+/g, '');
};

var table = document.getElementsByClassName('dataTable alternating no-footer')[0];
var rows = table.children[1].children;
var allChecked = JSON.parse(prompt("JSON output"));

for (var i = 0; i < rows.length; i++) {
    var cells = rows[i].children;
    var studentName = cells[0].children[0].innerText.alpha();

    ref = findMatch(allChecked, studentName);
    if (ref) {
        setRow(cells, ref);
    } else {
        for (var a = 0; a < cells.length; a++) {
            setCheck(cells[a], false);
        }
    }
}

function setRow(cells, ref) {
    for (var j = 1; j < cells.length; j++) {
        setCheck(cells[j], ref.boxes[getColumnTitle(j)]);
    }
}

function findMatch(allChecked, studentName) {
    for (var j = 0; j < allChecked.length; j++) {
        if (allChecked[j].studentName === studentName) {
            return allChecked[j];
        }
    }
    return false;
}

function setCheck(cell, value) {
    cell.children[0].checked = value;
}

function getColumnTitle(cellIndex) {
    return table.children[0].children[0].children[cellIndex].innerText.alpha();
}