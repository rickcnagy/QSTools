new QSZeusIterator(function() {
	var iter = this;
    var childIter = new QSIterator("td[style='width: 411.84px; padding: 0px;'] tbody:first>tr", function() {
        if (this.currentIndex !== 0 && this.currentIndex !== this.elems.length - 1) {
    		var marks = this.elem.children("td:eq(1)").find("div");
    		var letterGrade = this.elem.children("td:eq(2)").find("div");
    		var hasMarks = marks.text().match(/\d/g) !== null;
            var marksFromLetter = gradeToMarks(letterGrade.text());
    		if (!hasMarks && !iter.setDefaultVal(marks) && marksFromLetter) {
    			marks.text(gradeToMarks(letterGrade.text()));
    			marks.blur();
    			openPreviewChangesRequests ++;
    		}
        }
    	this.afterLoad(function() {
    		this.next();
    	}, function() {
    		return openPreviewChangesRequests <= 0;
    	});
    });
    this.afterChildIterator(function() {
        this.pause();
    }, childIter);
}).start();


function gradeToMarks(grade) {
    var marks = 0;
	if (grade.match("A")) {
		marks = 95;
	} else if (grade.match("B")) {
		marks = 85;
	} else if (grade.match("C")) {
		marks = 75;
    } else if (grade.match("D")) {
		marks = 65;
	} else if (grade.match("F")) {
		marks = 55;
    }
    if (marks && grade.match("\\+")) {
        marks += 2.5;
    } else if (marks && grade.match("-")) {
        marks -= 2.5;
    }
    return marks;
}
