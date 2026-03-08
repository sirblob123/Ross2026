import sympy as sp

order = 'RRLRRRLRRRLLLLLLLRLLLRRR' #change this as needed
theta = 0
total = 0
for c in order:  #Runs for each letter
    if c == 'R':
        d = sp.cos(sp.rad(theta+22.5)) + sp.sin(sp.rad(theta+22.5)) 
        #Distance change for new letter (use 22.5 instead of 45 since this isnt tracking direction faced)
        total += d #Update
        theta += 45
    else:        
        d = sp.cos(sp.rad(theta-22.5)) + sp.sin(sp.rad(theta-22.5)) #Identical but for L
        total += d
        theta -= 45

print(sp.Mod(theta,360), total.evalf()) #Return final answer (note that 0.e-124)

