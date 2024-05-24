import os
import numpy as np
import multiprocessing as mp
import time

def splitRangeIntoTasks(startValue, endValue, numberOfWorkers):
    #split range between startValue/endValue into multiple tasks   
    splitArrs = np.array_split(np.arange(startValue, endValue + 1), numberOfWorkers)
    tasks = [[i[0], i[-1]] for i in splitArrs]
    return tasks


def isPrimeNumberMP(value):
    if value < 2:
        return False
    for iCheckIfDivider in range(2, value):
        if (value % iCheckIfDivider) == 0:
            return False
    return True


def _countPrimesInRangeMP(startValue, endValue):
    countOfPrimes = 0
    for iValue in range(startValue, endValue + 1): #+1 required to test the endValue, too
        if isPrimeNumberMP(iValue):
            countOfPrimes += 1
    return countOfPrimes


def countPrimesInRangeMP(startValue, endValue): 
    countOfPrimes = _countPrimesInRangeMP(startValue, endValue)
    
    #print status of this worker
    processID = os.getpid() #ID of the process given by the Operation system
    message = "Worker (ID: %s) found %i primes from %i to %i"%(processID, countOfPrimes, startValue, endValue)
    print(message)

    return countOfPrimes, message


def countPrimesInRange_withSharedVars(startValue, endValue, sharedValue, messageQueue):
    countOfPrimes = _countPrimesInRangeMP(startValue, endValue)
    
    #store numberOfPrimes in multiprocessing value
    sharedValue.value += countOfPrimes
    
    #produce message
    processID = os.getpid()
    message = "Worker (ID: %s) found %i primes from %i to %i"%(processID, countOfPrimes, startValue, endValue)
    
    #store message in multiprocessing queue
    messageQueue.put(message)





#Multiprocessing classes-------------------------------------------------
class OwnWorker1(mp.Process):
    def __init__(self, tasks):
        super().__init__()       
        self.tasks = tasks
        self.results = []

    def run(self):
        for iValue in self.tasks:
            incValue = iValue + 1
            self.results.append(incValue)
        print('Done')



class OwnWorker2(mp.Process):
    def __init__(self, pipeWorker):
        super().__init__()       
        self.pipeWorker = pipeWorker
        self.isRunning = True

    def run(self):
        while self.isRunning:
            if self.pipeWorker.poll(timeout=0.5): #timeout is important, if not CPU load gets to 100%, alternative: use time.sleep(0.5)
                task = self.pipeWorker.recv()
                if isinstance(task, str): #check if close signal was send
                    if task == 'close':
                        self.isRunning = False
                else:
                    self.processTasks(task)
            #time.sleep(0.5)

        self.pipeWorker.send('worker is closed!')
        self.close()
            
    def processTasks(self, task):
        results = []
        for iValue in task:
            incValue = iValue + 1
            results.append(incValue)
        self.pipeWorker.send(results)
    
    



