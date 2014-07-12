#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python
"""A set of wrappers around different specific REST API's. If the wrapper (or a
part of that wrapper) can be used for another REST API, it should be moved to
rest_base.py
"""

import qs


class GitHubRequest(qs.BaseRequest):
    base_url = 'https://api.github.com'
