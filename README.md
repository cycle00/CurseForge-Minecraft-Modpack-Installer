# CurseForge Minecraft Modpack Downloader
Just a quick python script I wrote to automate the process of downloading a Minecraft modpack from CurseForge without actually having to install the CurseForge Launcher. I haven't done much extensive testing but it did successfully install MC Eternal 2 using this and the vanilla launcher.
## Usage
This script requires you to have installed:
* python 3.8+
* requests

Download whatever modpack you want from CurseForge (**make sure it has a manifest.json**).

The syntax is as follows:
```
python modpackinstaller.py "A:\Path\To\Modpack.zip" "B:\Path\To\Minecraft\Instance\"
```
**Make sure the path to your Minecraft instance contains the mods, resourcepacks, saves, etc. just to ensure you don't accidentally install your modpack into a folder that does not contain Minecraft.**

Once the program is done, you are free to delete the original modpack zip and the unzipped folder the program generates in the same folder as the zip. Make sure your forge version is correct and you have allocated enough RAM to Minecraft to ensure that the modpack loads and functions properly.
## Sample Usage
```
python modpackinstaller.py "C:\Users\cycle\Downloads\MC Eternal 2-1.1.1.0.zip" "C:\Users\cycle\AppData\Roaming\.minecraft\MC Eternal 2\"
```
In this example, I created a separate Minecraft instance using the vanilla Minecraft launcher to keep my files organized, I encourage you to do the same for large modpacks.