from cx_Freeze import setup, Executable

base = None

executables = [Executable("Twitter_selenium.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "twitter",
    options = options,
    version = "1.00",
    description = 'selenium',
    executables = executables
)