import sympy as sp
import math

order = 'RRLRRRLRRRLLLLLLLRLLLRRR' #Change this as needed
theta = 0
total = 0
x,y=0.0,0.0
visited = [(x,y)]
intersections = 0
tolerance = 1e-5
for c in order:  #Runs for each letter
    if c == 'R':
        d = sp.cos(sp.rad(theta+22.5)) + sp.sin(sp.rad(theta+22.5)) 
        dx=d*sp.cos(sp.rad(theta+22.5))
        dy=d*sp.sin(sp.rad(theta+22.5))
        #Distance change for new letter (use 22.5 instead of 45 since this isnt tracking direction faced)
        total += d #Update
        theta += 45
    else:        
        d = sp.cos(sp.rad(theta-22.5)) + sp.sin(sp.rad(theta-22.5)) #Identical but for L
        dx=d*sp.cos(sp.rad(theta-22.5))
        dy=d*sp.sin(sp.rad(theta-22.5))
        total += d
        theta -= 45
    x += dx
    y += dy
    for prev_x, prev_y in visited[:-1]: #Check for intersections with previous points (except the most recent one)
        dist = math.hypot(x - prev_x, y - prev_y)
        if dist < tolerance:
            intersections += 1
    visited.append((x, y))


print(sp.Mod(theta,360), total.evalf(),intersections) #Return final answer (note that 0.e-124 or 0.e-125, etc is identical to zero)
