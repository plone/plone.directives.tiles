import martian
import martian.error

import grokcore.component
import grokcore.security

import zope.component.zcml

import plone.tiles.type
import plone.tiles.interfaces
import plone.directives.tiles.components


class add_permission(grokcore.security.require):
    """Directive for giving the add permission of a tile
    """

    scope = martian.CLASS
    store = martian.ONCE


class icon(martian.Directive):
    """Directive for giving the icon of a tile
    """

    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateText


class schema(martian.Directive):
    """Directive for giving the schema of a tile
    """

    scope = martian.CLASS
    store = martian.ONCE
    validate = martian.validateInterface


class TileGrokker(martian.ClassGrokker):
    """Grokker to register a tile. Note that the regular ViewGrokker will
    actually take care of most of the registration for us.
    """

    martian.component(plone.directives.tiles.components.GrokkedTile)

    martian.directive(grokcore.component.name, default=None)
    martian.directive(grokcore.component.title)
    martian.directive(add_permission)

    martian.directive(grokcore.component.description, default=None)
    martian.directive(icon, default=None)
    martian.directive(schema, default=None)

    def execute(self, factory, config, name, title, add_permission,
                description=None, icon=None, schema=None):

        if not add_permission:
            raise martian.error.GrokError(
                u"You must set an add_permission() on the tile", factory)
        if not title:
            raise martian.error.GrokError(
                u"You must set a title() on the tile", factory)
        if not name:
            raise martian.error.GrokError(
                u"You must set a name() on the tile", factory)

        type_ = plone.tiles.type.TileType(name, title, add_permission,
                                          description=description,
                                          icon=icon, schema=schema)
        zope.component.zcml.utility(config,
                                    provides=plone.tiles.interfaces.ITileType,
                                    component=type_, name=name)
        return True
