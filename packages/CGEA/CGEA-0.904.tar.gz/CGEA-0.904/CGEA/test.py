from CGEA import testGeneListCGEA, testDrugListCGEA

if __name__ == '__main__' :
    testGeneListCGEA(numWorkers = 1, async = False)
    testDrugListCGEA(numWorkers = 1, async = False)