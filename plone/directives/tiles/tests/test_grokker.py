import unittest
import zope.component.testing
import five.grok.testing

from martian.error import GrokError
from grokcore.component.testing import grok_component
from zope.configuration.exceptions import ConfigurationError

from zope.component import getUtility, getMultiAdapter, provideAdapter
from zope.publisher.browser import TestRequest
from zope.traversing.browser.interfaces import IAbsoluteURL
from plone.tiles.interfaces import ITileType, ITile

# Sample grokked code used in tests

from five import grok
from plone.directives import tiles

from zope.interface import Interface, implements
from zope import schema


class DummyViewPermission(grok.Permission):
    grok.name('dummy.ViewPermission')
    grok.title(u'Dummy view permission')


class DummyAddPermission(grok.Permission):
    grok.name('dummy.AddPermission')
    grok.title(u'Dummy add permission')


class IDummyContext(Interface):
    pass


class DummyContext(object):
    implements(IDummyContext)


class IDummySchema(Interface):
    foo = schema.TextLine()


class TestTileGrokking(unittest.TestCase):

    def setUp(self):
        five.grok.testing.grok('grokcore.component.meta')
        five.grok.testing.grok('grokcore.security.meta')
        five.grok.testing.grok('grokcore.view.meta')

        five.grok.testing.grok('five.grok.meta')
        five.grok.testing.grok('plone.directives.tiles.meta')
        five.grok.testing.grok('plone.directives.tiles.tests.test_grokker')

    def tearDown(self):
        zope.component.testing.tearDown()

    def test_full_init(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            grok.description(u"My description")

            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)

        grok_component('MyTile', MyTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        tileType = getUtility(ITileType, name='my.tile')

        self.failUnless(isinstance(tileView, MyTile))
        self.assertEquals(u"My title", tileType.title)
        self.assertEquals(u"My description", tileType.description)
        self.assertEquals(IDummySchema, tileType.schema)
        self.assertEquals('dummy.AddPermission', tileType.add_permission)

    def test_full_init_persistent(self):
        class MyTile(tiles.PersistentTile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            grok.description(u"My description")

            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)

        grok_component('MyTile', MyTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        tileType = getUtility(ITileType, name='my.tile')

        self.failUnless(isinstance(tileView, MyTile))
        self.assertEquals(u"My title", tileType.title)
        self.assertEquals(u"My description", tileType.description)
        self.assertEquals(IDummySchema, tileType.schema)
        self.assertEquals('dummy.AddPermission', tileType.add_permission)

    def test_minimal_init(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

        grok_component('MyTile', MyTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        tileType = getUtility(ITileType, name='my.tile')

        self.failUnless(isinstance(tileView, MyTile))
        self.assertEquals(u"My title", tileType.title)
        self.assertEquals(None, tileType.description)
        self.assertEquals(None, tileType.schema)
        self.assertEquals('dummy.AddPermission', tileType.add_permission)

    def test_minimal_init_persistent(self):
        class MyTile(tiles.PersistentTile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

        grok_component('MyTile', MyTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        tileType = getUtility(ITileType, name='my.tile')

        self.failUnless(isinstance(tileView, MyTile))
        self.assertEquals(u"My title", tileType.title)
        self.assertEquals(None, tileType.description)
        self.assertEquals(None, tileType.schema)
        self.assertEquals('dummy.AddPermission', tileType.add_permission)

    def test_missing_permission(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            grok.description(u"My description")

            # omitted! tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)

        self.assertRaises(GrokError, grok_component, 'MyTile', MyTile)

    def test_missing_name(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            # omitted! grok.name('my.tile')
            grok.title(u"My title")
            grok.description(u"My description")

            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)

        self.assertRaises(GrokError, grok_component, 'MyTile', MyTile)

    def test_missing_title(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            # omitted! grok.title(u"My title")
            grok.description(u"My description")

            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)

        self.assertRaises(GrokError, grok_component, 'MyTile', MyTile)

    def test_template_association(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

        grok_component('MyTile', MyTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')

        self.assertEquals('<html><body><b>Hello</b></body></html>',
                          tileView().strip())

    def test_render_function(self):
        class MyOtherTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

            def render(self):
                return '<html><body><b>Good bye</b></body></html>'

        grok_component('MyOtherTile', MyOtherTile)

        # Check for view
        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')

        self.assertEquals('<html><body><b>Good bye</b></body></html>',
                          tileView())

    def test_render_or_template_required(self):
        class MyOtherTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

            # no render method and no template in test_grokker_templates/
            # def render(self):
            #                 return '<b>Good bye</b>'

        self.assertRaises(ConfigurationError, grok_component, 'MyOtherTile',
                          MyOtherTile)

    def test_getitem(self):
        class MyOtherTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

            def render(self):
                return '<html><body><b>Good bye %s</b></body></html>' % self.id

        class ViewOnTile(grok.View):
            grok.context(MyOtherTile)
            grok.require('dummy.ViewPermission')
            grok.name('view-on-tile')

            def render(self):
                return 'Dummy view'

        grok_component('MyOtherTile', MyOtherTile)
        grok_component('ViewOnTile', ViewOnTile)

        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        self.assertEquals(None, tileView.id)

        tileView = tileView['tile1']
        self.assertEquals('tile1', tileView.id)

        self.assertEquals('<html><body><b>Good bye tile1</b></body></html>',
                          tileView())

        viewOnTile = tileView['view-on-tile']
        self.assertEquals('Dummy view', viewOnTile())

    def test_url(self):
        class MyOtherTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')

            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')

            def render(self):
                return '<html><body><b>Good bye %s</b></body></html>' % self.id

        class DummyAbsoluteURL(grok.MultiAdapter):
            grok.provides(IAbsoluteURL)
            grok.adapts(IDummyContext, Interface)

            def __init__(self, context, request):
                self.context = context
                self.request = request

            def __unicode__(self):
                return u"http://example.com/context"

            def __str__(self):
                return u"http://example.com/context"

            def __call__(self):
                return self.__str__()

            def breadcrumbs(self):
                return ({'name': u'context',
                         'url': 'http://example.com/context'},)

        grok_component('MyOtherTile', MyOtherTile)
        grok_component('DummyAbsoluteURL', DummyAbsoluteURL)

        from plone.tiles.absoluteurl import TransientTileAbsoluteURL
        provideAdapter(TransientTileAbsoluteURL, adapts=(ITile, Interface,),
                       provides=IAbsoluteURL)

        from plone.tiles.data import TransientTileDataManager
        provideAdapter(TransientTileDataManager)

        context = DummyContext()
        request = TestRequest()

        tileView = getMultiAdapter((context, request,), name='my.tile')
        self.assertEquals(None, tileView.id)
        self.assertEquals('http://example.com/context/@@my.tile', tileView.url)

        tileView = tileView['tile1']
        self.assertEquals('tile1', tileView.id)
        self.assertEquals('http://example.com/context/@@my.tile/tile1',
                          tileView.url)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
