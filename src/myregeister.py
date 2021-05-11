
import unittest
from cpuElement import CPUElement
import common
from testElement import TestElement

class RegisterFile(CPUElement):
    def __init__(self):
        # Dictionary mapping register number to register value
        self.register = {}
        
        # All registers default to 0
        for i in range(0, 32):
            self.register[i] = 0
  
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)


        assert(len(inputSources) == 4), 'reg file should have 4 inputs'
        assert(len(outputValueNames) == 2), 'reg file has only 2 output'
        assert(len(control) == 1), 'reg file has one control signal'
        assert(len(outputSignalNames) == 0), 'reg file does not have any control output'

        self.inputZero = inputSources[0][1] #'register read port1 '
        self.inputOne = inputSources[1][1]  #'register read port2 '
        self.inputtwo = inputSources[2][1]  #' register write port'

        self.inputthree = inputSources[3][1] # ' write data port'
        self.outputNameone = outputValueNames[0] # 'read data 1'
        self.outputNametwo = outputValueNames[1]  # 'read data 2'
        self.controlName = control[0][1]  # 'regwrite contol signal'

    def writeOutput(self):
        regControl = self.controlSignals[self.controlName]
       # print(regControl)

        assert(isinstance(regControl, int))
        assert(not isinstance(regControl, bool))  # ...  (not bool)
     
        number = self.inputValues[self.inputZero]  # number variable stores  the register number
        self.outputValues[self.outputNameone] = self.register[number] # 32 bit data read from first register
        number2 = self.inputValues[self.inputOne]  # number variable stores  the register number
        self.outputValues[self.outputNametwo] = self.register[number2] # 32 bit data data read from second register

        if regControl == 1 :
           writeregnum = self.inputValues[self.inputtwo] # register number of the write process
           self.register[writeregnum] = self.inputValues[self.inputthree]  # 32 data written to the write register
         #  print(self.inputValues[self.inputthree])

        
       
        
    def printAll(self):
        '''
        Print the name and value in each register.
        '''
        
        # Note that we won't actually use all the registers listed here...
        registerNames = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                        '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                        '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                        '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']
        
        print()
        print("Register file")
        print("================")
        for i in range(0, 32):
            print("%s \t=> %s (%s)" % (registerNames[i], common.fromUnsignedWordToSignedWord(self.register[i]), hex(int(self.register[i]))[:-1]))
        print("================")
        print()
        print()
        
class TestRegisterFile(unittest.TestCase):
    
    def setUp(self):
       
        self.registerfile = RegisterFile()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['rreg1','rreg2','wreg','wdata'],
        [],
        ['reg_write']
        )

        self.registerfile.connect(
        [(self.testInput, 'rreg1'), (self.testInput, 'rreg2'), (self.testInput, 'wreg'), (self.testInput, 'wdata')],
        ['read_data1', 'read_data2'],
        [(self.testInput, 'reg_write')],
        []
        )

        self.testOutput.connect(
        [(self.registerfile, 'read_data1'),(self.registerfile, 'read_data2')],
        [],
        [],
        []
        )


    def test_correct_behavior(self):
        self.testInput.setOutputControl('reg_write', 1)
        self.testInput.setOutputValue('rreg1', 4)
        self.testInput.setOutputValue('rreg2', 5)

        self.testInput.setOutputValue('wreg', 6)
        self.testInput.setOutputValue('wdata', 500)
      #  self.register[4] = 78
      #  self.register[5] = 89
      

        self.registerfile.readInput()
        self.registerfile.readControlSignals()
        self.registerfile.writeOutput()
        self.testOutput.readInput()
      
        output1 = self.testOutput.inputValues['read_data1']
        output2 = self.testOutput.inputValues['read_data2']
        
        self.assertEqual(output1, 78)
        self.assertEqual(output2, 78)

        self.registerfile.printAll()
        

















if __name__ == '__main__':
    unittest.main()
