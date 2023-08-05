Version History
===============

`2.0.1`_ (29 Feb 2016)
----------------------
- Removed deprecation wrapper since it seems to cause really interesting
  problems including the much feared meta-class error.

`2.0.0`_ (24 Feb 2016)
----------------------
- Repackage from a module into a package.  Distributing raw modules inside
  of a namespace package is unreliable and questionably correct.
- Add :func:`sprockets.mixins.mediatype.content.add_transcoder`.
- Add :class:`sprockets.mixins.mediatype.transcoders.JSONTranscoder`.
- Add :class:`sprockets.mixins.mediatype.transcoders.MsgPackTranscoder`.
- Add :class:`sprockets.mixins.mediatype.transcoders.BinaryWrapper`.
- Normalize registered MIME types.
- Raise a 400 status when content body decoding fails.

`1.0.4`_ (14 Sep 2015)
----------------------
- Support using the default_content_type in the settings if request does not
  contain the Accept header

`1.0.3`_ (10 Sep 2015)
----------------------
- Update installation files

`1.0.2`_ (9 Sep 2015)
---------------------
- Rename package to mediatype

`1.0.1`_ (9 Sep 2015)
---------------------
- Repackaged for Travis-CI configuration.

`1.0.0`_ (9 Sep 2015)
---------------------
- Initial Release

.. _Next Release: https://github.com/sprockets/sprockets.http/compare/2.0.0...HEAD
.. _2.0.0: https://github.com/sprockets/sprockets.http/compare/1.0.4...2.0.0
.. _1.0.4: https://github.com/sprockets/sprockets.http/compare/1.0.3...1.0.4
.. _1.0.3: https://github.com/sprockets/sprockets.http/compare/1.0.2...1.0.3
.. _1.0.2: https://github.com/sprockets/sprockets.http/compare/1.0.1...1.0.2
.. _1.0.1: https://github.com/sprockets/sprockets.http/compare/1.0.0...1.0.1
.. _1.0.0: https://github.com/sprockets/sprockets.http/compare/0.0.0...1.0.0
