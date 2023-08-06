A collection of extensions for Django, developed for internal use at Mauve
Internet.

Most of this work was done in 2007-2011, and may not be up-to-date for use with
current Django.

* ``mauveinternet.calendar`` - Month and Week classes, for applications that
  would like to manipulate and traverse dates in this way.
* ``mauveinternet.content_scoring`` - functionality to rate how good a piece of
  content is.
* ``mauveinternet.devtools`` - management commands for introinspecting Django
  projects
* ``mauveinternet.emailing`` - tools for emailing
* ``mauveinternet.help`` - a self-service help system
* ``mauveinternet.markdown`` - a Markdown-aware input widget and field type
* ``mauveinterent.ordering`` - a basket/cart system, and utilities for building  web shops
* ``mauveinternet.svggraph`` - a server-rendered SVG graph system
* ``mauveinternet.tags`` - miscellaneous useful template tags
* ``mauveinternet.context_processors`` - miscellaneous useful context processors
* ``mauveinternet.csvresponse`` - a ``HttpResponse`` subclass for CSV data
* ``mauveinternet.decorators`` - miscellaneous decorators
* ``mauveinternet.formail`` - send a validated Django form as an e-mail
* ``mauveinternet.decorators`` - miscellaneous Django middleware
* ``mauveintenet.models`` - miscellaneous Django models
* ``mauveinternet.money`` - a Money class following the `Enterprise Design Pattern`_
* ``mauveinternet.shortcuts`` - helper functions to make common operations
  more concise
* ``mauveinternet.thumbnail`` - a Django model field that saves thumbnailed versions whenever a new original is saved

.. _`Enterprise Design Pattern`: http://martinfowler.com/eaaCatalog/money.html
