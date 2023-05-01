import wtm_draw as draw
from wtm_machines import machines

#tm = machines["Beaver 5 2"]
#step, left_shifts, tape, output = tm.run("0")
#print(step, left_shifts, output)
#ones = sum(["0" not in t.s != " " for t in tape])
#print("ones:", ones)

#filename = draw.draw_tm(machines["Binary increment"], input="111")
filename = draw.draw_tm(machines["Beaver 2 2"], input="0")

#filename = draw.draw_tm(machines["Beaver 3 2"], input="0", tileset=True, tiling=True)

#filename = draw.draw_tm(machines["Beaver 4 2"], input="0")
#filename = draw.draw_tm(machines["Beaver 5 2"], input="0")
#filename = draw.draw_tm(machines["Binary adder"], input="101#11", head_pos=5, tileset=True, tiling=True)

import subprocess
subprocess.call(['open', filename])
