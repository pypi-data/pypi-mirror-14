.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://travis-ci.org/collective/collective.calltoaction.svg?branch=master
    :target: https://travis-ci.org/collective/collective.calltoaction


==============================================================================
collective.calltoaction
==============================================================================

This shows a call to action: an overlay with an image, titel rich text.
This calls the attention of a visitor to take action, usually to click a link
or button.


Compatibility
-------------

Works on Plone 4.3.x, tested explicitly on Plone 4.3.8.
Not yet compatible with Plone 5: the javascript and css need work.


Features
--------

- A call to action portlet.
  This is basically a copy of the static text portlet with a few extra options.

- In the portlet you can set the number of milliseconds before the overlay is shown.

- When the overlay is shown, a cookie is set.
  We use this to show the overlay only once.
  The cookie is specific for this portlet:
  a new call to action portlet will be shown once too.

- When you edit the portlet,
  you can use a checkbox to say that this is not a minor edit, but a new version.
  The previous cookie is then not valid anymore and the visitor will again see the overlay once.

- The portlet itself is never shown.
  Instead a viewlet looks for portlets and shows the contents after a pause.
  This avoids a portlet column taking up space but not showing anything when there are no other portlets.

- You can create multiple portlets if you really want to,
  but only one overlay is shown on a page.
  If there are three portlets, and the user has already seen the first one but not the others, then the second one will be shown.


Examples
--------

This add-on is planned to be used on https://www.arbounie.nl and http://www.zeelandia.com,
who have sponsored development, but the sites may not always have a call to action configured.


Translations
------------

This product has been translated into

- Dutch (Maurits van Rees)


Installation
------------

Install collective.calltoaction by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.calltoaction


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.calltoaction/issues
- Source Code: https://github.com/collective/collective.calltoaction
- Documentation: https://pypi.python.org/pypi/collective.calltoaction


Support
-------

If you are having issues, please let us know by creating an issue in the tracker.


License
-------

The project is licensed under the GPLv2.
