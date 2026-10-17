import hashlib, io, json, tempfile, unittest, zipfile
from pathlib import Path
from PIL import Image
import asset_pack as a

class AssetPackTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.addCleanup(self.t.cleanup);self.root=Path(self.t.name)
        im=Image.new('RGBA',(64,64),(30,90,120,0));b=io.BytesIO();im.save(b,format='PNG');self.png=b.getvalue()
        self.m={'schema':'motion-assets/v1','title':'Test pack','context':'Illustrative fixture only','complete':True,'missing':[],
          'assets':[{'id':'scene-one','file':'assets/one.png','scene_ids':['scene-01'],'purpose':'Fixture illustration','width':64,'height':64,'transparent':True,'provenance':'generated','source':'Generated test fixture','reviewed':True,'sha256':hashlib.sha256(self.png).hexdigest()}]}
    def files(self):return {'asset-pack.json':json.dumps(self.m).encode(),'assets/one.png':self.png}
    def test_pack_import_roundtrip(self):
        f=self.root/'pack';(f/'assets').mkdir(parents=True)
        for n,d in self.files().items():(f/n).write_bytes(d)
        z=self.root/'pack.zip';a.write_zip(f,z);result=a.import_zip(z,self.root/'imported')
        self.assertEqual(result['schema'],'motion-assets/v1');self.assertEqual((self.root/'imported/assets/one.png').read_bytes(),self.png)
    def test_hash_mismatch(self):
        self.m['assets'][0]['sha256']='bad'
        with self.assertRaises(ValueError):a.validate_files(self.files())
    def test_real_png_required(self):
        f=self.files();f['assets/one.png']=b'jpeg pretending to be png'
        with self.assertRaises(ValueError):a.validate_files(f)
    def test_review_required(self):
        self.m['assets'][0]['reviewed']=False
        with self.assertRaises(ValueError):a.validate_files(self.files())
    def test_transparency_checked(self):
        self.m['assets'][0]['transparent']=False
        with self.assertRaises(ValueError):a.validate_files(self.files())
    def test_missing_rows_prevent_complete(self):
        self.m['missing']=['Background']
        with self.assertRaises(ValueError):a.validate_files(self.files())
    def test_partial_pack_allowed(self):
        self.m['complete']=False;self.m['missing']=['Background']
        self.assertFalse(a.validate_files(self.files())['complete'])
    def test_traversal_rejected(self):
        for n in ('../escape.png','/abs.png','assets/../../x.png','assets\\x.png','.git/config'):
            with self.assertRaises(ValueError):a.safe_path(n)
    def test_zip_duplicate_rejected(self):
        z=self.root/'duplicate.zip'
        with zipfile.ZipFile(z,'w') as f:
            f.writestr('asset-pack.json',b'{}');f.writestr('asset-pack.json',b'{}')
        with self.assertRaises(ValueError):a.read_zip(z)
    def test_unlisted_executable_rejected(self):
        f=self.files();f['run.py']=b'print(1)'
        with self.assertRaises(ValueError):a.validate_files(f)
    def test_symlink_rejected(self):
        z=self.root/'symlink.zip'
        with zipfile.ZipFile(z,'w') as f:
            i=zipfile.ZipInfo('assets/one.png');i.external_attr=0o120777<<16;f.writestr(i,b'/etc/passwd')
        with self.assertRaises(ValueError):a.read_zip(z)
    def test_dimension_mismatch(self):
        self.m['assets'][0]['width']=128
        with self.assertRaises(ValueError):a.validate_files(self.files())
if __name__=='__main__':unittest.main()
