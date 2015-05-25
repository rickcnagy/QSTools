`qs` Python Package
===

####[`api_keys.py`](./api_keys.py)

Module for setting and getting API keys in the locally saved API key store,
which is stored in ~/API keys.json


####[`data_migration.py`](./data_migration.py)

Data migration via the QuickSchools API - utility module.

####[`flash_object_util.py`](./flash_object_util.py)


Utility for working with FlashObject tools. This is great for manipulating Raw
Data Dumps, such as in the Templates module in Control.

Originally developed for replace_template_colors

Functions require that everything is based off of xml.etree.ElementTree
(normally abbreviated as tree) and xml.etree.Element (abbreviated as element)

Any functions/methods that use this module should be passing in and working
with ElementTrees or Elements.


####[`logger.py`](./logger.py)

Wrapper on top of the Logger for logging QuickSchools API requests.
\#TEST EXEMPT


####[`logs/`](./logs)

####[`messages.py`](./messages.py)

Messages for any long command line etc output.

####[`__pycache__/`](./__pycache__)

####[`rate_limiting.py`](./rate_limiting.py)

Limit request rates on REST servers by request base URL.

####[`rest_cache.py`](./rest_cache.py)

Custom caching for the QS package, centered around caching REST responses
in memory.


####[`rest_foundation.py`](./rest_foundation.py)

Base-level API interaction tools to be extended upon for different uses.
Generally, the intent is for extension towards the QS API, but this module
is designed to interaction with *any* REST API easier.


####[`rest_request_wrappers.py`](./rest_request_wrappers.py)

A set of wrappers around different specific REST API's. If the wrapper (or a
part of that wrapper) can be used for another REST API, it should be moved to
rest_base.py


####[`status_bar.py`](./status_bar.py)

A status bar for use in loops, based off of tqdm:
https://github.com/noamraph/tqdm
\#TEST EXEMPT


####[`test_data.py`](./test_data.py)

Config dummy data for tests

####[`titlecase.py`](./titlecase.py)


Return a titlecased version of a string.
Adapted from Stuart Colville http://muffinresearch.co.uk
Original Perl version by: John Gruber http://daringfireball.net/ 10 May 2008
License: http://www.opensource.org/licenses/mit-license.php


####[`util.py`](./util.py)

Utility functions for inclusion in public QS package API.

Includes lots of little functions that wouldn't be worth writing normally
but end up being super useful over multiple scripts.

The requirements for functionsto be in this module:
    - Simple, intuitive
    - Useful among multiple scripts/modules
