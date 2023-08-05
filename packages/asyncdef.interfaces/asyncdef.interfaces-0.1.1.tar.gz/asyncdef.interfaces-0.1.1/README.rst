==========
interfaces
==========

*Public APIs for the core asyncdef components.*

This package contains the public interface definitions for the core asyncdef
components. This package leverages
`iface <https://github.com/kevinconway/iface>`_ for the definitions. Items in
this package are intended to be used with `isinstance` and `issubclass` for
interface comparisons.

.. code-block:: python

    from asyncdef.interfaces.engine import iengine

    assert isinstance(some_implementation, iengine.IEngine)
    assert iface.isinstance(some_implementation, iengine.IEngine)

Interface definitions are placed here to prevent the need for importing the
actual implementation code in order to check the interface.

License
=======

    Copyright 2016 Kevin Conway

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

Contributing
============

Firstly, if you're putting in a patch then thank you! Here are some tips for
getting your patch merged:

Style
-----

As long as the code passes the PEP8 and PyFlakes gates then the style is
acceptable.

Docs
----

The PEP257 gate will check that all public methods have docstrings. If you're
adding something new, like a helper function, try out the
`napoleon style of docstrings <https://pypi.python.org/pypi/sphinxcontrib-napoleon>`_.
