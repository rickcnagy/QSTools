`qs` Python Package
===

####[`data_migration.py`](./data_migration.py)

Data migration via the QuickSchools API - utility module.

####[`limit_rate.py`](./limit_rate.py)

Limit request rates on REST servers by request base URL.

####[`logger.py`](./logger.py)

Wrapper on top of the Logger for logging QuickSchools API requests

####[`rest_base.py`](./rest_base.py)

Base-level API interaction tools to be extended upon for different uses.
Generally, the intent is for extension towards the QS API, but this module
is designed to interaction with *any* REST API easier.


####[`rest_request_wrappers.py`](./rest_request_wrappers.py)

A set of wrappers around different specific REST API's. If the wrapper (or a
part of that wrapper) can be used for another REST API, it should be moved to
rest_base.py


####[`util.py`](./util.py)

Utility functions for inclusion in public QS package API