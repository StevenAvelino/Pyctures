from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "Pyctures",
    version = "1.0",
	author = "Kevin Jordil & Steven Avelino",
    description = "Pyctures can edit metadata of images",
    executables = [Executable("main.py", base = "Win32GUI", icon="assets/logo.ico")],
)