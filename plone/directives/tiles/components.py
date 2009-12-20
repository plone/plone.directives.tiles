import martian
import plone.tiles
import five.grok

import plone.tiles.interfaces

class GrokkedTile(five.grok.View):
    """Base class for grokked tiles - not to be used directly.
    """
    martian.baseclass()

class Tile(GrokkedTile, plone.tiles.Tile):
    """Grokked tile. This uses the same logic as a groked view, but supports
    additional directives and provides the ``data`` attribute found in
    ``plone.tiles.Tile``.
    """
    martian.baseclass()
    
    # Make sure this interface is more specific than the ones from the view
    five.grok.implementsOnly(plone.tiles.interfaces.ITile)
    
    # Take these from the tile class instead of grok.View
    __getitem__ = plone.tiles.Tile.__getitem__
    url = plone.tiles.Tile.url

class PersistentTile(GrokkedTile, plone.tiles.PersistentTile):
    """Grokked persistent tile. This uses the same logic as a groked view, but
    supports additional directives and provides the ``data`` attribute found
    in ``plone.tiles.Tile``.
    """
    martian.baseclass()
    
    # Make sure this interface is more specific than the ones from the view
    five.grok.implementsOnly(plone.tiles.interfaces.IPersistentTile)

    # Take these from the tile class instead of grok.View
    __getitem__ = plone.tiles.PersistentTile.__getitem__
    url = plone.tiles.PersistentTile.url
