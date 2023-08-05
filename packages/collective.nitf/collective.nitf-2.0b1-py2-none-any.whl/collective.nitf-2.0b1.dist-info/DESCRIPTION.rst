===============
collective.nitf
===============

.. contents:: Table of Contents

Life, the Universe, and Everything
----------------------------------

News articles in Plone are instances of the 'News Item' content type: they can
contain a title, a description, a body text, an image and some basic metadata.
If you publish a couple of items from time to time, this is fine.

But suppose you have to publish dozens of items everyday... How do you tell
your readers who they are about? What do they cover? Where do they took place?
And, more important, how do you classify them? How do you organize them? How
do you tell your readers which ones are newsworthy?

To solve these, and other issues, the `IPTC`_ developed XML standards to
define the content and structure of news articles. `NITF`_, `NewsML`_ and
`NewsCodes`_ are among these standards and they support the classification,
identification and description of a huge number of news articles
characteristics.

NITF is intended to structure independent news articles and this package aims
to implement a content type inspired by the specification.

Mostly Harmless
---------------

.. image:: http://img.shields.io/pypi/v/collective.nitf.svg
    :target: https://pypi.python.org/pypi/collective.nitf

.. image:: https://img.shields.io/travis/collective/collective.nitf/master.svg
    :target: http://travis-ci.org/collective/collective.nitf

.. image:: https://img.shields.io/coveralls/collective/collective.nitf/master.svg
    :target: https://coveralls.io/r/collective/collective.nitf

Got an idea? Found a bug? Let us know by `opening a support ticket`_.

Don't Panic
-----------

Installation
^^^^^^^^^^^^

To enable this product in a buildout-based installation:

#. Edit your buildout.cfg and add ``collective.nitf`` to the list of eggs to install::

    [buildout]
    ...
    eggs =
        collective.nitf

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``collective.nitf`` and click the 'Activate' button.

.. Note::
	You may have to empty your browser cache and save your resource registries in order to see the effects of the product installation.

Behaviors
^^^^^^^^^

This package includes a behavior called ``collective.nitf.behaviors.interfaces.ISection``.
By applying it to a Dexterity-based content type you will get a new field called ``section``.

Helper views
^^^^^^^^^^^^

All news articles provide @@nitf and @@newsml views that are available although are not registered.

You can validate the output of the those views using services like `XML validation`_.

You may use the `NITF Document Type Definition`_ version 3.5 and the `XHTML Ruby Module`_ associated with it.

.. _`IPTC`: http://www.iptc.org/
.. _`NewsCodes`: http://www.iptc.org/NewsCodes/
.. _`NewsML`: http://www.newsml.org/
.. _`NITF`: http://www.nitf.org/
.. _`NITF Document Type Definition`: http://www.iptc.org/std/NITF/3.5/specification/nitf-3-5.dtd
.. _`XHTML Ruby Module`: http://www.iptc.org/std/NITF/3.5/specification/xhtml-ruby-1.mod
.. _`XML validation`: http://www.xmlvalidation.com/
.. _`opening a support ticket`: https://github.com/collective/collective.nitf/issues

Internals
---------

``collective.nitf`` uses Cycle2 slideshow plugin for jQuery and it can load its resources from the Plone JS registry if they are present there.

If you're using ``collective.nitf`` with other packages that use Cycle2 also (like `sc.photogallery`_ or `covertile.cycle2`_),
it is highly recommended that you register those resources to load them once and avoid conflicts.

You can use a ``jsregistry.xml`` file that includes the following:

.. code-block:: xml

    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.carousel.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />
    <javascript id="++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js"
        cacheable="True" compression="none" cookable="True" enabled="True" />

.. _`sc.photogallery`: https://pypi.python.org/pypi/sc.photogallery
.. _`covertile.cycle2`: https://pypi.python.org/pypi/covertile.cycle2

Share and Enjoy
---------------

``collective.nitf`` would not have been possible without the contribution of
the following people:

- Cleber J. Santos
- Franco Pellegrini
- Gonzalo Almeida
- Héctor Velarde
- Joaquín Rosales
- Juan A. Díaz
- Juan Pablo Giménez
- Marcos F. Romero
- Silvestre Huens
- Érico Andrei
- Rodrigo Ferreira de Souza

You can find an updated list of package contributors on `GitHub`_.

Development sponsored by Open Multimedia.

.. _`GitHub`: https://github.com/collective/collective.nitf/contributors

Changelog
---------

There's a frood who really knows where his towel is.

