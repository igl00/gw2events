from subprocess import call
import os
import sys


def resource_path(relative_path):
    '''Get absolute path to resource, works for dev and for PyInstaller'''
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def compile_assets():
    '''Compiles all *.qrc files in the directory and subdirectories to *_rc.py files'''

    print("Compiling assets...")
    for dirpath, dirnames, filenames, in os.walk("."):
        for filename in [f for f in filenames if f.endswith(".qrc")]:
            call(["C:\\Python34\\Lib\\site-packages\\PySide\\pyside-rcc.exe", "-py3",
                 os.path.join(dirpath, filename),
                 "-o", os.path.join(dirpath, filename.split(".")[0] + "_rc.py")])
    print("Assets compiled!")

def compile_ui():
    '''Compiles the ui files into pyside python files.'''
    for dirpath, dirnames, filenames, in os.walk("./ui"):
        for filename in [f for f in filenames if f.endswith(".ui")]:
            print("Compiling %s" % filename)
            call(["C:\\Python34\\Scripts\\pyside-uic.exe",
                 os.path.join(dirpath, filename),
                 "-o", os.path.join(dirpath, filename.split(".")[0] + "Gui.py")])
    print("Ui Compiled!")

if __name__ == '__main__':
    compile_ui()
    compile_assets()