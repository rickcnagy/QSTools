Transcript GUI Scripts
===

####[`addCustomSubjects.js`](../gui/Transcripts/addCustomSubjects.js)

 Add a set number of transcript subjects to a set of students by student name. QSImporter's data should be like: `[{name: Rick, subjects:[subjectName1, subjectName2]}] 

####[`deleteCustomSemester.js`](../gui/Transcripts/deleteCustomSemester.js)

 Delete custom semesters on transcripts with a specific string in the year header box. For instance, to delete all the subjects in 2014, set `deleteString` to 2014. 

####[`hideSubjects.js`](../gui/Transcripts/hideSubjects.js)

 Hide a specific subjects on transcripts by subject name. QSImporter's data should be like so: `[{name: Rick, subjects: [subjectName1, subjectName2]}]`