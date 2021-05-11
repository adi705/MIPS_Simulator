import unittest
from cpuElement import CPUElement
import common
from testElement import TestElement

class Alu(CPUElement):  
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)


        assert(len(inputSources) == 2), 'alu should have 2 inputs'
        assert(len(outputValueNames) == 1), 'alu has only 1 output'
        assert(len(control) == 1), 'alu has one control signal'
        assert(len(outputSignalNames) == 1), 'alu does  have  control output'

        self.inputZero = inputSources[0][1] # data1 
        self.inputOne = inputSources[1][1]  # data2 
      
        self.outputNameone = outputSignalNames[0]  # zerodata 1 control signal

        self.outputNametwo = outputValueNames[0]   # output data 2

        self.controlName = control[0][1]   # alu contol signal 4 bit

    def writeOutput(self):
        AluControl = self.controlSignals[self.controlName] # 4 bit direct control signal from main 
                                                            # control unit bypassing the inner level
        
        assert(isinstance(AluControl, int))
        assert(not isinstance(AluControl, bool))  # ...  (not bool)
    #    assert( AluControl == 0 AluControl == 1 or AluControl == 2 AluControl == 6 AluControl == 7), 'Invalid Alu control signal value: %d' % (muxControl,)
        
        if AluControl == 0: #AND
            self.outputControlSignals[self.outputNameone] = 0
            self.outputValues[self.outputNametwo] = self.inputValues[self.inputZero] & self.inputValues[self.inputOne]

        elif AluControl == 1:  # OR
            self.outputControlSignals[self.outputNameone] = 0
            self.outputValues[self.outputNametwo] = self.inputValues[self.inputZero] | self.inputValues[self.inputOne]

        elif AluControl == 2:  # add and addi 
            self.outputControlSignals[self.outputNameone] = 0
            self.outputValues[self.outputNametwo] = self.inputValues[self.inputZero] + self.inputValues[self.inputOne]

        elif AluControl == 7:  # set less than 
            self.outputControlSignals[self.outputNameone] = 0
            if self.inputValues[self.inputZero] < self.inputValues[self.inputOne]:
                self.outputValues[self.outputNametwo] = 1
            else:
                self.outputValues[self.outputNametwo] = 0       
       
        elif AluControl == 6:  # subtract
            self.outputValues[self.outputNametwo] = self.inputValues[self.inputZero] - self.inputValues[self.inputOne] 
            #print('output result of alu is : %d' % self.outputValues[self.outputNametwo])
            if self.outputValues[self.outputNametwo] == 0:
                self.outputControlSignals[self.outputNameone] = 1
                #print("         bruhhhhhhhhhhhhhhh          ")
                #print('output_zero flag = %d' % (self.outputControlSignals[self.outputNameone],))
            else:
                self.outputControlSignals[self.outputNameone] = 0 

        elif AluControl == 3:  # add unsigned and add iu
            self.outputControlSignals[self.outputNameone] = 0
            self.outputValues[self.outputNametwo] = ((self.inputValues[self.inputZero] & 0xffffffff) + (self.inputValues[self.inputOne] & 0xffffffff)) & 0xffffffff         




        elif AluControl == 8:  # subtract unsigned
            self.outputValues[self.outputNametwo] = ((self.inputValues[self.inputZero] & 0xffffffff) - (self.inputValues[self.inputOne] & 0xffffffff))         
            if self.outputValues[self.outputNametwo] == 0:
                 self.outputControlSignals[self.outputNameone] = 1
            else:
                 self.outputControlSignals[self.outputNameone] = 0  



class TestAlu(unittest.TestCase):
    def setUp(self):
        self.alu_test = Alu()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['input_one ', 'input_two'],
        [],
        ['input_control_signal']
        )

        self.alu_test.connect(
        [(self.testInput, 'input_one'),(self.testInput, 'input_two')],
        ['alu_result_data'],
        [(self.testInput, 'input_control_signal')],
        ['alu_result_zero']
        )

        self.testOutput.connect(
        [(self.alu_test, 'alu_result_data')],
        [],
        [(self.alu_test, 'alu_result_zero')],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('input_one', 54)
        self.testInput.setOutputValue('input_two', 54)
        self.testInput.setOutputControl('input_control_signal', 2)  #addition

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']

        self.testInput.setOutputControl('input_control_signal', 3)  #addition unsigned

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']
        
        self.assertEqual(output_data, 108)  
        self.assertEqual(output_zero, 0)    

        self.testInput.setOutputControl('input_control_signal', 6)  #subtraction

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']
        
        self.assertEqual(output_data, 0)  
        self.assertEqual(output_zero, 1) 

     


        self.testInput.setOutputValue('input_one', 24)
        self.testInput.setOutputValue('input_two', 24)

        self.testInput.setOutputControl('input_control_signal', 8)  #subtraction unsigned

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']
        
        self.assertEqual(output_data, 0)   #weird
        self.assertEqual(output_zero, 1)  # weird

        self.testInput.setOutputValue('input_one', 3)
        self.testInput.setOutputValue('input_two', 2)

        self.testInput.setOutputControl('input_control_signal', 0)  #AND

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']
        
        self.assertEqual(output_data, 2)  
        self.assertEqual(output_zero, 0)

        self.testInput.setOutputControl('input_control_signal', 1)  #OR

        self.alu_test.readInput()
        self.alu_test.readControlSignals()
        self.alu_test.writeOutput()

        self.testOutput.readInput()
        self.testOutput.readControlSignals()

        output_data = self.testOutput.inputValues['alu_result_data']
        output_zero = self.testOutput.controlSignals['alu_result_zero']
        
        self.assertEqual(output_data, 3)  
        self.assertEqual(output_zero, 0)                
            



if __name__ == '__main__':
    unittest.main() 










    
