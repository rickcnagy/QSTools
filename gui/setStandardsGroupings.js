new QSImporter.iterator(function() {
	$("tr:contains(" + this.item["Name"] + ") button:contains(Edit):last").click();

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