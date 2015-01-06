GUI Scripts
===

####[`cleanStudentNames.js`](./cleanStudentNames.js)

 Open up all student records and clean the student name, then trigger the .keyup() method on the student name input to get the display name to recalculate. Originally used for SacPrep (7/16/14) - (no ticket yet) 

####[`clickRCComments.js`](./clickRCComments.js)

 Click on all comments on all RC's, then save. This is useful for "recalculating" the comments, such as when rich text issues need to be reset. 

####[`Copy & Paste Switches.js`](./Copy & Paste Switches.js)

 Copy & Paste switches between Zeus templates. \#TODO: move to qs-supporttools 

####[`createFinalFormulas.js`](./createFinalFormulas.js)

 Create a final formula that consists of Assignments in each gradebook 

####[`deleteAllCriteria.js`](./deleteAllCriteria.js)

 Delete all criteria in the subject-specific criteria screen. 

####[`deleteAllSubjects.js`](./deleteAllSubjects.js)

 Delete all subjects visible on the Global Subject Setup screen. TODO: handle non-zero enrollment 

####[`downloadRCsFromOldSession.js`](./downloadRCsFromOldSession.js)

 Download all report cards from an old (pre-HTML5 session) Any RC sessions from before HTML5 don't show up except through the student profile. This allows for a mass export of rc's from a given session. Be sure to "Allow site to download multiple files" when prompted. To download from all sessions visible in the student profile, set SECTION_NAME to null, otherwise set it to a string of the section name. 

####[`dropdownsToLikerts.js`](./dropdownsToLikerts.js)

 Convert all dropdowns for a criteria to likert. This maintains the value in each criteria, but makes what was a dropdown into a likert. This uses the grading scale from the first dropdown, so if there are multiple grading scales in use that could be confusing. First written for lapazschool (\#32905). 

####[`exportCriteria.js`](./exportCriteria.js)

 Export criteria from the Report Cards module. Relies on the current template being Super Basic. Data is exported in the import format from ./importCriteria.js, so an export from here can be imported back in using ./importCriteria.js 

####[`importCriteria.js`](./importCriteria.js)

 Import criteria into the Report Cards module. Relies on the current template being Super Basic. If a subject template is found with the same name as the one being imported: - the criteria for that template will be added to the matched one. - The alternative subject section name will be updated to the one from the import. - If individual criteria are found that have the same value as the one being imported, those will be deleted and re-added if the type is different (i.e. one is adropdown and one is a field). QSImporter should have an object like this: [ { "Template Name": "Reading 3-5", "Alternative Subject Section Name": "Reading", "Criteria": [ {"Criteria Name": "A,B,C,D,F"}, // dropdown "Criteria Name", // field ... ] }, ... ] 

####[`importInquiriesOrApplicants.js`](./importInquiriesOrApplicants.js)

 Import inquiries or applicants from QSImporter. QSImporter should have a JSONArray, each with an object with fields matching the Add Inquiry/Add Applicant page. 

####[`likertsToDropdowns.js`](./likertsToDropdowns.js)

 Convert Likerts to dropdowns. This maintains the value in each criteria, but makes what was a likert value into a drop down. This requires that ALL criteria in each criteria set is a Likert. First written for lapazschool (\#32879). 

####[`manuallyParseStudentNames.js`](./manuallyParseStudentNames.js)

 Parse full names on the Students module and manually set First, MI, Last. This is an alternative to simply triggering the blur() event on the name field, when for some reason that isn't working. This parses full names like "Jobs, Steve P.", but the regex could be adapted to fit whatever format the full name is currently in. 

####[`saveAllGradebooks.js`](./saveAllGradebooks.js)

 Save all Gradebooks visible in the Gradebook module. 

####[`saveAllStudentRecords.js`](./saveAllStudentRecords.js)

 Save all student records visible in the Students module and trigger the blur() event on the full name field to update the name separation. For more fine-grain control over the parsing, see ./manuallyParseStudentNames.js. 

####[`Transcripts/`](./Transcripts)
