#!/usr/bin/env python
'''
Created on Jan 8, 2016

@author: wes
'''

class Fanuc0tb:
  def __init__(self):
    pass
  
  def onOpen(self, argDict={}):
    return ("()\n()\nG20 (Programming in inches)\n"
            "G50 S2000 (Max spindle speed)\nG28 U0. W0. (Go home)\n")
  
  def onClose(self, argDict={}):
    return "\nG28 U0. W0. (Go Home)\n%s\nM30 (End Program)\n%%" % (self.onSpindleStop())
  
  def onRapid(self, argDict={'x':0,'y':0,'z':0}):
    return "G0 X%.3f Z%.3f\n" % (argDict.get('x'),
                               argDict.get('z'))
  
  def onLinear(self, argDict={'x':0,'y':0,'z':0, 'feed':0.001}):
    return "G1 X%.3f Z%.3f F%.3f\n" % (argDict.get('x'),
                               argDict.get('z'),
                               argDict.get('feed'))
    
  def onSpindleStart(self, argDict={'dir':'CW', 'speed':500}):
    return "G99 S%s %s (Feedrate per rev, Start spindle %s)\n" %\
            (argDict.get('speed'), 
            "M3" if argDict.get('dir') == 'CCW' else "M4", argDict.get('dir'))
  
  def onSpindleStop(self, argDict={}):
    return "M5 (Stop Spindle)\n"
  
  def goHome(self, argDict={}):
    return "G28 U0. W0. (Go Home)\n"
  
  def writeBlankLine(self, argDict={}):
    return "\n"
  
  def M0Stop(self, argDict={}):
    return "M0 (Non-optional stop)\n"
    
if __name__ == "__main__":
  testClass = Fanuc0tb()
  outStr = (testClass.onOpen() +
              testClass.writeBlankLine() +
            testClass.onSpindleStart({'dir':'CCW', 'speed':500}) +
              testClass.writeBlankLine() +
            testClass.onRapid({'x':1.5, 'y':0, 'z':0.05}) +
              testClass.writeBlankLine() +
            testClass.onLinear({'x':1.5, 'y':0, 'z':-1, 'feed':0.001}) +
              testClass.writeBlankLine() +
            testClass.goHome() +
              testClass.writeBlankLine() +
            testClass.M0Stop() +
              testClass.writeBlankLine() +
            testClass.onClose())
  print outStr