2.0b1 (2016-02-29)
^^^^^^^^^^^^^^^^^^

- Show title of news article as ``alt`` attribute on tile's image.
  [hvelarde]

- Fix upgrade step to work with both, Archetypes and Dexterity-based collections.
  [rodfersou]


2.0a1 (2015-09-30)
^^^^^^^^^^^^^^^^^^

.. Warning::
    Upgrades are supported only from release 1.0b3.

- Make control panel configlet accesible to Site Administrator role (closes `#137`_).
  [hvelarde]

- Load Cycle2 resources from the JS registry if available (closes `#133`_).
  [hvelarde]

- Fix display of byline and refactor override of ``documentbyline`` viewlet;
  avoid performance issues when having many users by memoizing expensive call to Membership tool (fixes `#128`_).
  [hvelarde, rodfersou]

- Replace slideshow framework machinery;
  we use `Cycle2`_ now instead of `Galleria`_.
  Don't forget do uninstall and remove collective.js.galleria if you no longer depend on it on your site (closes `#116`_).
  [rodfersou, hvelarde]

- Fix default values for genre and urgency fields (closes `#118`_).
  [rodfersou]

- Add NITF tile for collective.cover (closes `#123`_).
  [hvelarde]

- Reimplement section field as a behavior (closes `#98`_).
  [hvelarde]

- Drop support of Plone 4.2.
  [hvelarde]

- Remove dependency on collective.z3cform.widgets.
  Don't forget do uninstall and remove the package if you no longer depend on it on your site.
  [hvelarde]

- Update package i18n and Spanish and Brazilian Portuguese translations.
  [hvelarde]

- Restore default binding on Link content type at uninstall time.
  [hvelarde]

- Add ``Current`` as default value for available_genres and ``General`` as
  default value for available_sections.
  [hvelarde]

- Character counter code was removed from package; this should be
  reimplemented using collective.js.charcount (closes `#75`_).
  [hvelarde]

- Package was cleaned by removing some dependencies,
  deprecated methods on default view,
  unused macros from templates,
  and needless resources, scripts and styles.
  [marcosfromero, hvelarde]

- Remove all javascript from templates, create new nitf.js and use
  jsregistry (closes `#94`_). [marcosfromero]

- Add confirmation overlay before removing an image in media.pt
  (closes `#85`_). [marcosfromero]

- Add required script library in media.pt to prevent image not loading
  when editing in overlay (closes `#84`_). [marcosfromero]

- Fields were reordered to enhance user experience on adding/editing content:
  'location' field is now above 'body text' and 'urgency' is below 'genre'.
  [hvelarde]

- Reimplement ``keywords`` and ``documentbyline`` viewlets with semantic markup and
  support for news article byline for INITF interface.
  [jpgimenez, hvelarde, cleberjsantos]

- Refactor templates to implement semantic markup to annotate news-specific
  metadata using rNews, schema.org and RDFa (closes `#47`_).
  [jpgimenez, marcosfromero, hvelarde]

- Add plone.app.relationfield as a dependency; this is needed for Dexterity
  to proper handle relations (closes `#71`_). [jpgimenez]

- Remove five.grok dependency, will easy the mainteinance and the
  extendibility of the package. [jpgimenez]

- Changes image link behavior in view.pt for mobile devices
  (closes `#62`_). [marcosfromero]


.. _`Cycle2`: http://jquery.malsup.com/cycle2/
.. _`Galleria`: http://galleria.io/
.. _`#47`: https://github.com/collective/collective.nitf/issues/47
.. _`#62`: https://github.com/collective/collective.nitf/issues/62
.. _`#71`: https://github.com/collective/collective.nitf/issues/71
.. _`#75`: https://github.com/collective/collective.nitf/issues/75
.. _`#84`: https://github.com/collective/collective.nitf/issues/84
.. _`#85`: https://github.com/collective/collective.nitf/issues/85
.. _`#94`: https://github.com/collective/collective.nitf/issues/94
.. _`#98`: https://github.com/collective/collective.nitf/issues/98
.. _`#116`: https://github.com/collective/collective.nitf/issues/116
.. _`#118`: https://github.com/collective/collective.nitf/issues/118
.. _`#123`: https://github.com/collective/collective.nitf/issues/123
.. _`#128`: https://github.com/collective/collective.nitf/issues/128
.. _`#133`: https://github.com/collective/collective.nitf/issues/133
.. _`#137`: https://github.com/collective/collective.nitf/issues/137


