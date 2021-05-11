from cpuElement import CPUElement
import unittest
from testElement import TestElement


class SignExtend(CPUElement):
    
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), '    signextend should have 1 input'
        assert(len(outputValueNames) == 1), ' signextend  has only 1 output'
        assert(len(control) == 0), ' signextend has 0 control signal'
        assert(len(outputSignalNames) == 0), ' signextend  has 0 control output'

        self.inputZero = inputSources[0][1] #'input '
        
        self.output1 = outputValueNames[0] #'output '
       

        
     
    
    def writeOutput(self):

       address = self.inputValues[self.inputZero]
       if ( address >> 15) == 1:
         address =  -(((~address) & 0xffff) + 1)  # coverts it into 16 bit signed integer

       self.outputValues[self.output1] = address  




class TestAltershift(unittest.TestCase):
    def setUp(self):
        self.signextend = SignExtend()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['input_one'],
        [],
        []
        )

        self.signextend.connect(
        [(self.testInput, 'input_one')],
        ['result_data'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.signextend, 'result_data')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('input_one', 2)
      
       

        self.signextend.readInput()
    
        self.signextend.writeOutput()

        self.testOutput.readInput()
   

        output_data = self.testOutput.inputValues['result_data']
    

        
        self.assertEqual(output_data, 2)  
        


if __name__ == '__main__':
    unittest.main() 


    