CHANGE LOG
==========

1.0.0
-----

- Added multi-language support

Backwards incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- deprecated use of ``LanguagePage``: your words competition is now direct child of ``Main`` (use ``SiteLanguage`` for multilanguage support)
- deprecated use of ``competition.thank_you_page``: use the template tag ``{% load_thank_you_page_for_competition competition as thank_you_pages %}``

NOTE: This release is not compatible with molo versions less than 3.0

0.0.2
-----
- update django admin
- add convert to article functionality

0.0.1
-----
- initial release
