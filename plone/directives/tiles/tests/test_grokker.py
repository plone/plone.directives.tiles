import unittest
import zope.component.testing
import five.grok.testing

from martian.error import GrokError
from zope.configuration.exceptions import ConfigurationError

from zope.component import getUtility, getMultiAdapter
from zope.publisher.browser import TestRequest
from plone.tiles.interfaces import ITileType

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
        
        five.grok.testing.grok_component('MyTile', MyTile)
        
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
        
        five.grok.testing.grok_component('MyTile', MyTile)
        
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
        
        five.grok.testing.grok_component('MyTile', MyTile)
        
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
        
        five.grok.testing.grok_component('MyTile', MyTile)
        
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
        
        self.assertRaises(GrokError, five.grok.testing.grok_component, 'MyTile', MyTile)
    
    def test_missing_name(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')
    
            # omitted! grok.name('my.tile')
            grok.title(u"My title")
            grok.description(u"My description")
    
            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)
        
        self.assertRaises(GrokError, five.grok.testing.grok_component, 'MyTile', MyTile)
    
    def test_missing_title(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')
    
            grok.name('my.tile')
            # omitted! grok.title(u"My title")
            grok.description(u"My description")
    
            tiles.add_permission(DummyAddPermission)
            tiles.schema(IDummySchema)
        
        self.assertRaises(GrokError, five.grok.testing.grok_component, 'MyTile', MyTile)
    
    def test_template_association(self):
        class MyTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')
    
            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')
        
        five.grok.testing.grok_component('MyTile', MyTile)
        
        # Check for view
        context = DummyContext()
        request = TestRequest()
        
        tileView = getMultiAdapter((context, request,), name='my.tile')
        
        self.assertEquals('<b>Hello</b>', tileView())
    
    def test_render_function(self):
        class MyOtherTile(tiles.Tile):
            grok.context(IDummyContext)
            grok.require('dummy.ViewPermission')
    
            grok.name('my.tile')
            grok.title(u"My title")
            tiles.add_permission('dummy.AddPermission')
            
            def render(self):
                return '<b>Good bye</b>'
        
        five.grok.testing.grok_component('MyOtherTile', MyOtherTile)
        
        # Check for view
        context = DummyContext()
        request = TestRequest()
        
        tileView = getMultiAdapter((context, request,), name='my.tile')
        
        self.assertEquals('<b>Good bye</b>', tileView())
    
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
        
        self.assertRaises(ConfigurationError, five.grok.testing.grok_component, 'MyOtherTile', MyOtherTile)
    
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
