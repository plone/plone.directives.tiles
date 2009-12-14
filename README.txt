plone.directives.tiles
======================

This package provides declarative configuration (grokkers) for the
`plone.tiles <http://pypi.python.org/pypi/plone.tiles>`_ package.

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
        

Notes:

* A persistent tile can be configured by deriving from ``PersistentTile``
  instead of ``Tile``.
* The ``context()``, ``requires()``, ``name()``, and ``layer()`` directives
  are used in the same way as they are for a view derived from ``grok.View``.
* Templates are associated using the same semantics as are used for views. For
  example, a tile in ``mytiles.py`` defined in the class ``MyTile`` would 
  be associated with a template ``mytiles_templates/mytile.pt`` by default.
* Unlike a view, the ``name()`` directive is required and should give a dotted
  name for the tile by convention.
