#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#PD2-Mod-Builder by shinrax2

import os
import shutil
import argparse
import json
import hashlib
import sys

def getfiles(dirpath):
    f =  []
    for root, dirs, files in os.walk(dirpath):
        for file in files:
            if os.path.isfile(os.path.join(root, file)):
                f.append(os.path.join(root, file))
    f.sort(key=str.lower)
    return f

def hashdir(path):
    hashstr = ""
    files = getfiles(path)
    for file in files:
        thash = hashlib.sha256()
        with open(file, "rb") as f:
            for line in iter(lambda: f.read(65536), b''):
                thash.update(line)
        hashstr += thash.hexdigest()
    h = hashlib.sha256()
    h.update(bytes(hashstr, "ascii"))
    return h.hexdigest()

#setup argparse
parser = argparse.ArgumentParser(description="buildscript for Real Weapon Names")
parser.add_argument("-v", action="store", help="Version to bump to")
parser.add_argument("-c", action="store", help="config file")
args = parser.parse_args()

print("PD2-Mod-Builder by shinrax2")
#load config
if args.c != None and os.path.isfile(args.c):
    with open(args.c, "r", encoding="utf8") as f:
        config = json.loads(f.read())
        print("loaded config \""+args.c+"\"")
else:
    print("please specify a configuration file with the \"-c\" option")
    sys.exit(1)

#create clean config["builddir"]
if os.path.exists(config["builddir"]):
    shutil.rmtree(config["builddir"])
os.mkdir(config["builddir"])

#version bump
if args.v != None:
    print("bumping mod version to \""+args.v+"\"")
    with open(os.path.join(config["moddir"], "mod.txt"), "r", encoding="utf8") as f:
        modtxt =  json.loads(f.read())
    modtxt["version"] = str(args.v)
    with open(os.path.join(config["moddir"], "mod.txt"), "w", encoding="utf8") as f:
        f.write(json.dumps(modtxt, sort_keys=False, indent=4))

#copy files
print("copying files")
for file in config["copy_files"]:
    shutil.copy2(os.path.join(config["moddir"], file), os.path.join(config["builddir"], file))
for dir in config["copy_dirs"]:
    shutil.copytree(os.path.join(config["moddir"], dir), os.path.join(config["builddir"], dir))

#compute sha256 hash and write new meta file
print("generating hash")
hash = hashdir(config["builddir"])
with open(config["metafile"], "w", encoding="utf8") as f:
    f.write(json.dumps([{"ident": config["metaident"], "hash": hash}], sort_keys=True, indent=4))
print("metafile written to \""+config["metafile"]+"\"")

#build zip
print("building zip file")
shutil.make_archive(config["zipfile"], "zip", root_dir=os.path.abspath(os.path.join(config["builddir"], "..")), base_dir=os.path.basename(config["builddir"]))
if os.path.exists(os.path.join(config["zipdir"], config["zipfile"]+".zip")):
    os.remove(os.path.join(config["zipdir"], config["zipfile"]+".zip"))
shutil.move(os.path.join(os.getcwd(), config["zipfile"]+".zip"), os.path.join(config["zipdir"], config["zipfile"]+".zip"))
print("zipfile wrote to \""+os.path.join(config["zipdir"], config["zipfile"]+".zip")+"\"")

#cleanup
if os.path.exists(config["builddir"]):
    shutil.rmtree(config["builddir"])