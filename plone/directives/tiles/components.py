import martian
import plone.tiles
import five.grok

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

class PersistentTile(GrokkedTile, plone.tiles.PersistentTile):
    """Grokked persistent tile. This uses the same logic as a groked view, but
    supports additional directives and provides the ``data`` attribute found
    in ``plone.tiles.Tile``.
    """
    martian.baseclass()
