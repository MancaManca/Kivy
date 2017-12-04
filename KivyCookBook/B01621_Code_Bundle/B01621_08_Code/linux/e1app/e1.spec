# -*- mode: python -*-
from kivy.tools.packaging.pyinstaller_hooks import install_hooks
install_hooks(globals())

a = Analysis(['/home/hugo/Downloads/linux/linux/e1.py'],
             pathex=['/home/hugo/Downloads/PyInstaller-2.1/e1'],
             hiddenimports=[],
            )
pyz = PYZ(a.pure)
exe = EXE(pyz,
          Tree('/home/hugo/Downloads/linux/linux/'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='e1',
          debug=False,
          strip=None,
          upx=True,
          console=False )
