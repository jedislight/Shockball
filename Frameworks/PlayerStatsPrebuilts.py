from AI import PlayerStats

def __MakeStats(pick=2, run=2, stamina=2, throw=2):
    stats = PlayerStats()
    stats.pick = pick
    stats.run = run
    stats.stamina = stamina
    stats.throw = throw
    stats.__doc__ = "foo"
    return stats

#balanced
balanced =    __MakeStats(pick=2, run=2, stamina=2, throw=2)

#focused
stealer =     __MakeStats(pick=3, run=2, stamina=2, throw=1)
passer =      __MakeStats(pick=3, run=2, stamina=1, throw=2)
avenger =     __MakeStats(pick=3, run=1, stamina=2, throw=2)
assistant =   __MakeStats(pick=2, run=3, stamina=1, throw=2)
sprinter =    __MakeStats(pick=2, run=3, stamina=2, throw=1)
vangaurd =    __MakeStats(pick=1, run=3, stamina=2, throw=2)
infiltrator = __MakeStats(pick=1, run=2, stamina=3, throw=2)
turtle =      __MakeStats(pick=2, run=1, stamina=3, throw=2)
smasher =     __MakeStats(pick=2, run=2, stamina=3, throw=1)
resupplier =  __MakeStats(pick=2, run=2, stamina=1, throw=3)
cannon =      __MakeStats(pick=2, run=1, stamina=2, throw=3)
forward =     __MakeStats(pick=1, run=2, stamina=2, throw=3)

#specialists
blitzer =     __MakeStats(pick=1, run=3, stamina=3, throw=1)
striker =     __MakeStats(pick=1, run=3, stamina=1, throw=3)
catapault =   __MakeStats(pick=1, run=1, stamina=3, throw=3)
retailiator = __MakeStats(pick=3, run=1, stamina=1, throw=3)
rebounder =   __MakeStats(pick=3, run=1, stamina=3, throw=1)
dervish =     __MakeStats(pick=3, run=3, stamina=1, throw=1)




