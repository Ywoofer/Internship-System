from cx_Freeze import setup, Executable
import sys


base = None
if sys.platform == "win32":
    base = "Win32GUI"


include_files = ["staj.db", "assets/favicon.ico"]  


executables = [Executable("staj_ilan_sistemi.py", base=base, icon="assets/favicon.ico")]  

setup(
    name="Staj İlan Sistemi",
    version="1.0",
    description="Staj ilanları yönetim sistemi",
    options={"build_exe": {"include_files": include_files}},
    executables=executables
)
