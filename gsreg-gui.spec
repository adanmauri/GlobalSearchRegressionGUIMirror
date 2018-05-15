# -*- mode: python -*-

block_cipher = None

added_files = [
    ( 'assets', 'assets' ),
    ( 'src', 'src' ),
    ( 'templates', 'templates')
]

a = Analysis(['main.py'],
             pathex=['/home/adanmauri/Documentos/GUI_QT'],
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
