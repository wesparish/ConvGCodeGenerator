#!/usr/bin/env python

import importlib

class ConvGCodeGenerator:
  VALID_MACHINE_TYPES = ['lathe','mill']
  VALID_OPERATIONS = ['newtooltest']
  VALID_CONTROLLERS = ['fanuc0tb']
  
  def __init__(self, options=[]):
    self.options = options
    # [lathe, mill]
    self.machineType = options.machineType
    # [Newtooltest]
    self.operation = options.operation
    # [Fanuc0tb]
    self.controller = options.controller
    
  def getCodeGenerator(self):
    module = importlib.import_module("%s.%s" % (self.machineType, self.operation))
    class_ = getattr(module, self.operation)
    return class_()
  
  def getOutputFormatter(self):
    module = importlib.import_module("controllers.%s" % (self.controller))
    class_ = getattr(module, self.controller)
    return class_()    
  
  def start(self):
    codeGenerator = self.getCodeGenerator()
    outputFormatter = self.getOutputFormatter()
    
    outputCodeList = codeGenerator.generateCode()
    gCodeToWrite = outputFormatter.onOpen()
    for line in outputCodeList:
      gCodeToWrite += getattr(outputFormatter, line[0])(line[1])
    gCodeToWrite += outputFormatter.onClose()
    print gCodeToWrite

if __name__ == "__main__":
  #print "ConvGCodeGenerator starting..."
  from optparse import OptionParser
  parser = OptionParser()
  parser.add_option("-t", "--machine-type", dest="machineType",
                    help="type of machine: [lathe, mill]", default="lathe")
  parser.add_option("-o", "--operation", dest="operation", default="Newtooltest",
                    help="operation: [Newtooltest]")
  parser.add_option("-c", "--controller", dest="controller", default="Fanuc0tb",
                    help="controller types: [Fanuc-0T-B]")
  
  (options, args) = parser.parse_args()
  
  if options.machineType.lower() not in ConvGCodeGenerator.VALID_MACHINE_TYPES:
    raise Exception('Unknown machineType: %s, valid options: %s' % 
                    (options.machineType, ConvGCodeGenerator.VALID_MACHINE_TYPES))
    
  if options.operation.lower() not in ConvGCodeGenerator.VALID_OPERATIONS:
    raise Exception('Unknown operation: %s, valid options: %s' % 
                    (options.operation, ConvGCodeGenerator.VALID_OPERATIONS))
    
  if options.controller.lower() not in ConvGCodeGenerator.VALID_CONTROLLERS:
    raise Exception('Unknown controller: %s, valid options: %s' % 
                    (options.controller, ConvGCodeGenerator.VALID_CONTROLLERS))
  
  convGCodeGenerator = ConvGCodeGenerator(options)
  convGCodeGenerator.start()
  
  #print "ConvGCodeGenerator finishing..."