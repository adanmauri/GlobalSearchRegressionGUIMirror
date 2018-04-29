# -*- mode: python -*-

block_cipher = None

added_files = [
    ( 'htmlPy/binder.js', 'htmlPy' ),
    ( 'templates/*', 'templates' ),
    ( 'static', 'static' ),
    ( 'scripts', 'scripts' )
]

a = Analysis(['gsreg-gui.py'],
             pathex=['/home/adanmauri/Documentos/julia/GSRegGUI'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='gsreg-gui',
          debug=False,
          strip=False,
          upx=True,
          console=False
          )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='gsreg-gui')
