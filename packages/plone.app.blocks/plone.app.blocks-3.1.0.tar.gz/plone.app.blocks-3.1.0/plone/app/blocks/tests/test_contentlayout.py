# -*- coding: utf-8 -*-
import unittest

from lxml import html
import pkg_resources
from plone.app.blocks.indexing import LayoutSearchableText
from plone.app.blocks.layoutbehavior import ContentLayoutView
from plone.app.blocks.layoutbehavior import ILayoutAware
from plone.app.blocks.subscribers import onLayoutEdited
from plone.app.blocks.testing import BLOCKS_FUNCTIONAL_TESTING
from plone.app.blocks.utils import bodyTileXPath
from plone.app.blocks.utils import getLayout
from plone.app.blocks.utils import tileAttrib
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from plone.tiles.data import ANNOTATIONS_KEY_PREFIX
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from zope.component import getGlobalSiteManager
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory

try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    HAS_PLONE_APP_CONTENTTYPES = False
else:
    HAS_PLONE_APP_CONTENTTYPES = True


class TestContentLayout(unittest.TestCase):

    layer = BLOCKS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.registry = getUtility(IRegistry)

        setRoles(self.portal, TEST_USER_ID, ('Manager',))
        self.portal.invokeFactory('Folder', 'f1', title=u"Folder 1")
        self.portal['f1'].invokeFactory('Document', 'd1', title=u"Document 1")
        setRoles(self.portal, TEST_USER_ID, ('Member',))

        if HAS_PLONE_APP_CONTENTTYPES:
            from plone.app.contenttypes.interfaces import IDocument
            iface = IDocument
        else:
            iface = self.portal['f1']['d1'].__class__

        class DocumentLayoutAware(object):
            implements(ILayoutAware)
            adapts(iface)

            def __init__(self, context):
                self.context = context

            content = None
            contentLayout = None
            sectionSiteLayout = None
            pageSiteLayout = None

        self.behavior = DocumentLayoutAware

        sm = getGlobalSiteManager()
        sm.registerAdapter(self.behavior)
        registrations = sm.getAdapters((self.portal['f1']['d1'],),
                                       ILayoutAware)
        self.assertEqual(len(list(registrations)), 1)

    def tearDown(self):
        sm = getGlobalSiteManager()
        sm.unregisterAdapter(self.behavior)
        registrations = sm.getAdapters((self.portal['f1']['d1'],),
                                       ILayoutAware)
        self.assertEqual(len(list(registrations)), 0)

    def test_content_layout_vocabulary(self):
        factory = getUtility(IVocabularyFactory,
                             name='plone.availableContentLayouts')
        vocab = factory(self.layer['portal'])
        self.assertEqual(len(vocab), 3)

        self.assertIn('testlayout1/content.html', vocab.by_token)
        self.assertEqual(
            vocab.getTermByToken('testlayout1/content.html').value,
            u'/++contentlayout++testlayout1/content.html')
        self.assertEqual(
            vocab.getTermByToken('testlayout1/content.html').title,
            'Testlayout1')

        self.assertIn('testlayout2/mylayout.html', vocab.by_token)
        self.assertEqual(
            vocab.getTermByToken('testlayout2/mylayout.html').value,
            u'/++contentlayout++testlayout2/mylayout.html')
        self.assertEqual(
            vocab.getTermByToken('testlayout2/mylayout.html').title,
            'My content layout')

        self.assertIn('testlayout2/mylayout2.html', vocab.by_token)
        self.assertEqual(
            vocab.getTermByToken('testlayout2/mylayout2.html').value,
            u'/++contentlayout++testlayout2/mylayout2.html')
        self.assertEqual(
            vocab.getTermByToken('testlayout2/mylayout2.html').title,
            'My content layout 2')

    def test_content_layout(self):
        self.behavior.contentLayout = \
            '/++contentlayout++testlayout1/content.html'
        rendered = ContentLayoutView(self.portal['f1']['d1'], self.request)()
        tree = html.fromstring(rendered)
        tiles = [node.attrib[tileAttrib] for node in bodyTileXPath(tree)]
        self.assertIn(
            './@@test.tile1/tile2?magicNumber:int=2&X-Tile-Persistent=yes',
            tiles)
        self.assertIn(
            './@@test.tile1/tile3?X-Tile-Persistent=yes',
            tiles)

    def test_error_layout(self):
        self.behavior.contentLayout = \
            '/++sitelayout++missing/missing.html'
        rendered = ContentLayoutView(self.portal['f1']['d1'], self.request)()
        self.assertIn('Could not find layout for content', rendered)

    def test_getLayout(self):
        self.behavior.contentLayout = '/++contentlayout++testlayout1/content.html'
        layout = getLayout(self.portal['f1']['d1'])
        self.assertIn(
            './@@test.tile1/tile2?magicNumber:int=2',
            layout)

    def test_getLayout_custom(self):
        self.behavior.content = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html data-layout="./@@default-site-layout">
  <body>
    <h1>Foobar!</h1>
    <div data-panel="panel1">
      Page panel 1
       <div id="page-tile2" data-tile="./@@test.tile1/tile99?magicNumber:int=3">
       Page tile 2 placeholder</div>
    </div>
  </body>
