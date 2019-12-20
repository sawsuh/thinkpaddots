import subprocess as sp
import time

recordcmd = [
    "slop",
    "-t",
    "0",
    "-b",
    "3",
    "-c",
    "0.9296875,0.890625,0.89453125,1",
    "-f",
    "%w %h %x %y",
    "--nokeyboard",
]
recording = sp.run(recordcmd, stdout=sp.PIPE, stderr=sp.DEVNULL)
width, height, topx, topy = recording.stdout.decode("utf-8").split(" ")

width = int(width) - 6
height = int(height) - 6
topx = int(topx) + 3
topy = int(topy) + 3

sp.Popen(["urxvt", "-name", "float"])
time.sleep(0.250)

widcommand = sp.run(["xdotool", "getwindowfocus"],
                    stdout=sp.PIPE, stderr=sp.DEVNULL)
wid = hex(int(widcommand.stdout.decode("utf-8")))
geomstring = f"0,{topx},{topy},{width},{height}"
sp.run(["wmctrl", "-i", "-r", wid, "-e", geomstring])
middlex = topx + width / 2
middley = topy + height / 2
sp.run(["xdotool", "mousemove", str(middlex), str(middley)])
sp.run(["xdotool", "windowactivate", wid])
