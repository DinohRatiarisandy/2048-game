import sys
from cx_Freeze import setup, Executable

# Chemin vers l'icône
icon_path = "issets/icon-game.ico"

# Nom de votre fichier exécutable
exe_name = "Play 2048"

# Paramètres de configuration de Cx_Freeze
build_exe_options = {"packages": ["pygame"], "excludes": None, "include_files": [icon_path, 'requirements.txt', '2048-icon.png', 'high_score.txt']}

# Création de l'exécutable
base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = Executable(script="main.py", base=base, targetName=exe_name, icon=icon_path)

setup(name="2048 on windows",
      version="1.0",
      description="Jeu 2048 fait par pygame de python",
      options={"build_exe": build_exe_options},
      executables=[exe])
