from cpuElement import CPUElement
import unittest
from testElement import TestElement

class Shift2(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), ' left Shift2 should have 1 input'
        assert(len(outputValueNames) == 1), ' left Shift2  has only 1 output'
        assert(len(control) == 0), ' left shift2 has 0 control signal'
        assert(len(outputSignalNames) == 0), ' left shift2  has 0 control output'

        self.inputZero = inputSources[0][1] # input
        
        self.output1 = outputValueNames[0]  # output
    
    def writeOutput(self):
        # Remove this and replace with your implementation!

      self.outputValues[self.output1] = self.inputValues[self.inputZero] << 2


class TestShift2(unittest.TestCase):
    def setUp(self):
        self.shift2 = Shift2()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['address'],
        [],
        []
        )

        self.shift2.connect(
        [(self.testInput, 'address')],
        ['shiftedAddress'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.shift2, 'shiftedAddress')],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('address', 0x1)

        self.shift2.readInput()
        self.shift2.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['shiftedAddress']
        self.assertEqual(output, 0x4)



if __name__ == '__main__':
    unittest.main()