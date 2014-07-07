QSTools
=======

A toolset for programmatically interacting with the QuickSchools API and GUI quickly and efficiently.


###How this works
* This is a toolset designed to be the building blocks for large and complicated scripts that can be written and run in a short amount of time.
    * As a result, it consists of lots of small and contained but useful scripts.
* The scripts, utilities, and modules contained in this repo are organized by type:
    * [**api**](../master/api): any script that somehow leverages the [QuickSchools REST API](http://apidocs.quickschools.com/). This is currently all Python scripts, but could also be JavaScript (or any other language).
    * [**gui**](../master/gui): any script that programmatically manipulates the GUI (e.g. [ricknagy.quickschools.com](http://ricknagy.quickschools.com/)) to do things that can't be done with the API. These scripts rely heavily on QSIterator, which comes with [QuickSchools Support Tools](https://chrome.google.com/webstore/detail/quickschools-support-tool/hibklcekgpmoheniagkbaeebmelihonh) ([repo here](https://github.com/br1ckb0t/qs-supporttools)).
    * [**modules**](../master/modules): Files that can be *imported*, *included*, etc in scripts in other folders. Provides boilerplate code to make scripts simpler. This folder should be added to your `PYTHONPATH` if you want to run scripts locally.
    * [**utility**](../master/utility): Anything that you run locally that’s a utility - like converting stuff, counting stuff, etc. These generally don't rely on QSTools modules (though can) but more just are useful utilities for automating things locally.
    * [**deprecated**](../master/deprecated): When something changes in the API, GUI, etc to make a script either useless or impossible, it is moved here. These scripts are here just for archive purposes and won't be maintained.
    * [**fun**](../master/fun): Fun stuff, like changing 'Tickets' on ZD to 'Mysteries' :smiley:
* If a script has a docstring at the top, it will not be deleted. Instead, it will be maintained to continue to match that docstring, even if the implementation completely changes.
   * Furthermore, in these "public" scripts, the implementation will be kept up to date to ensure that they can be used quickly and reliably under a deadline.
