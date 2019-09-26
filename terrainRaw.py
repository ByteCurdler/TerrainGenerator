import random
from math import floor

if "reps" in _GET:
    reps = int(_GET["reps"])
else:
    reps = 2
map = [[0]]

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
        tmp.append([0]*len(map)*2)
    for x in range(len(map)*2):
        for y in range(len(map)*2):
            preX, preY = floor(x/2), floor(y/2)
            tmp2 = [map[preX][preY]]
            if preX != 0:
                tmp2.append(map[preX-1][preY])
            if preX != len(map)-1:
                tmp2.append(map[preX+1][preY])
            if preY != 0:
                tmp2.append(map[preX][preY-1])
            if preY != len(map)-1:
                tmp2.append(map[preX][preY+1])
            tmp[x][y] = (sum(tmp2) / len(tmp2)) + random.random() - 0.5
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
    scale = 0.25/2**reps
    for x in range(len(map)):
        for y in range(len(map)):
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
