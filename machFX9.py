'''
main issue here was to global patforrec. youll probs forget. 
'''

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from numpy import loadtxt
import time



totalStart = time.time()

date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
                              delimiter=',',
                              converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})
avgLine = ((bid+ask)/2)

patternAr = []
performanceAr = []
patForRec = []


def percentChange(startPoint,currentPoint):
    try:
        x = ((float(currentPoint)-startPoint)/abs(startPoint))*100.00
        if x == 0.0:
            return 0.000000001
        else:
            return x
    except:
        return 0.0001


def patternStorage():
    '''
    The goal of patternFinder is to begin collection of %change patterns
    in the tick data. From there, we also collect the short-term outcome
    of this pattern. Later on, the length of the pattern, how far out we
    look to compare to, and the length of the compared range be changed,
    and even THAT can be machine learned to find the best of all 3 by
    comparing success rates.'''

    startTime = time.time()
    
    
    x = len(avgLine)-30
    y = 11
    currentStance = 'none'
    
    while y < x:
        pattern = []
        p1 = percentChange(avgLine[y-10], avgLine[y-9])
        p2 = percentChange(avgLine[y-10], avgLine[y-8])
        p3 = percentChange(avgLine[y-10], avgLine[y-7])
        p4 = percentChange(avgLine[y-10], avgLine[y-6])
        p5 = percentChange(avgLine[y-10], avgLine[y-5])
        p6 = percentChange(avgLine[y-10], avgLine[y-4])
        p7 = percentChange(avgLine[y-10], avgLine[y-3])
        p8 = percentChange(avgLine[y-10], avgLine[y-2])
        p9 = percentChange(avgLine[y-10], avgLine[y-1])
        p10= percentChange(avgLine[y-10], avgLine[y])

        outcomeRange = avgLine[y+20:y+30]
        currentPoint = avgLine[y]

        try:
            avgOutcome = reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)
        except Exception, e:
            print str(e)
            avgOutcome = 0
        futureOutcome = percentChange(currentPoint, avgOutcome)

        '''
        print 'where we are historically:',currentPoint
        print 'soft outcome of the horizon:',avgOutcome
        print 'This pattern brings a future change of:',futureOutcome
        print '_______'
        print p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
        '''

        pattern.append(p1)
        pattern.append(p2)
        pattern.append(p3)
        pattern.append(p4)
        pattern.append(p5)
        pattern.append(p6)
        pattern.append(p7)
        pattern.append(p8)
        pattern.append(p9)
        pattern.append(p10)



        patternAr.append(pattern)
        performanceAr.append(futureOutcome)
        
        y+=1

    endTime = time.time()
    print len(patternAr)
    print len(performanceAr)
    print 'Pattern storing took:', endTime-startTime


def currentPattern():
    mostRecentPoint = avgLine[-1]

    

    cp1 = percentChange(avgLine[-11],avgLine[-10])
    cp2 = percentChange(avgLine[-11],avgLine[-9])
    cp3 = percentChange(avgLine[-11],avgLine[-8])
    cp4 = percentChange(avgLine[-11],avgLine[-7])
    cp5 = percentChange(avgLine[-11],avgLine[-6])
    cp6 = percentChange(avgLine[-11],avgLine[-5])
    cp7 = percentChange(avgLine[-11],avgLine[-4])
    cp8 = percentChange(avgLine[-11],avgLine[-3])
    cp9 = percentChange(avgLine[-11],avgLine[-2])
    cp10= percentChange(avgLine[-11],avgLine[-1])

    patForRec.append(cp1)
    patForRec.append(cp2)
    patForRec.append(cp3)
    patForRec.append(cp4)
    patForRec.append(cp5)
    patForRec.append(cp6)
    patForRec.append(cp7)
    patForRec.append(cp8)
    patForRec.append(cp9)
    patForRec.append(cp10)



def graphRawFX():
    
    fig=plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)
    ax1.plot(date,bid)
    ax1.plot(date,ask)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.grid(True)
    for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    ax1_2 = ax1.twinx()
    ax1_2.fill_between(date, 0, (ask-bid), facecolor='g',alpha=.3)

    plt.subplots_adjust(bottom=.23)
    plt.show()



    
def patternRecognition():
    for eachPattern in patternAr:
        sim1 = 100.00 - abs(percentChange(eachPattern[0], patForRec[0]))
        sim2 = 100.00 - abs(percentChange(eachPattern[1], patForRec[1]))
        sim3 = 100.00 - abs(percentChange(eachPattern[2], patForRec[2]))
        sim4 = 100.00 - abs(percentChange(eachPattern[3], patForRec[3]))
        sim5 = 100.00 - abs(percentChange(eachPattern[4], patForRec[4]))
        sim6 = 100.00 - abs(percentChange(eachPattern[5], patForRec[5]))
        sim7 = 100.00 - abs(percentChange(eachPattern[6], patForRec[6]))
        sim8 = 100.00 - abs(percentChange(eachPattern[7], patForRec[7]))
        sim9 = 100.00 - abs(percentChange(eachPattern[8], patForRec[8]))
        sim10 = 100.00 - abs(percentChange(eachPattern[9], patForRec[9]))
        howSim = (sim1+sim2+sim3+sim4+sim5+sim6+sim7+sim8+sim9+sim10)/10.00

        if howSim > 70:
            patdex = patternAr.index(eachPattern)
            print patdex
            
            print '##################################'
            print '##################################'
            xp = [1,2,3,4,5,6,7,8,9,10]
            fig = plt.figure()
            plt.plot(xp, patForRec)
            plt.plot(xp, eachPattern)
            plt.show()
            print patForRec
            print '==================================='
            print '==================================='
            print eachPattern
            print '----------'
            print 'predicted outcome:',performanceAr[patdex]
            print '##################################'
            print '##################################'
            



            
patternStorage()
currentPattern()
patternRecognition()
totalEnd = time.time()-totalStart
print 'Entire processing took:',totalEnd,'seconds'
    
