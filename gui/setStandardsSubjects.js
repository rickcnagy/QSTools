var standardsIter = new QSTableIterator(function() {
    var name = QSIterator.getQPVal("Name");

    if(name.match(/^GR/)) {
        var gradeNumber = name.match(/^[a-zA-Z]*(\d)/)[1];
    } else {
        var gradeNumber = name.match(/^(\w+) /)[1];
    
            if (gradeNumber == "TK"){
                gradeNumber = "Transitional Kindergarten";
            } else {
                gradeNumber = "Kindergarten";
            }
    }

    var subjectName = name.match(/ - (.+)/)[1];

    QSIterator.setQPVal("Grade level", gradeNumber);
    setTimeout(function() {
        QSIterator.setQPVal("Subjects", subjectName);

        this.next();
    }.bind(this), 1000);
});

standardsIter.setCloseButton("Update");
standardsIter.start();
