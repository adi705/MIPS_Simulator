from cpuElement import CPUElement
import unittest
from testElement import TestElement

class Shift16(CPUElement):
  
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), '    left Shift16 should have 1 input'
        assert(len(outputValueNames) == 1), ' left Shift16  has only 1 output'
        assert(len(control) == 0), ' left shift16 has 0 control signal'
        assert(len(outputSignalNames) == 0), ' left shift16  has 0 control output'

        self.inputZero = inputSources[0][1] #input 
        
        self.output1 = outputValueNames[0] #output 
       

        
      
    
    def writeOutput(self):
       

      self.outputValues[self.output1] = self.inputValues[self.inputZero] << 16
    #  print('Upper Imm: %s' % hex(self.outputValues[self.output1]))


class TestShift16(unittest.TestCase):
    
    def setUp(self):
      self.testInput =  TestElement()
      self.testOutput = TestElement()
      self.shift16 = Shift16()

      self.testInput.connect(
        [],
        ['inputaddress'],
        [],
        []

        )

      self.shift16.connect(
        [(self.testInput, 'inputaddress')],
        ['shifted_output'],
        [],
        []
        )

      self.testOutput.connect(
        [(self.shift16, 'shifted_output')],
        [],
        [],
        []
        )

    def test_correct_behaviour(self):
        self.testInput.setOutputValue('inputaddress', 1) 
        self.shift16.readInput()
        self.shift16.writeOutput()
        self.testOutput.readInput()


        output = self.testOutput.inputValues['shifted_output']
        self.assertEqual(output, 65536)




if __name__ == '__main__':
    unittest.main()







