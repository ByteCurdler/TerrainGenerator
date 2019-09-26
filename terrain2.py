#!/usr/bin/env python3
import cgi,sys,os
import cgitb
cgitb.enable()
print("Content-Type: text/html")
print("")

def _goto(link, reDir = True, relative=False):
    if(relative):
        i = "'" + link + "'"
    else:
        if(link.startswith("https://") or link.startswith("http://")):
            i = "'" + link + "'"
        else:
            i = "'http://" + link + "'"
    if(reDir):
        print("<script>window.location.replace(" + i + ");</script>")
    else:
        print("<script>window.location = " + i + ";</script>")

def _status(dct,value):
    if(value in dct):
        return dct[value]
    else:
        return False

def _cleanup(raw):
    ret = {}
    raw = raw.replace("+"," ")
    tmp = ""
    i = -1
    while i < len(raw) - 1:
        i += 1
        j = i
        char = raw[i]
        if char == "%":
           try:
               char = chr(int(raw[i+1] + raw[i+2], 16))
               i += 2
           except:
               tmp += char
               continue
        else:
           tmp += char
           continue
        if(raw[j:j+6] == "%0D%0A"):
           continue
        elif(char == "&"):
            char = ""
        elif(char == "="):
            char = ""
        elif(char == "%"):
            char = ""
        tmp += char
    for j in tmp.split("&"):
        i = j.replace("","&").replace("","%")
        if("=" in i):
            ret.update({i.split("=")[0].replace("","="):"=".join(i.split("=")[1:]).replace("","=")})
        else:
            ret.update({i:True})
    if(ret == {'':True}):
        ret = {}
    return ret

RAW_POST = sys.stdin.read()
_POST = _cleanup(RAW_POST)

RAW_GET = os.getenv('QUERY_STRING')
_GET = _cleanup(RAW_GET)
import random
from math import floor

if "reps" in _GET:
    reps = int(_GET["reps"])
else:
    reps = 2
if "w" in _GET:
    w = int(_GET["w"])
else:
    w = 2
if "h" in _GET:
    h = int(_GET["h"])
else:
    h = 2
if "flux" in _GET:
    flux = float(_GET["flux"])
else:
    flux = 0.1
if "range" in _GET:
    rnge = float(_GET["range"])
else:
    rnge = 4
map = []
for i in range(w):
    map.append([])
    for j in range(h):
        map[-1].append((random.random()*2*rnge)-rnge)
print("""<style>
td {
    width:38px;
    height:40px;
    color:white;
    text-align:right;
}
table, a-scene {
    border:blue outset;
}
a-scene {
    width:800px;
    height:600px;
}
</style>
<script src="https://aframe.io/releases/0.6.1/aframe.min.js"></script>""")

def expand(map):
    tmp = []
    for _ in range(len(map)*2):
        tmp.append([0]*len(map[0])*2)
    for x in range(len(map)*2):
        for y in range(len(map[0])*2):
            preX, preY = floor(x/2), floor(y/2)
            tmp2 = [map[preX][preY]/2]
            if preX != 0:
                tmp2.append(map[preX-1][preY])
            if preX != len(map)-1:
                tmp2.append(map[preX+1][preY])
            if preY != 0:
                tmp2.append(map[preX][preY-1])
            if preY != len(map[0])-1:
                tmp2.append(map[preX][preY+1])
            tmp[x][y] = (sum(tmp2) / (len(tmp2)-0.5)) + (random.random()*flux*2) - flux
            tmp[x][y] = round(tmp[x][y]*10)/10
    return tmp

def disp():
    try:
        mult_pos = 255 / max([max([max(j, 0) for j in i]) for i in map])
    except ZeroDivisionError:
        mult_pos = 0
    try:
        mult_neg = 255 / max([max([max(-j, 0) for j in i]) for i in map])
    except ZeroDivisionError:
        mult_neg = 0
    print("<table>")
    for row in map:
        print("<tr>")
        for cell in row:
            print("<td style='background-color:rgb({},{},{})'>{}</td>".format(
                abs(min(cell*mult_neg, 0)), 0, max(cell*mult_pos, 0), cell
            ))
        print("</tr>")
    print("</table>")

def a_frame():
    def hexify(n):
        tmp = hex(int(n))[2:]
        return "0" * (2-len(tmp)) + tmp
    try:
        mult_pos = 255 / max([max([max(j, 0) for j in i]) for i in map])
    except ZeroDivisionError:
        mult_pos = 0
    try:
        mult_neg = 255 / max([max([max(-j, 0) for j in i]) for i in map])
    except ZeroDivisionError:
        mult_neg = 0
    print("""<a-scene embedded>
<a-sky src='360-palace.jpg'></a-sky>
<a-plane position='0 0 0' color='#a67328' width=4 height=4 rotation="-90 0 0"></a-plane>
<a-entity oculus-touch-controls='hand: right' position='0 1.60 0'><a-entity rotation="-45 0 0" position="-0.125 -0.0625 -0.0625">""")
    scale = (0.25/(w*h)**0.5)/2**reps
    for x in range(len(map)):
        for y in range(len(map[0])):
            cell = map[x][y]
            print("<a-box scale='{scale} {height} {scale}' position='{x} {value} {y}' rotation='0 0 0' color='#{r}55{b}'></a-box>".format(
                r=hexify(abs(min(cell*mult_neg, 0))), b=hexify(max(cell*mult_pos, 0)), value=cell*(scale), x=x*scale, y=y*scale, scale=scale, height=scale/3
            ))
##    print("</a-entity></a-entity><a-entity position='0 1.6 -4' rotation='20 0 0'>")
##    scale = 1/2**reps
##    for x in range(len(map)):
##        for y in range(len(map)):
##            cell = map[x][y]
##            print("<a-box scale='{scale} {height} {scale}' position='{x} {value} {y}' rotation='0 0 0' color='#{r}55{b}'></a-box>".format(
##                r=hexify(abs(min(cell*mult_neg, 0))), b=hexify(max(cell*mult_pos, 0)), value=cell*(scale), x=x*scale, y=y*scale, scale=scale, height=scale/3
##            ))
    print("</a-entity></a-scene>")
for i in range(reps):
    map = expand(map)
disp()
a_frame()
