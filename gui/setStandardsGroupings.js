// See examples/setStandardsGroupings.example.json

new QSImporter.iterator(function() {
	var regex = new RegExp("^" + this.item["Name"] + "\W");
	$("tr").filter(function() {
		return regex.test($(this).text());
	}).find("button:contains(Edit):last").click();

    this.afterLoad(function() {
        var groupingCreator = new QSImporter.iterator(function(grouping) {
            this.click("Add Group");

            QSIterator.setQPVal("Name", this.item["Name"]);
            QSIterator.setQPVal("Sort Order", this.item["Sort Order"]);

            QSIterator.setCheckBoxVal("Is Active", this.item["Is Active"]);
            QSIterator.setCheckBoxVal("Show Header in Report Card", this.item["Show Header in Report Card"]);

            var selectedStandards = this.item["Selected Standards"];
            for(var i = 0; i < selectedStandards.length; i++) {
                var selectedStandard = selectedStandards[i];

                QSIterator.setQPVal("Add Standard", selectedStandard);
            }

            this.click("Add");

            this.next();
        }, this.item["Groupings"]);


        this.afterChildIterator(function() {
            this.click("Ok");
            this.next();
        }, groupingCreator);
    });
}).start();