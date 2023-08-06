.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide_addons.html
   This text does not appear on pypi or github. It is a comment.

==========================
collective.z3cform.select2
==========================

Features
--------

- select2 multivalued facetednavigation widget for 2-level vocabulary created
  with collective.taxonomy.
  Select "Select2" criteria in facetednavigation and select a taxonomy.
- select2 multivalued z3c.form widget that works nice with 2-level vocabulary
  created with collective.taxonomy
- Upon installation, the default zc3form widget for List/Set of Choice will be
  select2 based. If you don't want this behavior, you can exclude
  collective.z3cform.select2.widget adapters.zcml with z3c.unconfigure.


Theming
-------

The widget was developped initially for a bootstrap 3 theme and fontawesome.
There is a search button icon left to the select that upon click open the select.
If your site doesn't have a bootstrap based theme, you may want to add this
css rule to your project to hide the tiny button::

    button[data-select2-open] { display: none; }

The z3cform widget in display mode uses the badge class, without a comma
separator so it may be confusing when you don't have style for the badge class.
You can revert to a comma separated display by including minimal.zcml instead
of configure.zcml, see Installation below.


Translations
------------

- One constant Faceted.taxonomyAllString currently in French.


Installation
------------

Install collective.z3cform.select2 by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.z3cform.select2
    zcml =
        collective.z3cform.select2
        # or collective.z3cform.select2-minimal


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.z3cform.select2/issues
- Source Code: https://github.com/collective/collective.z3cform.select2


Support
-------

If you are having issues, please let us know.


License
-------

The project is licensed under the GPLv2.
