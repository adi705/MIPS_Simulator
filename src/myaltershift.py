from cpuElement import CPUElement
from memory import Memory
import unittest
from testElement import TestElement

class Altershift(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), '   alteredshift left should have 2 inputs'
        assert(len(outputValueNames) == 1), ' alteredshiftleft  has only 1 output'
        assert(len(control) == 0), 'alteredshiftleft has no control signal'
        assert(len(outputSignalNames) == 0), 'alteredshiftleft does not have any control output'

        self.inputZero = inputSources[0][1] # input from instruction 25:0
        self.inputOne = inputSources[1][1] # input from adder 31:0
        self.output1 = outputValueNames[0] # 31:28 concatenated with 26 bits left shifted by 2

    
    def writeOutput(self):

       lsbits = self.inputValues[self.inputZero] << 2 #left shifted bits
       topfour = self.inputValues[self.inputOne] & 0xf0000000 # top 4 most significant bits
       fr = lsbits + topfour # final result 32 bit jump address
       self.outputValues[self.output1] = fr


class TestAltershift(unittest.TestCase):
    def setUp(self):
        self.altershift = Altershift()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['input_one ', 'input_two'],
        [],
        []
        )

        self.altershift.connect(
        [(self.testInput, 'input_one'),(self.testInput, 'input_two')],
        ['result_data'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.altershift, 'result_data')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('input_one', 0x3f00080)
        self.testInput.setOutputValue('input_two', 0xbfc00004)
       

        self.altershift.readInput()
     #   self.alu_test.readControlSignals()
        self.altershift.writeOutput()

        self.testOutput.readInput()
     #   self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['result_data']
    

        
        self.assertEqual(output_data, 0xbfc00200)  
        


if __name__ == '__main__':
    unittest.main() 




