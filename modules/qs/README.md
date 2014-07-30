`qs` Python Package
===

####[`api_keys.py`](./api_keys.py)

Module for setting and getting API keys in the locally saved API key store,
which is stored in ~/API keys.json


####[`data_migration.py`](./data_migration.py)

Data migration via the QuickSchools API - utility module.

####[`logger.py`](./logger.py)

Wrapper on top of the Logger for logging QuickSchools API requests.
\#TEST EXEMPT


####[`logs/`](./logs)

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

####[`util.py`](./util.py)

Utility functions for inclusion in public QS package API