</html>"""
        layout = getLayout(self.portal['f1']['d1'])
        self.assertIn(
            './@@test.tile1/tile99?magicNumber:int=3',
            layout)

    def test_getting_indexed_data(self):
        self.behavior.content = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html data-layout="./@@default-site-layout">
<body>
  <div class="mosaic-tile rawhtml-tile
              mosaic-plone.app.standardtiles.rawhtml-tile">
    <div class="mosaic-tile-content">
      <div data-tile="./@@plone.app.standardtiles.rawhtml/rawhtml-1"></div>
    </div>
  </div>
  <div class="mosaic-tile mosaic-text-tile">
    <div class="mosaic-tile-content">
        <p>Foobar inserted text tile</p>
    </div>
  </div>
</body>
</html>"""
        content = self.portal['f1']['d1']
        annotations = IAnnotations(content)
        annotations[ANNOTATIONS_KEY_PREFIX + '.rawhtml-1'] = {
            'content': '<p>Foobar inserted raw tile</p>'
        }
        indexed_data = LayoutSearchableText(content)()
        self.assertTrue('Foobar inserted text tile' in indexed_data)
        self.assertTrue('Foobar inserted raw tile' in indexed_data)

    def test_on_save_tile_data_is_cleaned(self):
        self.behavior.content = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html data-layout="./@@default-site-layout">
<body>
  <div data-tile="./@@faketile/foobar-1"></div>
  <div data-tile="./@@faketile/foobar-2"></div>
  <div data-tile="./@@faketile/foobar-3"></div>
  <div data-tile="./@@faketile/foobar-4"></div>
</body>
</html>"""

        content = self.portal['f1']['d1']
        annotations = IAnnotations(content)
        annotations.update({
            ANNOTATIONS_KEY_PREFIX + '.foobar-1': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.foobar-2': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.foobar-3': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.foobar-4': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.bad-1': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.bad-2': {
                'foo': 'bar'
            },
            ANNOTATIONS_KEY_PREFIX + '.bad-3': {
                'foo': 'bar'
            },
        })

        onLayoutEdited(content, None)
        annotations = IAnnotations(content)
        self.assertTrue(ANNOTATIONS_KEY_PREFIX + '.foobar-1' in annotations)
        self.assertTrue(ANNOTATIONS_KEY_PREFIX + '.foobar-2' in annotations)
        self.assertTrue(ANNOTATIONS_KEY_PREFIX + '.foobar-3' in annotations)
        self.assertTrue(ANNOTATIONS_KEY_PREFIX + '.foobar-4' in annotations)
        self.assertFalse(ANNOTATIONS_KEY_PREFIX + '.bad-1' in annotations)
        self.assertFalse(ANNOTATIONS_KEY_PREFIX + '.bad-2' in annotations)
        self.assertFalse(ANNOTATIONS_KEY_PREFIX + '.bad-3' in annotations)
