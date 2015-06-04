QSTools
=======
[![Build Status](https://travis-ci.org/br1ckb0t/QSTools.svg?branch=master)](https://travis-ci.org/br1ckb0t/QSTools)
[![Coverage Status](https://img.shields.io/coveralls/br1ckb0t/QSTools.svg)](https://coveralls.io/r/br1ckb0t/QSTools?branch=master)

A toolset for programmatically controlling the QuickSchools API and GUI.

###Installation:

1. Download and unzip this repo.
2. `cd` into the unzipped folder.
3. Run:
```
python setup.py install
```
After doing this, a `qs` module will be importable from all Python scripts, and all scripts in this repo will have the necessary dependencies.

###How This Repo Works
* This is a toolset designed to be the **building blocks for large and complicated scripts that can be written and run under a time pressure *without failing*.** As a result, it consists of lots of small, contained, and useful scripts.
* If a script has a docstring at the top, it will not be deleted. Instead, it will be maintained and tested to continue to match that docstring, even if the implementation has to completely change.
* The scripts, utilities, and modules contained in this repo are organized by type:
    * [**api**](./api): any script that somehow leverages the [QuickSchools REST API](http://apidocs.quickschools.com/) for the purpose of changing data within QuickSchools. This is currently all Python scripts, but could also be JavaScript (or any other language).
    * [**csv**](./csv): any script that manipulates CSV's somehow, especially for imports. While they may access the api to GET information, these scripts don't impact the data on QuickSchools on thier own. 
    * [**gui**](./gui): any script that programmatically manipulates the GUI (e.g. [ricknagy.quickschools.com](http://ricknagy.quickschools.com/)) to do things that can't be done with the API. These scripts rely heavily on QSIterator, which comes with [QuickSchools Support Tools](https://chrome.google.com/webstore/detail/quickschools-support-tool/hibklcekgpmoheniagkbaeebmelihonh) ([repo here](https://github.com/br1ckb0t/qs-supporttools)).
    * [**modules**](./modules): Files that can be *imported*, *included*, etc in scripts in other folders. Importable code here is considered an **API** in and of itself. Properties in this API will generally not be deprecated (or at least not often) in order to avoid refactoring issues throughout the codebase, though properties can and will be added over time. The [**qs**](./modules/qs) subdirectory contains the code for the API wrapper utilized throughout this project. 
    * [**utility**](./utility): Anything that you run locally that’s a utility - like converting stuff, counting stuff, etc. These generally don't rely on QSTools modules (though can) but more just are useful utilities for automating things locally.
    * [**deprecated**](./deprecated): When something changes in the API, GUI, etc to make a script either useless or impossible, it is moved here. These scripts are here just for archive purposes and won't be maintained.
    * [**tests**](./tests): All unit tests and integration tests, covering Python only for now. As stated above, *any file with a docstring* will be included in the coverage metrics and tested if possible. More on this below.
    * [**examples**](./examples): Example data for what scripts need to ingest to run properly. (*remember: this is a public repo so no school data here, please*)
    * [**fun**](./fun): Fun stuff, like changing the labels on Zendesk for `Tickets` to `Mysteries` :smiley:

###Git Hooks, the Build, and Coverage
There is one important git hook: building docs in the `pre-commit` hook. The `pre-commit` must call [`buildocs.sh`](./pre-commit.sh), which contains the actual logic. This serves two purposes:

1. It ensures that all automatically generated `README`s (such as [the ./api README](./api/README.md)]) are always up to date with each commit.
2. It ensures that all files in documented folders can at least be successfully imported, which clears alot of the issues that would cause tests to fail.

The build currently takes place on [travis-ci](https://travis-ci.org/br1ckb0t/QSTools.svg?branch=master) with each commit (usually after a ≈2 minute delay) and the status ([![Build Status](https://travis-ci.org/br1ckb0t/QSTools.svg?branch=master)](https://travis-ci.org/br1ckb0t/QSTools)) is always present at the top of this document.

The coverage metric ([![Coverage Status](https://img.shields.io/coveralls/br1ckb0t/QSTools.svg)](https://coveralls.io/r/br1ckb0t/QSTools?branch=master)) reflects the amount of testable Python code that is currently covered by tests. A high coverage number shows that this module is probably ready for most Python-centric imports.

###More On Testing
Since the purpose of this repo is to provide lots of ready-made tools for quickly and efficiently making imports and manipulating data, it's *really* important that one can rely that the repo actually does what it says it does. As a result, there's a testing system to ensure that all implementations match their docstrings:
* **Any script with a docstring** is considered testable.
* **The coverage number reflects the amount of documented Python code that is covered by tests.**
* If a file is testable, there are three options:
    1. If it's a Python file, a test should exist for it in [tests/](../tests). Regardless of whether a test exists for it, it'll be included in the coverage number.
    2. If it's a JavaScript file, it'll be hand-tested at regular intervals, and the status of the test will be included at the beginning of the docstring, like so:

         ```
         /**
         * Last test: 7/14/14: #PASSED
         */
         ```
         
   3. It can be exempted from testing. For instance, [`logger.py`](./modules/qs/logger.py) is hard to test, and the output is being viewed all the time anyways. So, for similar instances, files can be tagged as `#TEST_EXEMPT` like so:
      
      ```
      """#TEST_EXEMPT. Some description here..."""
      
      /**
       * #TEST_EXEMPT
       * ...
       */
      ```
   
      Any test exempt script should be added to `omit` in [`.coveragerc`](./.coveragerc).
* Testing will be done on [qstools.quickschools.com](https://qstools.quickschools.com). For API scripts, this means that caching is imperative to keep testing time down - but this should be baked into the `qs` package anyways :+1:

###The `qs` Package
Included in this repo is a Python package that provides a simple API for doing lots of complicated, often repeated tasks. Full documentation doesn't currently exist, but is in process. See the installation section above for installation directions.

###Contributing and using
At this point, there are `2` dependencies to running scripts in this repo:
* The `qs` package (installation above).
* QS Support Tools ([install extension here](https://chrome.google.com/webstore/detail/quickschools-support-tool/hibklcekgpmoheniagkbaeebmelihonh))

###Support
If you have any questions on this repo, feel free to contact us ([Rick](https://github.com/br1ckb0t) and [Anna](https://github.com/sirfrancium)) on HipChat :smile:
