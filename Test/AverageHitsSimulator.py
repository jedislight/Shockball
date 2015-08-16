@@ -0,0 +1,59 @@
import Simulation
import Frameworks.PlayerStatsPrebuilts as Stats

def GetSpread():
    balanced = Simulation.Player(1)
    focused_stam_high = Simulation.Player(1)
    focused_stam_low = Simulation.Player(1)
    focused_stam_mid = Simulation.Player(1)
    specialist_stam_high = Simulation.Player(1)
    specialist_stam_low = Simulation.Player(1)
    
    balanced.SetStats(Stats.balanced)
    focused_stam_high.SetStats(Stats.turtle)
    focused_stam_low.SetStats(Stats.passer)
    focused_stam_mid.SetStats(Stats.sprinter)
    specialist_stam_high.SetStats(Stats.blitzer)
    specialist_stam_low.SetStats(Stats.striker)
    
    spread = {}
    spread["balanced"] = balanced
    spread["focused_stam_high"] = focused_stam_high
    spread["focused_stam_low"] = focused_stam_low
    spread["focused_stam_mid"] = focused_stam_mid
    spread["specialist_stam_high"] = specialist_stam_high
    spread["specialist_stam_low"] = specialist_stam_low
    
    return spread

hit_results = {}
harmony_results = {}
spread = GetSpread()
for key in spread.keys():
    hit_results[key] = []
    harmony_results[key] = []
    
for t in range(10000):
    hits = 0.0
    spread = GetSpread()
    while(spread):
        hits += 1.0
        done = []
        for p in spread.keys():
            harmony = 1 * (1.0 + 0.1*spread[p].run)*(1.0 + 0.1*spread[p].throw)*(1.0 + 0.1*spread[p].pick)
            harmony_results[p].append(harmony)            
            spread[p].TakeDamage()
            if spread[p].run == 0 or spread[p].throw == 0 or spread[p].pick == 0:
                hit_results[p].append(hits)
                done.append(p)
        for d in done:
            del spread[d]
    average_hits = {}
    average_harmony = {}
    for key in hit_results.keys():
        average_hits[key] = sum(hit_results[key]) / len(hit_results[key])
        average_harmony[key] = sum(harmony_results[key]) / len(harmony_results[key])
    print(t)
    print("hits: \n\t", average_hits)  
    print("harmony: \n\t", average_harmony)
