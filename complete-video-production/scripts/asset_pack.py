#!/usr/bin/env python3
"""Validate, package and safely import motion-assets/v1 PNG bundles."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import warnings
import zipfile
from PIL import Image

MAX_ENTRIES = 256
MAX_FILE = 20 * 1024 * 1024
MAX_TOTAL = 200 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 20_000_000


def safe_path(name):
    p = PurePosixPath(name)
    if '\\' in name or p.is_absolute() or any(x in {'', '.', '..'} or x.startswith('.') for x in name.split('/')):
        raise ValueError('Unsafe archive path')
    if not re.fullmatch(r'[A-Za-z0-9_./-]+', name): raise ValueError('Unsupported filename')
    return p


def validate_files(files):
    if 'asset-pack.json' not in files: raise ValueError('Not a motion asset pack: missing root manifest')
    if len(files)>MAX_ENTRIES or sum(map(len,files.values()))>MAX_TOTAL: raise ValueError('Pack limits exceeded')
    for name,data in files.items():
        safe_path(name)
        if len(data)>MAX_FILE: raise ValueError('Individual file limit exceeded')
    m=json.loads(files['asset-pack.json'])
    if m.get('schema')!='motion-assets/v1': raise ValueError('Unsupported pack schema')
    if not isinstance(m.get('complete'),bool) or not isinstance(m.get('missing'),list): raise ValueError('Completion status required')
    if m['complete'] and m['missing']: raise ValueError('Complete pack cannot have missing assets')
    if not m['complete'] and not m['missing']: raise ValueError('Partial pack must explain missing assets')
    if not isinstance(m.get('title'),str) or not m['title'].strip() or not isinstance(m.get('context'),str) or not m['context'].strip(): raise ValueError('Title/context required')
    assets=m.get('assets')
    if not isinstance(assets,list) or not assets: raise ValueError('No assets')
    used={'asset-pack.json'}; ids=set()
    with warnings.catch_warnings():
        warnings.simplefilter('error',Image.DecompressionBombWarning)
        for a in assets:
            if not isinstance(a,dict): raise ValueError('Invalid asset record')
            identity=a.get('id')
            if not isinstance(identity,str) or not re.fullmatch(r'[a-z0-9][a-z0-9-]*',identity) or identity in ids: raise ValueError('Invalid/duplicate asset ID')
            ids.add(identity)
            name=a.get('file','');safe_path(name)
            if not name.startswith('assets/') or not name.endswith('.png') or name in used or name not in files: raise ValueError('Missing/duplicate/non-PNG asset')
            used.add(name);data=files[name]
            if not data.startswith(b'\x89PNG\r\n\x1a\n'): raise ValueError('Not PNG bytes')
            if hashlib.sha256(data).hexdigest()!=a.get('sha256'): raise ValueError('Asset hash mismatch')
            if a.get('reviewed') is not True or a.get('provenance') not in {'generated','supplied','downloaded'}: raise ValueError('Review/provenance required')
            if not isinstance(a.get('source'),str) or not a['source'].strip(): raise ValueError('Source required')
            if a['provenance']!='generated' and a.get('rights_reviewed') is not True: raise ValueError('Supplied/downloaded asset rights review required')
            if not isinstance(a.get('scene_ids'),list) or not a['scene_ids'] or any(not isinstance(s,str) or not s.strip() for s in a['scene_ids']): raise ValueError('Scene mapping required')
            if not isinstance(a.get('purpose'),str) or not a['purpose'].strip(): raise ValueError('Purpose required')
            with Image.open(io.BytesIO(data)) as im:
                if im.format!='PNG' or getattr(im,'n_frames',1)!=1: raise ValueError('Static PNG required')
                im.load()
                if im.width*im.height>20_000_000: raise ValueError('Pixel limit exceeded')
                if type(a.get('width')) is not int or type(a.get('height')) is not int or im.size!=(a['width'],a['height']): raise ValueError('Dimension mismatch')
                alpha=im.convert('RGBA').getchannel('A').getextrema()[0]<255
                if type(a.get('transparent')) is not bool or alpha!=a['transparent']: raise ValueError('Transparency mismatch')
    if set(files)!=used: raise ValueError('Unlisted files rejected')
    return m


def read_folder(folder):
    root=Path(folder)
    files={};total=0
    for p in root.rglob('*'):
        if p.is_symlink(): raise ValueError('Symlinks rejected')
        if not p.is_file(): continue
        if p.stat().st_size>MAX_FILE: raise ValueError('File too large')
        total+=p.stat().st_size
        if total>MAX_TOTAL or len(files)>=MAX_ENTRIES: raise ValueError('Folder limits exceeded')
        name=p.relative_to(root).as_posix();safe_path(name);files[name]=p.read_bytes()
    validate_files(files);return files


def read_zip(path):
    if Path(path).stat().st_size>MAX_FILE: raise ValueError('ZIP exceeds 20 MiB attachment limit')
    files={};total=0
    with zipfile.ZipFile(path) as z:
        if len(z.infolist())>MAX_ENTRIES: raise ValueError('Too many entries')
        seen=set()
        for i in z.infolist():
            name=i.filename.rstrip('/') if i.is_dir() else i.filename
            safe_path(name)
            if name in seen: raise ValueError('Duplicate archive path')
            seen.add(name)
            mode=i.external_attr>>16
            if i.flag_bits&1 or stat.S_ISLNK(mode): raise ValueError('Encrypted/symlink entry rejected')
            if i.is_dir(): continue
            if i.file_size>MAX_FILE or (i.compress_size and i.file_size/i.compress_size>200): raise ValueError('Expansion limit exceeded')
            total+=i.file_size
            if total>MAX_TOTAL: raise ValueError('Expanded size limit exceeded')
            with z.open(i) as f: data=f.read(MAX_FILE+1)
            if len(data)>MAX_FILE: raise ValueError('Actual expanded file too large')
            files[name]=data
    validate_files(files);return files


def write_zip(folder,path):
    target=Path(path)
    if target.exists(): raise ValueError('Output already exists')
    files=read_folder(folder)
    try:
        with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
            for name,data in sorted(files.items()): z.writestr(name,data)
        read_zip(target)
    except Exception:
        target.unlink(missing_ok=True);raise


def import_zip(path,out):
    files=read_zip(path);target=Path(out)
    if target.exists(): raise ValueError('Import destination must be new')
    target.parent.mkdir(parents=True,exist_ok=True)
    temp=Path(tempfile.mkdtemp(dir=target.parent,prefix='png-import-'))
    try:
        for name,data in files.items():
            p=temp/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        temp.rename(target)
    finally:
        if temp.exists(): shutil.rmtree(temp)
    return validate_files(files)


def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    for cmd in ('validate','pack','inspect','import'):
        c=sub.add_parser(cmd)
        if cmd in {'validate','pack'}: c.add_argument('--folder',type=Path,required=True)
        if cmd in {'pack','inspect','import'}: c.add_argument('--zip',type=Path,required=True)
        if cmd=='import': c.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    try:
        if a.command=='validate': m=validate_files(read_folder(a.folder))
        elif a.command=='pack': write_zip(a.folder,a.zip);m=validate_files(read_zip(a.zip))
        elif a.command=='inspect': m=validate_files(read_zip(a.zip))
        else: m=import_zip(a.zip,a.out)
        print(json.dumps({'valid':True,'schema':m['schema'],'assets':len(m['assets']),'complete':m['complete'],'missing':m['missing']},indent=2))
        return 0
    except Exception:
        print('Pack rejected: check schema, paths, limits, PNG bytes, hashes, review records and output destination. No archive code was executed.')
        return 2

if __name__=='__main__': raise SystemExit(main())
