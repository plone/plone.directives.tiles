This package provides declarative configuration (grokkers) for the
`plone.tiles <http://pypi.python.org/pypi/plone.tiles>`_ package.

.. image:: https://secure.travis-ci.org/plone/plone.directives.tiles.png?branch=master
    :target: http://travis-ci.org/plone/plone.tiles

.. contents::

Usage
=====


A basic tile is configured like this::

    from five import grok
    from plone.directives import tiles

    from my.package import MyMessageFactory as _
    from my.package.interfaces import IMyTileSchema

    class MyTile(tiles.Tile):
        grok.context(IContext)
        grok.require('zope2.View')
        
        grok.name('my.tile')
        grok.title(_(u"My title"))
        grok.description(_(u"My description"))
        
        tiles.add_permission('mypackage.AddMyTile')
        tiles.schema(IMyTileSchema)


Notes
=====

* A persistent tile can be configured by deriving from ``PersistentTile``
  instead of ``Tile``.
* The ``context()``, ``requires()``, ``name()``, and ``layer()`` directives
  are used in the same way as they are for a view derived from ``grok.View``.
* Templates are associated using the same semantics as are used for views. For
  example, a tile in ``mytiles.py`` defined in the class ``MyTile`` would 
  be associated with a template ``mytiles_templates/mytile.pt`` by default.
* Unlike a view, the ``name()`` directive is required and should give a dotted
  name for the tile by convention.
* Dictionary key access (``__getitem__()``) is defined to work as it does in
  a tile. In a standard grokked view, it will retrieve a macro from the
  template. In a tile, it is used as a traversal hook to set the tile id,
  and subsequently to look up views on the tile. See ``plone.tiles`` for
  details.
* Similarly, standard grokked views have a ``url()`` method which can be used
  to construct a URL, possibly with query string parameters. For grokked
  tiles, this is replaced by a ``url`` read-only property, which returns the
  canonical tile URL, as per ``plone.tiles``.


Changelog
=========

1.1 (2012-11-26)
----------------

- Added icon directive to support plone.tiles >= 1.1.
  [datakurre]

1.0 (2012-06-23)
----------------

- Initial release
  [garbas]
