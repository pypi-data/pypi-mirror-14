from featureBasedCGEA import CGEAdata
from statistics import makeMixmdl


data = CGEAdata()
cmap = data.get('cmap')
unifiedCompoundLevelSets = data.get("unifiedCompoundLevelSets")
mixmdls = data.getModel('mixmdl')
setSizes = reduce(lambda x,y: set.union(x,set(map(len,y.values()))), unifiedCompoundLevelSets.values(), set())
makeMixmdl(cmap.keys(), data.getPath('mixmdl'), setSizes = setSizes, numIterations = 100000)