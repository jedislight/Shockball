import Simulation

def GetSpread():
    balanced = Simulation.Player(1)
    focused_stam_high = Simulation.Player(1)
    focused_stam_low = Simulation.Player(1)
    focused_stam_mid = Simulation.Player(1)
    specialist_stam_high = Simulation.Player(1)
    specialist_stam_low = Simulation.Player(1)
    
    focused_stam_high.stamina =3
    focused_stam_high.pick =1
    
    focused_stam_low.stamina = 1
    focused_stam_low.pick = 3
    
    focused_stam_mid.pick = 1
    focused_stam_low.throw = 3
    
    specialist_stam_high.stamina = 3
    specialist_stam_high.pick = 3
    specialist_stam_high.run = 1
    specialist_stam_high.throw = 1
    
    specialist_stam_low.stamina = 1
    specialist_stam_low.pick = 1
    specialist_stam_low.run = 3
    specialist_stam_low.throw = 3
    
    spread = {}
    spread["balanced"] = balanced
    spread["focused_stam_high"] = focused_stam_high
    spread["focused_stam_low"] = focused_stam_low
    spread["focused_stam_mid"] = focused_stam_mid
    spread["specialist_stam_high"] = specialist_stam_high
    spread["specialist_stam_low"] = specialist_stam_low
    
    return spread

results = {}
spread = GetSpread()
for key in spread.keys():
    results[key] = []
    
for t in range(10000):
    hits = 0
    spread = GetSpread()
    while(spread):
        hits += 1
        done = []
        for p in spread.keys():
            spread[p].TakeDamage()
            if spread[p].run == 0 or spread[p].throw == 0 or spread[p].pick == 0:
                results[p].append(hits)
                done.append(p)
        for d in done:
            del spread[d]
    averages = {}
    for key in results.keys():
        averages[key] = sum(results[key]) / len(results[key])
    print(averages)    
