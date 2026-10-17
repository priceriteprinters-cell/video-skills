#!/usr/bin/env python3
"""Validated creative briefs and bounded public design-asset acquisition."""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import re
import socket
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HOSTS = {'cdn.simpleicons.org', 'api.iconify.design', 'fonts.googleapis.com',
         'fonts.gstatic.com', 'fonts.bunny.net', 'cdn.jsdelivr.net',
         'raw.githubusercontent.com', 'images.unsplash.com', 'images.pexels.com'}
SENSITIVE = {'token', 'key', 'api_key', 'apikey', 'signature', 'access_token', 'password', 'secret'}


def public_url(url, hosts):
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise ValueError('Only credential-free public HTTPS URLs on port 443 are permitted')
    if p.hostname not in hosts:
        raise ValueError('Hostname is not approved; inspect the source and add --allow-host if appropriate')
    try:
        ipaddress.ip_address(p.hostname)
    except ValueError:
        pass
    else:
        raise ValueError('IP-literal URLs are not allowed')
    if any(k.lower() in SENSITIVE for k, _ in urllib.parse.parse_qsl(p.query)):
        raise ValueError('Sensitive query parameter is not permitted')
    addresses = socket.getaddrinfo(p.hostname, 443, type=socket.SOCK_STREAM)
    if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
        raise ValueError('Private or non-public network destination rejected')
    return url


class Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, hosts):
        super().__init__()
        self.hosts = hosts

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        public_url(newurl, self.hosts)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_public(url, hosts, limit):
    public_url(url, hosts)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), Redirects(hosts))
    req = urllib.request.Request(url, headers={'User-Agent': 'DesignAssetHelper/2.0'})
    with opener.open(req, timeout=30) as response:
        public_url(response.geturl(), hosts)
        length = response.headers.get('Content-Length')
        if length and int(length) > limit:
            raise ValueError('Response exceeds download limit')
        data = response.read(limit + 1)
        if not data or len(data) > limit:
            raise ValueError('Empty response or download limit exceeded')
        return data, response.geturl()


