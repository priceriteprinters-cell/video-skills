import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import design_tools as d


class DesignToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        font = self.root/'example.woff2'; font.write_bytes(b'wOF2fixture')
        self.brief = {'aspect_ratio':'16:9','width':1920,'height':1080,
            'aspect_ratio_confirmed':True,'font_choice_confirmed':True,'palette_choice_confirmed':True,
            'fonts':{'heading':'Space Grotesk','body':'DM Sans','captions':'DM Sans'},
            'font_files':[str(font)], 'font_verification':{'licenses_reviewed':True,'glyphs_checked':True,'renderer_loaded':True},
            'theme':'studio-light', 'palette':{'background':'#F7F8FA','text':'#15212B','accent':'#12634E','secondary':'#8B3B21'}}

    def test_pairing_allows_multiple_families(self):
        self.assertTrue(d.validate_brief(self.brief)['valid'])

    def test_single_family_allowed(self):
        self.brief['fonts'] = dict.fromkeys(('heading','body','captions'), 'Manrope')
        self.assertTrue(d.validate_brief(self.brief)['valid'])

    def test_ratio_requires_confirmation(self):
        self.brief['aspect_ratio_confirmed'] = False
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_font_requires_confirmation(self):
        self.brief['font_choice_confirmed'] = False
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_palette_requires_confirmation(self):
        self.brief['palette_choice_confirmed'] = False
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_ratio_mismatch(self):
        self.brief['width'] = 1080
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_missing_font(self):
        self.brief['font_files'] = ['/missing/font.woff2']
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_low_contrast(self):
        self.brief['palette']['text'] = '#F7F8FA'
        self.assertFalse(d.validate_brief(self.brief)['valid'])

    def test_preview_and_presets_complete(self):
        presets = json.loads((Path(__file__).resolve().parent.parent/'assets/design-presets.json').read_text())
        self.assertGreaterEqual(len(presets['font_pairings']),25); self.assertGreaterEqual(len(presets['palettes']),20)
        for p in presets['font_pairings'].values():
            for role in ('heading','body','captions'): self.assertIn(p[role], p['google_dirs'])
        out = d.preview_html(presets, list(presets['font_pairings'])[:3], 'noir-gold', '<x>')
        self.assertIn('fonts.googleapis.com/css2', out); self.assertIn('&lt;x&gt;', out); self.assertNotIn('<x>', out)

    def test_contrast_reference(self):
        self.assertAlmostEqual(d.contrast('#000000','#FFFFFF'), 21)

    def test_presets_contrast(self):
        presets = json.loads((Path(__file__).resolve().parent.parent/'assets/design-presets.json').read_text())
        for palette in presets['palettes'].values():
            self.assertGreaterEqual(d.contrast(palette['text'],palette['background']),4.5)

    def test_svg_and_html_validation(self):
        self.assertEqual(d.file_kind(b'<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0"/></svg>'),'svg')
        for data in (b'<html>login</html>', b'<svg><script>alert(1)</script></svg>',
                     b'<svg><image href="https://example.org/x"/></svg>',
                     b'<svg><path fill="url(https://example.org/x)"/></svg>',
                     b'<!DOCTYPE svg [<!ENTITY x "x">]><svg/>'):
            with self.assertRaises(ValueError): d.file_kind(data)

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError): d.save_asset(b'x','../x.png',self.root,{})

    def test_no_overwrite_and_provenance(self):
        entry = d.save_asset(b'wOF2fixture','new.woff2',self.root,{'url':'https://fonts.gstatic.com/example'})
        self.assertEqual(len(entry['sha256']),64)
        with self.assertRaises(ValueError): d.save_asset(b'other','new.woff2',self.root,{})
        self.assertEqual((self.root/'new.woff2').read_bytes(),b'wOF2fixture')

    def test_private_http_credentials_and_secret_urls_rejected(self):
        for url in ('http://cdn.simpleicons.org/x','https://user:pass@cdn.simpleicons.org/x',
                    'https://cdn.simpleicons.org/x?token=abc','https://127.0.0.1/x'):
            with self.assertRaises(ValueError): d.public_url(url,d.HOSTS|{'127.0.0.1'})
        with patch('socket.getaddrinfo',return_value=[(0,0,0,'',('127.0.0.1',443))]):
            with self.assertRaises(ValueError): d.public_url('https://cdn.simpleicons.org/x',d.HOSTS)

    def test_redirect_destination_rechecked(self):
        handler = d.Redirects(d.HOSTS)
        with self.assertRaises(ValueError): handler.redirect_request(None,None,302,'',{},'http://localhost/x')

    def test_download_limit(self):
        class Response:
            headers = {'Content-Length':'1000'}
            def geturl(self): return 'https://cdn.simpleicons.org/x'
            def __enter__(self): return self
            def __exit__(self,*a): pass
        with patch.object(d,'public_url'), patch('urllib.request.build_opener') as opener:
            opener.return_value.open.return_value = Response()
            with self.assertRaises(ValueError): d.read_public('https://cdn.simpleicons.org/x',d.HOSTS,100)

    def test_invalid_records_do_not_crash(self):
        for field in ('fonts','font_verification','font_files','palette'):
            brief = copy.deepcopy(self.brief); brief[field] = None
            self.assertFalse(d.validate_brief(brief)['valid'])


if __name__ == '__main__': unittest.main()
