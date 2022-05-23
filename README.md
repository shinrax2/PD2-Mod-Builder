# PD2-Mod-Builder
 
this tool packages zip files of payday2 mods and generates a meta.json file for superblt auto updates

# requirements:
- Python 3

# usage:
write a config file for your mod and run this script from the commandline like this

    python builder.py -c yourconfigfile.json

if you also want to bump your mod to a higher version run this script from the commandline like this

    python builder.py -c yourconfigfile.json -v your.mod.version

# config file:
rename config.sample.json to your liking and replace the values with real ones

- moddir: absolute path to your mod directory
- builddir: absolute path to where your mod will be built
- metafile: absolute path to where your meta.json file will be written
- metaident: update identifier for your mod (case sensitive)
- zipfile: name of the zip file you want your mod to have without file extension e.g. "examplemod" not "examplemod.zip"
- zipdir: absolute path to where the zip file will be written
- copy_files: list of files to copy for your mod relative to moddir
- copy_dirs: list of folders to copy for your mod relative to moddir

for windows users:

either use forward slahes or double backslashes for your paths 

e.g. "c:/windows" or "c:\\windows" not "c:\windows"
