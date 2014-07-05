String.prototype.alpha = function() {
    return this.replace(/\s+/g, '');
};

var table = document.getElementsByClassName('dataTable alternating no-footer')[0];
var rows = table.children[1].children;
var allChecked = [];
for (var i = 0; i < rows.length; i++) {
    var cells = rows[i].children;
    allChecked.push(new Row(cells[0].children[0].innerText.alpha()));
    for (var j = 1; j < cells.length; j++) {
        checked = cells[j].children[0].checked;
        allChecked[allChecked.length - 1].boxes[getColumnTitle(j)] = checked;
    }
}

open().document.write(JSON.stringify(allChecked));


function Row(studentName) {
    this.studentName = studentName.alpha();
    this.boxes = {};
}

function getColumnTitle(cellIndex) {
    return table.children[0].children[0].children[cellIndex].innerText.alpha();
}