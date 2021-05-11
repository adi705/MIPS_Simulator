from cpuElement import CPUElement
from memory import Memory
import unittest
from testElement import TestElement

class Alterand(CPUElement):
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 0), '   alteredand left should have 0 inputs'
        assert(len(outputValueNames) == 0), ' alteredand  has only 0 output'
        assert(len(control) == 3), 'alteredand has 3 control signal'
        assert(len(outputSignalNames) == 1), 'alteredand has one control output'

        self.inputZero = control[0][1] # input from branch control signal
        self.inputOne = control[1][1] # input from branch not equal control signal
        self.inputTwo = control[2][1] # zero input control signal from alu
        self.output1 = outputSignalNames[0] # output branch contol signal
       
    
    def writeOutput(self):


       if self.controlSignals[self.inputZero] == 1 and self.controlSignals[self.inputTwo] == 1 :  # beq and zero flag is 1
          self.outputControlSignals[self.output1] = 1  # control signal set as 1 which activates branching
          

       if self.controlSignals[self.inputOne] == 1 and self.controlSignals[self.inputTwo] == 0 :  # bne is 1 and zero flag is 0
          self.outputControlSignals[self.output1] = 1   # control signal set as 1 which activates branching 

       if self.controlSignals[self.inputOne] == 0 and self.controlSignals[self.inputTwo] == 0 :  # bne is 0 and zero flag is 0
          self.outputControlSignals[self.output1] = 0   # control signal set as 1 which activates branching 
       if self.controlSignals[self.inputZero] == 0 and self.controlSignals[self.inputTwo] == 1 :  # beq is 0 and zero flag is 1
          self.outputControlSignals[self.output1] = 0   # control signal set as 1 which activates branching     
   

       



class TestAlterand(unittest.TestCase):
    def setUp(self):
        self.alterand = Alterand()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        [],
        [],
        ['branche', 'branchne','zero_flag']
        )

        self.alterand.connect(
        [],
        [],
        [(self.testInput, 'branche'),(self.testInput, 'branchne'),(self.testInput, 'zero_flag')],
        ['result_signal']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.alterand, 'result_signal')],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputControl('branche', 1)
        self.testInput.setOutputControl('branchne', 0)
        self.testInput.setOutputControl('zero_flag', 0)

        self.alterand.readInput()
        self.alterand.readControlSignals()
        self.alterand.writeOutput()
        self.testOutput.readControlSignals()
        output = self.testOutput.controlSignals['result_signal']
        
        self.assertEqual(output, 0)




if __name__ == '__main__':
    unittest.main()          