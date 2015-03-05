# -*- mode: python -*-
import os

a = Analysis(['./main.py'],
             pathex=[os.path.dirname(__name__)], # Set the path to the current dir. Will need to update if moved.
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
a.datas += [("timed_bosses.json", "timed_bosses.json", "DATA")]

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GW2 Events.exe',
          debug=False,
          strip=None,
          upx=False,
          console=False,
          icon="assets\icons\Gw2.ico"
          )