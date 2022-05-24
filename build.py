import PyInstaller.__main__

args = [
    "--name=pd2builder",
    "--clean",
    "--onefile",
    "builder.py"
]
PyInstaller.__main__.run(args)