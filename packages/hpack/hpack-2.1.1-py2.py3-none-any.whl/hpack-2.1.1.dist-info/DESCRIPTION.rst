========================================
hpack: HTTP/2 Header Encoding for Python
========================================

.. image:: https://raw.github.com/Lukasa/hyper/development/docs/source/images/hyper.png

.. image:: https://travis-ci.org/Lukasa/hpack.png?branch=master
    :target: https://travis-ci.org/Lukasa/hpack

This module contains a pure-Python HTTP/2 header encoding (HPACK) logic for use
in Python programs that implement HTTP/2. It also contains a compatibility
layer that automatically enables the use of ``nghttp2`` if it's available.

Contributing
============

``hpack`` welcomes contributions from anyone! Unlike many other projects we are
happy to accept cosmetic contributions and small contributions, in addition to
large feature requests and changes.

Before you contribute (either by opening an issue or filing a pull request),
please `read the contribution guidelines`_.

.. _read the contribution guidelines: http://hyper.readthedocs.org/en/development/contributing.html

License
=======

``hpack`` is made available under the MIT License. For more details, see the
``LICENSE`` file in the repository.

Authors
=======

``hpack`` is maintained by Cory Benfield, with contributions from others. For
more details about the contributors, please see ``CONTRIBUTORS.rst``.


Release History
===============

2.1.1 (2016-03-16)
------------------

**Bugfixes**

- When passing a dictionary or dictionary subclass to ``Encoder.encode``, HPACK
  now ensures that HTTP/2 special headers (headers whose names begin with
  ``:`` characters) appear first in the header block.

2.1.0 (2016-02-02)
------------------

**API Changes (Backward Compatible)**

- Added new ``InvalidTableIndex`` exception, a subclass of
  ``HPACKDecodingError``.
- Instead of throwing ``IndexError`` when encountering invalid encoded integers
  HPACK now throws ``HPACKDecodingError``.
- Instead of throwing ``UnicodeDecodeError`` when encountering headers that are
  not UTF-8 encoded, HPACK now throws ``HPACKDecodingError``.
- Instead of throwing ``IndexError`` when encountering invalid table offsets,
  HPACK now throws ``InvalidTableIndex``.
- Added ``raw`` flag to ``decode``, allowing ``decode`` to return bytes instead
  of attempting to decode the headers as UTF-8.

**Bugfixes**

- ``memoryview`` objects are now used when decoding HPACK, improving the
  performance by avoiding unnecessary data copies.

2.0.1 (2015-11-09)
------------------

- Fixed a bug where the Python HPACK implementation would only emit header
  table size changes for the total change between one header block and another,
  rather than for the entire sequence of changes.

2.0.0 (2015-10-12)
------------------

- Remove unused ``HPACKEncodingError``.
- Add the shortcut ability to import the public API (``Encoder``, ``Decoder``,
  ``HPACKError``, ``HPACKDecodingError``) directly, rather than from
  ``hpack.hpack``.

1.1.0 (2015-07-07)
------------------

- Add support for emitting 'never indexed' header fields, by using an optional
  third element in the header tuple. With thanks to @jimcarreer!

1.0.1 (2015-04-19)
------------------

- Header fields that have names matching header table entries are now added to
  the header table. This improves compression efficiency at the cost of
  slightly more table operations. With thanks to `Tatsuhiro Tsujikawa`_.

.. _Tatsuhiro Tsujikawa: https://github.com/tatsuhiro-t

1.0.0 (2015-04-13)
------------------

- Initial fork of the code from `hyper`_.

.. _hyper: https://hyper.readthedocs.org/