def file_kind(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    if data.startswith(b'\xff\xd8\xff'): return 'jpg'
    if data[:6] in (b'GIF87a', b'GIF89a'): return 'gif'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return 'webp'
    if data[:4] == b'RIFF' and data[8:12] == b'WAVE': return 'wav'
    if data[4:8] == b'ftyp': return 'mp4'
    if data[:4] == b'OggS': return 'ogg'
    if data[:3] == b'ID3' or (len(data) > 1 and data[0] == 255 and data[1] & 224 == 224): return 'mp3'
    for magic, kind in ((b'wOF2', 'woff2'), (b'wOFF', 'woff'), (b'OTTO', 'otf'), (b'\x00\x01\x00\x00', 'ttf')):
        if data.startswith(magic): return kind
    # Reject non-UTF8 SVG and active/external content, including inline CSS.
    try:
        text = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        raise ValueError('Unsupported media signature') from None
    if '<!doctype' in text.lower() or '<!entity' in text.lower():
        raise ValueError('SVG declarations/entities rejected')
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        raise ValueError('Expected supported media, not HTML or text') from None
    if root.tag.split('}')[-1] != 'svg': raise ValueError('Response is not an SVG')
    for node in root.iter():
        tag = node.tag.split('}')[-1].lower()
        if tag in {'script', 'foreignobject', 'style', 'image', 'animate', 'set', 'animatetransform', 'animatemotion'}:
            raise ValueError('Active/external SVG content rejected')
        for key, value in node.attrib.items():
            local = key.split('}')[-1].lower()
            if local.startswith('on') or local in {'style', 'base'}:
                raise ValueError('Active SVG attribute rejected')
            if local in {'href', 'src'} and not value.startswith('#'):
                raise ValueError('External SVG reference rejected')
            for ref in re.findall(r'url\s*\((.*?)\)', value, flags=re.I):
                if not ref.strip(' \t\n\r\'"').startswith('#'):
                    raise ValueError('External SVG paint reference rejected')
    return 'svg'


def save_asset(data, name, out, metadata):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,159}', name) or '..' in name:
        raise ValueError('Use a simple non-traversing filename')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    dest = out / name
    manifest = out / 'asset-manifest.json'
    if name == manifest.name or dest.exists(): raise ValueError('Destination already exists or is reserved')
    entries = json.loads(manifest.read_text()) if manifest.exists() else []
    entry = dict(metadata, file=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    partial = None
    try:
        with tempfile.NamedTemporaryFile(dir=out, suffix='.partial', delete=False) as f:
            partial = Path(f.name)
            f.write(data)
        # Exclusive creation avoids accidental replacement; serial writes required.
        with dest.open('xb') as target:
            target.write(partial.read_bytes())
        entries.append(entry)
        temp_manifest = out / 'asset-manifest.json.partial'
        temp_manifest.write_text(json.dumps(entries, indent=2) + '\n')
        temp_manifest.replace(manifest)
    except Exception:
        # Do not remove a pre-existing destination if exclusive creation failed.
        raise
    finally:
        if partial: partial.unlink(missing_ok=True)
    return entry


def fetch(url, name, args):
    if not args.rights_reviewed or not args.license or not args.license_url or not args.purpose:
        raise ValueError('Reviewed rights, license description/evidence URL and purpose are required')
    evidence = urllib.parse.urlsplit(args.license_url)
    if evidence.scheme != 'https' or not evidence.hostname or evidence.username or evidence.password:
        raise ValueError('License evidence must be a public HTTPS URL')
    data, final = read_public(url, HOSTS | set(args.allow_host), args.max_bytes)
    kind = file_kind(data)
    extension = Path(name).suffix.lower().lstrip('.')
    if extension == 'jpeg': extension = 'jpg'
    if extension != kind: raise ValueError('Filename extension does not match detected media type')
    return save_asset(data, name, args.out, {'url': final, 'source_url': url, 'type': kind,
        'license': args.license, 'license_url': args.license_url, 'attribution': args.attribution,
        'rights_reviewed': True, 'purpose': args.purpose})


def luminance(color):
    if not isinstance(color, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
        raise ValueError('Colors must be six-digit HEX values')
    values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return sum(a*b for a,b in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    x, y = sorted((luminance(a), luminance(b)))
    return (y + .05) / (x + .05)


def validate_brief(b):
    errors = []
    for key in ('aspect_ratio_confirmed', 'font_choice_confirmed', 'palette_choice_confirmed'):
        if b.get(key) is not True: errors.append(f'{key} must be true from an explicit answer')
    try:
        ratio = str(b['aspect_ratio'])
        if not re.fullmatch(r'[1-9]\d*(?:\.\d+)?:[1-9]\d*(?:\.\d+)?', ratio): raise ValueError()
        x,y = map(float, ratio.split(':'))
        w,h = b['width'],b['height']
        if type(w) is not int or type(h) is not int or min(w,h) <= 0 or w%2 or h%2: raise ValueError()
        if abs(w/h-x/y) > .001: raise ValueError()
    except (KeyError, ValueError, TypeError, OverflowError): errors.append('Invalid ratio, even dimensions, or aspect mismatch')
    roles = b.get('fonts', {})
    if not isinstance(roles, dict) or any(not isinstance(roles.get(k), str) or not roles[k].strip() for k in ('heading','body','captions')):
        errors.append('Heading, body and caption font roles are required')
    files = b.get('font_files')
    if not isinstance(files, list) or not files or any(not isinstance(p, str) or not Path(p).is_file() for p in files):
        errors.append('Existing local font files are required')
    checks = b.get('font_verification', {})
    if not isinstance(checks, dict) or any(checks.get(k) is not True for k in ('licenses_reviewed','glyphs_checked','renderer_loaded')):
        errors.append('Font license, glyph and renderer checks must be recorded')
    if not isinstance(b.get('theme'), str) or not b['theme'].strip(): errors.append('A selected theme is required')
    ratios = {}
    try:
        palette = b['palette']
        for k in ('background', 'text', 'accent', 'secondary'): luminance(palette[k])
        ratios = {k: round(contrast(palette[k], palette['background']), 3) for k in ('text','accent','secondary')}
        if contrast(palette['text'], palette['background']) < 4.5: errors.append('Normal text/background contrast must be at least 4.5:1')
    except (KeyError, TypeError, ValueError): errors.append('Four valid semantic palette colors are required')
    return {'valid': not errors, 'errors': errors, 'contrast_against_background': ratios,
            'qualification': 'Record validation only; not final font, rights, layout, motion or audio QA'}


def preview_html(presets, pairing_keys, palette_key, title='Your video headline', body='Supporting text shows how narration-led captions will read on screen.'):
    """Build a specimen sheet: one card per pairing, rendered in the chosen palette."""
    import html as H
    pal = presets['palettes'][palette_key]
    fams, cards = {}, []
    for key in pairing_keys:
        p = presets['font_pairings'][key]
        for fam in p['google_dirs']:
            w = p.get('heading_weights', p['weights']) if fam == p['heading'] else p['weights']
            fams.setdefault(fam, set()).update(w)
        cards.append(f"""<section class=c><div class=k>{H.escape(key)} &middot; {H.escape(p['label'])} &middot; {H.escape(p.get('mood',''))}</div>
<h1 style="font-family:'{p['heading']}'">{H.escape(title)}</h1>
<p style="font-family:'{p['body']}'">{H.escape(body)}</p>
<div class=cap style="font-family:'{p['captions']}'">Caption sample 0123456789 &mdash; AaBbCc &amp; ?!</div></section>""")
    q = '&'.join('family=' + urllib.parse.quote(f) + ':wght@' + ';'.join(map(str, sorted(w))) for f, w in fams.items())
    return f"""<!doctype html><meta charset=utf-8><link rel=stylesheet href="https://fonts.googleapis.com/css2?{q}&display=block">
<style>body{{margin:0;padding:32px;background:{pal['background']};color:{pal['text']};display:grid;grid-template-columns:repeat(auto-fill,minmax(560px,1fr));gap:24px}}
.c{{background:{pal.get('surface',pal['background'])};border-left:8px solid {pal['accent']};padding:28px 32px;border-radius:14px}}
.k{{font:600 14px monospace;color:{pal['secondary']};margin-bottom:10px}}h1{{font-size:54px;line-height:1.05;margin:0 0 14px;color:{pal['text']}}}
p{{font-size:22px;line-height:1.45;margin:0 0 14px;opacity:.9}}.cap{{display:inline-block;font-size:18px;background:{pal['accent']};color:{pal['background']};padding:6px 12px;border-radius:6px}}</style>
<body>{''.join(cards)}</body>"""


def acquire_fonts(args, presets):
    pairing = presets['font_pairings'][args.pairing]
    families = list(dict.fromkeys(pairing[k] for k in ('heading','body','captions')))
    hosts = HOSTS | set(args.allow_host)
    entries = []
    for family in families:
        slug = pairing['google_dirs'][family]
        license_url = f'https://raw.githubusercontent.com/google/fonts/main/ofl/{slug}/OFL.txt'
        license_data, final = read_public(license_url, hosts, 200000)
        if b'SIL OPEN FONT LICENSE' not in license_data.upper(): raise ValueError('Expected OFL license not found; review font manually')
        save_asset(license_data, slug+'-OFL.txt', args.out, {'url':final, 'type':'license', 'family':family})
        weights = pairing.get('heading_weights', pairing['weights']) if family == pairing['heading'] else pairing['weights']
        query = urllib.parse.quote(family, safe='') + ':wght@' + ';'.join(map(str, weights))
        css_url = 'https://fonts.googleapis.com/css2?family=' + query + '&display=block'
        css_data, final = read_public(css_url, hosts, 1000000)
        css = css_data.decode('utf-8')
        if '@font-face' not in css: raise ValueError('Expected font-face CSS')
        urls = list(dict.fromkeys(re.findall(r'url\(\s*[\'"]?(https://[^)\s\'"]+)[\'"]?\s*\)', css)))
        if not urls: raise ValueError('No public font URLs found')
        for index,url in enumerate(urls):
            data, resolved = read_public(url, hosts, args.max_bytes)
            kind = file_kind(data)
            if kind not in {'ttf','otf','woff','woff2'}: raise ValueError('Expected font bytes')
            name = f'{slug}-{index}.{kind}'
            entries.append(save_asset(data, name, args.out, {'url':resolved, 'source_url':css_url,
                'type':kind, 'family':family, 'requested_weights':weights, 'license':'OFL-1.1',
                'license_url':license_url, 'license_file':slug+'-OFL.txt', 'rights_reviewed':False,
                'purpose':'User-selected video typography; verify license and glyphs before rendering'}))
            css = css.replace(url, name)
        if re.search(r'https?://|@import', css, flags=re.I): raise ValueError('Unresolved remote CSS reference')
        save_asset(css.encode(), slug+'.css', args.out, {'url':final, 'type':'css', 'family':family})
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--presets', type=Path, default=Path(__file__).resolve().parent.parent/'assets/design-presets.json')
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('presets')
    pv = sub.add_parser('preview'); pv.add_argument('--pairings', nargs='+', required=True); pv.add_argument('--palette', default='studio-light')
    pv.add_argument('--title', default='Your video headline'); pv.add_argument('--out', type=Path, required=True)
    v = sub.add_parser('validate'); v.add_argument('--brief', type=Path, required=True)
    for command in ('fetch','icon','fonts'):
        p = sub.add_parser(command)
        p.add_argument('--out', type=Path, required=True)
        p.add_argument('--allow-host', action='append', default=[])
        p.add_argument('--max-bytes', type=int, default=20*1024*1024)
        if command == 'fonts': p.add_argument('--pairing', required=True)
        else:
            p.add_argument('--name', required=True)
            p.add_argument('--license', required=True)
            p.add_argument('--license-url', required=True)
            p.add_argument('--attribution', default='')
            p.add_argument('--purpose', required=True)
            p.add_argument('--rights-reviewed', action='store_true')
            if command == 'fetch': p.add_argument('--url', required=True)
            else: p.add_argument('--provider', choices=['simpleicons','iconify'], required=True)
    args = parser.parse_args()
    try:
        if args.command == 'presets': result = json.loads(args.presets.read_text())
        elif args.command == 'preview':
            presets = json.loads(args.presets.read_text())
            args.out.write_text(preview_html(presets, args.pairings, args.palette, args.title), encoding='utf-8')
            result = {'html': str(args.out), 'next': 'Render to PNG with a headless browser after fonts load, then inspect and show the PNG'}
        elif args.command == 'validate':
            result = validate_brief(json.loads(args.brief.read_text()))
            print(json.dumps(result, indent=2)); return 0 if result['valid'] else 2
        else:
            if not 1 <= args.max_bytes <= 100*1024*1024: raise ValueError('Size limit must be 1–100 MiB')
            if args.command == 'fonts': result = acquire_fonts(args, json.loads(args.presets.read_text()))
            else:
                name = args.name
                if args.command == 'icon':
                    if args.provider == 'simpleicons':
                        if not re.fullmatch(r'[a-z0-9-]+', name): raise ValueError('Invalid Simple Icons slug')
                        url = f'https://cdn.simpleicons.org/{name}'
                    else:
                        if not re.fullmatch(r'[a-z0-9-]+:[a-z0-9-]+', name): raise ValueError('Use prefix:icon-name')
                        prefix, icon = name.split(':'); url = f'https://api.iconify.design/{prefix}/{icon}.svg'
                    name = name.replace(':','-')+'.svg'
                else: url = args.url
                result = fetch(url, name, args)
        print(json.dumps(result, indent=2)); return 0
    except (ValueError, OSError, KeyError, TypeError, urllib.error.URLError, ET.ParseError):
        # Avoid echoing URLs or provider response bodies, which could contain secrets.
        print('Operation failed: check public access, approved host, size/type, existing filenames, rights metadata and input format.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
