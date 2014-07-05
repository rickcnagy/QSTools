enrollmentChanges = getInput();

var i = 0;
new QSIterator("div:first", function() {
    var change = enrollmentChanges[i];
    i ++;
    if (typeof change["Students to Unenroll"] === "string") {
        change["Students to Unenroll"] = change["Students to Unenroll"].split(" | ");
        change["Students to Enroll"] = change["Students to Enroll"].split(" | ");   
    }
    
    var row = $("tr:contains(" + change["Course Name"] +
        "):contains(" + change["Course Grade Level"] +
        "):contains(" + change["Course Teacher(s)"] + ")");
    if (row.length !== 1) {
        debugger;
        console.warn("Couldn't find match", change);
        alert("Problem - couldn't find match");
    }
    row.find(".linkWidget").click();
    this.afterLoad(function() {
        if (change["Students to Unenroll"][0] !== "") {
            change["Students to Unenroll"].forEach(function(student) {
                $(".dataTableContentRow:contains(" + student + ")").find("button").click();
            }, this);
        }
        $(".easySelectorWidget input").click();
        this.afterLoad(function() {
            if (change["Students to Enroll"][0] !== "") {
                change["Students to Enroll"].forEach(function(student) {
                    $(".easySelectorWidget li:contains(" + student + ")").click();
                }, this);
            }
            this.click("Save");
        });
    });
}, true, enrollmentChanges.length).start();

function getInput() {
    return JSON.parse(prompt("JSON input"));
}
