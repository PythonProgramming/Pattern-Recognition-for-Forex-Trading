'''
Welcome to part 4 of machine learning for forex and stock trading and analysis.

Now that we've seen our data, let's talk about our goals.

Generally, with machine learning, everything boils down to actually:
Machine Classification.

With quant analysis, generally the first few things you are taught are
"patterns" Right, head and shoulders, teacup.... and whatever else.

There are tons.

So what is the theory behind these patterns? The idea is that the prices
of stocks or various forex ratios are a direct reflection of the psychology
of the people trading, ie: the traders
(either people or computers)are making  decisions, based on
a bunch of variables. The theory is that, when those same variables present
themselves again, we get a repeat of actions that creates a similar
"pattern" ... then the outcome as well is likely to be similar, because the
variables are almost the same.

So what we're going to do here is

1. Create a machine learned batch of what will end up being millions of
algorithms with their results, which can be used to predict future outcomes.

2. Test this completely.

The beauty of machine learning, is that the worry about "data snooping". Data snooping occurs when the analyst
makes new inferences after peaking at the data. With Machine learning, DS is
built in, and already accounted for. Our entire system is really built on
the inference of pattern recognition, so if patterns change due to new data,
that's really built in and is done by programming that was done before results.

This allows researches to get the best of both worlds, while avoiding the
pitfalls of data snooping. 

This allows backtesting to actually
serve a very truthful and accurate purpose. If a machine learned live algo
passes the back test, it is highly likely to continue performing well in the
future, not because it passed a back test, but because our hypothesis REALLY
and entire model
passed the backtest... unlike finding the best algo at the time and backtesting
for great results. 

With that, what we will do is take a range of data in succession, and create
a pattern with it. How we're going to do this is going to be with % change

We want to have the data normalized as best we can, so it can be used
no matter what the price was. If we required prices to be the same, whew that
would be rare to see too much identical. We could do this
logarithmically, or keep it super simple with % change, so we'll do that.

To start, we'll do forward percent change, from starting point.
This means, the longer the pattern,
the more likely the END is to be less similar, but the actual direction
of the pattern will be more similar. This can be useful, since
some patterns might take more time to react than others, and we want the
build up to be most accurate, but we might acctually prefer the end to be
more accurate in the future, so we could do reverse percent change. We can
also do a point-to-point percent change as well. Trust me, when it comes to
variables, we're gonna be very busy.

For now, forward and
starting point. Now what that means is first we just need to store a
bunch of patterns, in their percent change format. In reality, and in our back
test that will eventually mimic it, your patterns can only come from the past.

Then, what we'll do to compare patterns is how similar the % changes are.

Again, this can also be done logarithmically, and might be better that way,
but the goal here is to keep things as simple as possible right now. 

'''


import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import numpy as np
from numpy import loadtxt
import time

date,bid,ask = np.loadtxt('GBPUSD1d.txt', unpack=True,
                              delimiter=',',
                              converters={0:mdates.strpdate2num('%Y%m%d%H%M%S')})


def percentChange(startPoint,currentPoint):
    return ((currentPoint-startPoint)/startPoint)*100.00
    



def patternFinder():
    '''
    The goal of patternFinder is to begin collection of %change patterns
    in the tick data. From there, we also collect the short-term outcome
    of this pattern. Later on, the length of the pattern, how far out we
    look to compare to, and the length of the compared range be changed,
    and even THAT can be machine learned to find the best of all 3 by
    comparing success rates.
    '''
    
    #Simple Average
    avgLine = ((bid+ask)/2)
    
    #This finds the length of the total array for us
    x = len(avgLine)-30
    #This will be our starting point, allowing us to compare to the
    #past 10 % changes. 
    y = 11
    # where we are in a trade. #
    # can be none, buy,
    currentStance = 'none'
    while y < x:
        
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

        #function to account for the average of the items in the array
        print reduce(lambda x, y: x + y, outcomeRange) / len(outcomeRange)

        
        print currentPoint
        print '_______'
        print p1, p2, p3, p4, p5, p6, p7, p8, p9, p10
        time.sleep(55)
        
        y+=1
        
        
        
    
    
    
    



def graphRawFX():
    
    fig=plt.figure(figsize=(10,7))
    ax1 = plt.subplot2grid((40,40), (0,0), rowspan=40, colspan=40)
    ax1.plot(date,bid)
    ax1.plot(date,ask)
    
    #ax1.plot(date,((bid+ask)/2))
    ax1.plot(date,percentChange(ask[0],ask),'r')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    #####
    plt.grid(True)
    for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)
    plt.gca().get_yaxis().get_major_formatter().set_useOffset(False)
    #######
    ax1_2 = ax1.twinx()
    #ax1_2.plot(date, (ask-bid))
    ax1_2.fill_between(date, 0, (ask-bid), facecolor='g',alpha=.3)
    #ax1_2.set_ylim(0, 3*ask.max())
    #######
    plt.subplots_adjust(bottom=.23)
    #plt.grid(True)
    plt.show()
    




    
    
