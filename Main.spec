# -*- mode: python -*-

## Specification for .exe using pyinstaller

a = Analysis(['Main.py'],
             pathex=['C:\\Users\\SBASTI~1\\DOCUME~1\\WORKSP~1\\STEGOM~1\\STEGOM~1','./',],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)

a.datas += [('pymclevel/classic.yaml', 'pymclevel/classic.yaml', 'DATA')]
a.datas += [('pymclevel/indev.yaml', 'pymclevel/indev.yaml', 'DATA')]
a.datas += [('pymclevel/minecraft.yaml', 'pymclevel/minecraft.yaml', 'DATA')]
a.datas += [('pymclevel/pocket.yaml', 'pymclevel/pocket.yaml', 'DATA')]

# Static link the Visual C++ Redistributable DLLs if on Windows
if sys.platform == 'win32':
	a.binaries += [('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'), ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY')]

pyz = PYZ(a.pure)


exe = EXE(pyz,
          a.scripts,
          a.binaries,
          name='StegoMinecraft.exe',
          debug=False,
          strip=None,
          upx=True,
          exclude_binaries=True,
          console=True )
    
coll = COLLECT(exe,
		a.binaries,
		a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name='StegoMinecraft')
