from cx_Freeze import setup, Executable

# Kör denna fil för att skapa en exe.
# Man kör den genom att skriva: python execute.py build
# Då skapas en ny mapp som heter 'build'. I den ligger en till mapp som heter exe punkt någonting.
# I den ligger en .exe fil som heter 'runner' som kan köras genom att dubellklicka på den eller skriva runner.exe i terminalen.


base = None

executables = [Executable("runner.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'includes':["matplotlib.backends.backend_tkagg"],
        'packages':packages,
    },
}

setup(
    name = "<any name>",
    options = options,
    version = "<any number>",
    description = '<any description>',
    executables = executables
)
