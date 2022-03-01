import os
import shutil
import subprocess
import zipfile

shutil.rmtree("./KuchiPaku/lib", True)

subprocess.call(["python", "-m", "ensurepip", "--user"])
subprocess.call(["python", "-m", "pip", "install", "--upgrade", "pip"])
subprocess.call(
    [
        "python",
        "-m",
        "pip",
        "install",
        "--upgrade",
        "-t",
        "KuchiPaku/lib",
        "librosa",
        "numba==0.53",
    ]
)

zf = zipfile.ZipFile("./KuchiPaku.zip", "w")
for dirname, subdirname, filenames in os.walk("./KuchiPaku"):
    for filename in filenames:
        zf.write(os.path.join(dirname, filename))
zf.close()
