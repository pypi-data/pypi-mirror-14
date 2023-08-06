3.4.1
=====

Fixed issue in _resolve_url where aliaslist was referenced
before being defined (when paste didn't resolve).

Also corrected indentation in that function.

3.4
===

Moved hosting to Github.

3.3
===

Allow package to be invoked with ``python -m lpaste``.

3.2
===

Use `jaraco.clipboard <https://pypi.python.org/pypi/jaraco.clipboard>`_
for multi-platform clipboard support.

3.1
===

Improved support for SSL with https://paste.jaraco.com and other Heroku-hosted
librarypaste servers.

3.0
===

Dropped support for a configuration file. Use environment variables
``LIBRARYPASTE_URL`` and ``LIBRARYPASTE_USER`` to override default values
in the environment.

2.0
===

Dropped support for Python 2.6
