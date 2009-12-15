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
    five.grok.implements(plone.tiles.interfaces.ITile)

class PersistentTile(GrokkedTile, plone.tiles.PersistentTile):
    """Grokked persistent tile. This uses the same logic as a groked view, but
    supports additional directives and provides the ``data`` attribute found
    in ``plone.tiles.Tile``.
    """
    martian.baseclass()
    
    # Make sure this interface is more specific than the ones from the view
    five.grok.implements(plone.tiles.interfaces.IPersistentTile)
