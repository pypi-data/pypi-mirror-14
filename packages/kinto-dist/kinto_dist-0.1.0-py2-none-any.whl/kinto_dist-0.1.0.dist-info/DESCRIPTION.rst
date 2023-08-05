Kinto Distribution
==================

This repository contains:

1. a Pip requirements file that combines all packages needed
   to run a Kinto server will a known good set of deps
2. a configuration file to run it


To install it, make sure you have Python 2.x or 3.x with virtualenv, and run::

    $ make install

To run the server::

    $ make serve


CHANGELOG
#########

This document describes changes between each past release.

0.1.0 (2016-03-11)
==================

**Configuration changes**

- ``kinto.plugins.default_bucket`` plugin is no longer assumed. We invite users
  to check that the ``kinto.plugins.default_bucket`` is present in the
  ``includes`` setting if they expect it. (ref #495)

**Version control**

Dependencies version where updated to:

- **cliquet 3.1.0**: https://github.com/mozilla-services/cliquet/releases/tag/3.1.0
- **kinto 2.0.0**: https://github.com/Kinto/kinto/releases/tag/2.0.0
- **kinto-attachment 0.4.0**: https://github.com/Kinto/kinto-attachment/releases/tag/0.4.0
- **kinto-changes 0.1.0**: https://github.com/Kinto/kinto-changes/releases/tag/0.1.0
- **kinto-signer 0.1.0**: https://github.com/Kinto/kinto-signer/releases/tag/0.1.0
- **cliquet-fxa 1.4.0**: https://github.com/mozilla-services/cliquet-fxa/releases/tag/1.4.0
- **boto 2.39**: https://github.com/boto/boto/releases/tag/2.39.0


