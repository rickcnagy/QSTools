new QSZeusIterator(function() {
	var iter = this;
    var childIter = new QSIterator("td[style='width: 411.84px; padding: 0px;'] tbody:first>tr", function() {
        if (this.currentIndex !== 0 && this.currentIndex !== this.elems.length - 1) {

    		var marks = this.elem.children("td:eq(1)").find("div");
    		var letterGrade = this.elem.children("td:eq(2)").find("div");
    		var hasMarks = marks.text().match(/\d/g) !== null;
    		if (!hasMarks && !iter.setDefaultVal(marks)) {
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
        var studentName = $("div[style='padding-bottom: 0px; line-height: normal; font-family: ProximaNovaBold; font-size: 12px; color: rgb(0, 0, 0); min-height: 1em;']:first");
        studentName.text(studentName.text());
        studentName.blur();
        openPreviewChangesRequests ++;
        this.afterLoad(function() {
            this.next();
        }, function() {
            return openPreviewChangesRequests <= 0;
        });
    }, childIter);
}).start();


function gradeToMarks(grade) {
	if (grade.match("A")) {
		return 95;
	} else if (grade.match("B")) {
		return 85;
	} else if (grade.match("C")) {
		return 75;
	} else if (grade.match("F")) {
		return 65;
	} else if (grade.match("E")) {
	    return 92.5;
	} else if (grade.match("S")) {
	    return 77.5;
	} else if (grade.match("U")) {
	    return 62.5;
	}
	return "";
}
