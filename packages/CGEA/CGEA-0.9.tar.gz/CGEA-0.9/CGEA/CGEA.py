from lib.featureBasedCGEA import featureBasedCGEA
from lib.fishersBasedCGEA import fishersBasedCGEA
from lib.file import write_JSON, read_file
from lib.errorHandling import printException
import time, re, os, threading, getopt
from copy import deepcopy
from operator import itemgetter
from multiprocessing import cpu_count, Value as mpVal
from ctypes import c_double
#saveAs can also be a list.
#outputDir specifies output directory. If None, does not save an output.
#if returnResults is True, will store results in memory and return them. This is memory intensive.
#data allows you to specify alternate datafiles

    


    
def runCGEA(upgenes = None, downgenes = None, druglist = None, saveAs = "json", sort = 'up', outputDir = None, prefix = 'CGEAResults', data = {}, verbose = False):
    myCGEA = CGEA_async(upgenes = upgenes, downgenes = downgenes, druglist = druglist, saveAs = saveAs, sort = sort, prefix = prefix, outputDir = outputDir)
    myCGEA.start()
    prevStatus = ''
    while (myCGEA.status[2]<1.0):
        if verbose:
            curStatus = myCGEA.status[1]
            if not curStatus == prevStatus:
                print curStatus
                prevStatus = curStatus
        time.sleep(1)
    return [myCGEA.results, myCGEA.filepaths]
    
class CGEA_async(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = True
        self.myCGEA = CGEA(*args, **kwargs)
        self.status = self.myCGEA.status
        self.results = self.myCGEA.results
        self.filepaths = self.myCGEA.filepaths
        
    def run(self):
        self.myCGEA.run()


class CGEA():
    def __init__(self, upgenes = None, downgenes = None, druglist = None, saveAs = "json", sort = 'up', outputDir = None, prefix = 'CGEAResults', data = {}, numWorkers = cpu_count()):
                 
        self.upgenes = upgenes
        self.downgenes = downgenes
        self.druglist = druglist
        self.status = ['PENDING','Initialized', 0.0]
        self.saveAs = saveAs
        self.outputDir = outputDir
        self.sort = sort
        self.prefix = str(prefix)
        self.data = data
        self.filepaths = []
        self.results = {}
        self.numWorkers = numWorkers
        self.saveFunction = {'json': self.writeEnrichmentsToJSON,
                             'jsons': self.writeEnrichmentsToJSONs
                             }
    
    def writeResults(self):
        #print 'keys of results is ' + str(self.results.keys())
        self.saveFunction[self.saveAs]()
    
    def writeEnrichmentsToJSONs(self):
        filepaths = []
        for name, result in self.results.items():
            if len(self.prefix) > 0: filepath = self.outputDir+re.sub('\s+', '_', '_'.join([self.prefix,name])+'.json')
            else: filepath = self.outputDir+re.sub('\s+', '_', name+'.json')
            self.filepaths.append(filepath)
            write_JSON(self.outputDir+re.sub('\s+', '_', ' '.join(self.prefix,name)+'.json'), result)

    def writeEnrichmentsToJSON(self):
        filepath = self.outputDir+self.prefix+'.json'
        write_JSON(filepath, self.results)
        self.filepaths.append(filepath)
    
    def run(self):
        self.status[0] = 'RUNNING'
        try:
            if self.upgenes == None and self.downgenes == None and self.druglist == None:
                raise RuntimeError("No input given to CGEA.")
            elif not (self.upgenes == None and self.downgenes == None):
                self.results.update(featureBasedCGEA(self.upgenes, self.downgenes, self.saveAs, self.outputDir, self.sort, self.data, self.status, numWorkers = self.numWorkers))
            else:
                self.results.update(fishersBasedCGEA(self.druglist, self.saveAs, self.outputDir, self.sort, self.data, self.status, numWorkers = self.numWorkers))
            if self.saveAs and os.path.isdir(self.outputDir):
                curTime = time.time()
                self.writeResults()
                #print 'Wrote Results - took ' + str(time.time()-curTime)
                self.status[0] = 'SUCCESS'
                self.status[1] = 'Finished'
                self.status[2] = 1.0
            #print "Finished"
        except Exception as e:
            printException()
            print e
            self.status[0] = 'ERROR'
            self.status[1] = e
            self.status[2] = 1.0
        #return results

if __name__ == '__main__' :
    upgenes = "data/sampledata/up_genes.txt"
    downgenes = "data/sampledata/down_genes.txt"
    druglist = None
    #upgenes = None
    #downgenes = None
    #druglist = "data/sampledata/drug_list.txt"

    saveAs = "json"
    outputDir = "data/sampledata/sampleout/"
    curTime = time.time()
    [results, _] = runCGEA(upgenes = upgenes, downgenes = downgenes, druglist = druglist, saveAs = saveAs, sort = 'up', prefix = '1', outputDir = outputDir, verbose = True)
#     myCGEA = CGEA(upgenes = upgenes, downgenes = downgenes, druglist = druglist, saveAs = saveAs, sort = 'up', prefix = '1', outputDir = outputDir)
#     print myCGEA.status
#     myCGEA.start()
#     while not myCGEA.status[0] == 'SUCCESS':
#         time.sleep(10)
#         print myCGEA.status[2]
    #print '\n'.join(map(lambda x: ' '.join([x['Name'], str(x['Adjusted P-Value']), str(x['Adjusted P-Value'])]),sorted(results['Annotated Compounds'], key = itemgetter('Score'))[0:10]))
    
    print 'Total time: ' + str(time.time()-curTime)
    