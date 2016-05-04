import sys
from cx_Freeze import setup, Executable

includes = ['sys', 'PyQt5', 'PyQt5.Core', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'os', 'os.path', 'datetime', 'textwrap', ]
excludes = []
packages = ['os', 'PyQt5']
path = []
build_exe_options = {
    'includes': includes,
    'excludes': excludes,
    'packages': packages,
    'path': path,
    # 'dll_includes': ['msvcr100.dll'],
    'include_msvcr': True,
    'include_files': [
        (r'C:\Windows\System32\msvcr100.dll', 'msvcr100.dll'),
    ],

}

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

setup(
    name="t411 NFO Builder",
    version="0.2",
    description="Générateur de NFO pour t411",
    options={'build_exe_options': build_exe_options},
    executables=[Executable("main.pyw", base=base, appendScriptToLibrary=False, copyDependentFiles=True)]
)
