#!/usr/bin/env python

import Newtooltest
import math

'''
This class will generate lathe code for new tool testing
'''
class Newtooltest:
  def __init__(self):
    pass
    
  def generateCode(self, rawStockDiameter=1.25, startZ=0, endZ=-1, 
                   minDepthOfCut=0.02, maxDepthOfCut=0.02, rpm=1000, 
                   startingfeedPerRev=.001, maxFeedPerRev=0.025, 
                   stopAfterEachPass=True):
    # Note: Not using minDepthOfCut at this time
    maxPossiblePasses = int(math.floor(rawStockDiameter / maxDepthOfCut))
    maxPassesByFeedRate = int(math.floor((maxFeedPerRev - 
                                          startingfeedPerRev) * 1000))
    
    # g-code array to return
    retVal = []
    numPasses = min(maxPossiblePasses,maxPassesByFeedRate)
    for index in xrange(numPasses):
      currX = rawStockDiameter - maxDepthOfCut * index
      # Setup
      retVal.append(("onRapid", 
                    {'x':rawStockDiameter+0.05, 
                     'y':0, 
                     'z':startZ+0.05}))
      # Move to start of pass
      retVal.append(("onLinear", {'x':currX,
                                  'y':0,
                                  'z':startZ,
                                  'feed':startingfeedPerRev + index * 0.001}))
      # Make pass
      retVal.append(("onLinear", {'x':currX,
                                  'y':0,
                                  'z':endZ,
                                  'feed':startingfeedPerRev + index * 0.001}))
      # Move out of pass
      retVal.append(("onLinear", {'x':rawStockDiameter + 0.05,
                                  'y':0,
                                  'z':endZ,
                                  'feed':startingfeedPerRev + index * 0.001}))
      # Go to home
      retVal.append(("goHome",{}))
      # Stop spindle
      retVal.append(("onSpindleStop",{}))
      # M0 Stop
      retVal.append(("M0Stop",{}))
      # Blank line
      retVal.append(("writeBlankLine",{}))
      
    return retVal
  
if __name__ == "__main__":
  testClass = Newtooltest()
  retVal = testClass.generateCode()
  for item in retVal:
    print item