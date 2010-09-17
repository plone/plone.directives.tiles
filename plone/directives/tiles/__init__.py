import zope.deferredimport

#
# Grokked tile base classes
#

zope.deferredimport.defineFrom('plone.directives.tiles.components',
    'Tile', 'PersistentTile',
)

#
# Directives
#

zope.deferredimport.defineFrom('plone.directives.tiles.meta',
    'add_permission', 'schema',
)

#
# Convenience import for directives used by tiles
#

zope.deferredimport.defineFrom('five.grok',
    'context', 'require', 'name', 'layer', 'title', 'description',
)
