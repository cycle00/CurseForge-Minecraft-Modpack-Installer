import json
import os
import requests
import shutil
import sys
import urllib.parse
import zipfile

# sick ass progress bar
def progress(cur, total, mod_name, prev_line_length):
    bar_len = 20
    filled = int(round(bar_len * cur/float(total)))
    percent = round(100.0 * cur/float(total), 1)
    bar = '#' * filled + '-' * (bar_len - filled)
    
    line = "[%s] %s%s (%s/%s) - %s" % (bar, percent, '%', cur, total, mod_name)
    if (prev_line_length > 0 and prev_line_length > len(line)):
        line += ' ' * (prev_line_length - len(line))
    
    sys.stdout.write(line)
    if cur != total:
        sys.stdout.write('\r')
        sys.stdout.flush()
    else:
        sys.stdout.write('\n')

    return len(line)

# some sanity checking
modpack_path = sys.argv[1]
if not os.path.exists(modpack_path):
    print("ERROR: Invalid path to modpack.")
    exit(1)

minecraft_path = sys.argv[2]
if not os.path.exists(minecraft_path):
    print("ERROR: Invalid path to Minecraft.")
    exit(1)

# unzip modpack
modpack_dir = ""
with zipfile.ZipFile(sys.argv[1], 'r') as z:
    print(os.path.basename(modpack_path) + " has been found! Unzipping...")
    modpack_dir = modpack_path.rsplit('.', 1)[0] + '\\'
    z.extractall(modpack_dir)
    print("Done!")

# deserialize manifest.json
if not os.path.exists(modpack_dir + "manifest.json"):
    print("ERROR: This is not a valid modpack! (manifest.json is missing)")
manifest = open(modpack_dir + "manifest.json", 'r')
data = json.load(manifest)
manifest.close()
modpack_name = data["name"]
print(f"Modpack \"{modpack_name}\" has been successfully loaded!")

# parse mods
n_mods = len(data["files"])
print(f"{n_mods} mods/resource packs found. Installing...")
prev_line_length = 0
for index, mod in enumerate(data["files"]):
    # retrieve each mod from curseforge
    url = "https://www.curseforge.com/api/v1/mods/" + str(mod["projectID"]) + "/files/" + str(mod["fileID"]) + "/download"
    response = requests.get(url)
    mod_name = urllib.parse.unquote((response.url).rsplit('/', 1)[1])
    if mod_name.endswith(".jar"):    
        jar = open(os.path.join(minecraft_path, "mods\\", mod_name), 'wb')
        jar.write(response.content)
        jar.close()
    elif mod_name.endswith(".zip"):
        rp = open(os.path.join(minecraft_path, "resourcepacks\\", mod_name), 'wb')
        rp.write(response.content)
        rp.close()

    prev_line_length = progress(index + 1, n_mods, mod_name, prev_line_length)
print("Done!")

# copy overrides to minecraft folder, if they exist
print("Checking for overrides...")
if "overrides" not in data:
    print(f"\nNo overrides found, {modpack_name} has been successfully installed!")
    exit()
print("Overrides found! Copying...")
shutil.copytree(os.path.join(modpack_dir, data["overrides"]), minecraft_path, dirs_exist_ok=True)
print(f"\nDone! \"{modpack_name}\" has been successfully installed!")