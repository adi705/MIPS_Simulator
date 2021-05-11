from cpuElement import CPUElement
from memory import Memory
import sys
import unittest
from testElement import TestElement
class InstructionMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 1), ' InstructionMemory should have 1 input'
        assert(len(outputValueNames) == 7), ' InstructionMemory has only 7 outputs'
        assert(len(control) == 0), 'InstructionMemory has no control signal'
        assert(len(outputSignalNames) == 0), 'InstructionMemory does not have any control output'

        self.inputZero = inputSources[0][1] #'read address port'



        self.output1 = outputValueNames[0] #'control signal or opcode '
        self.output2 = outputValueNames[1] # ' read register 1'
        self.output3 = outputValueNames[2]  #'read register 2 or mux upper input'
      #  self.output4 = outputValueNames[3]  'mux upper input'
        self.output4 = outputValueNames[3]  # 'mux lower input'
        self.output5 = outputValueNames[4]  # 'sign extend'
        self.output6 = outputValueNames[5]   #   'alu control'

        self.output7 = outputValueNames[6]    #  'jump address'

        
      
    
    def writeOutput(self):
       

        # faddress is one of the serialized memory locations available in the instruction memory
        faddress = self.inputValues[self.inputZero] 
        # each fadress corresponds or maps to a specific instruction which in itself is a 32 bit binary code
     #   rbicode = self.memory.get(faddress, 0) # resulting binary code
        rbicode = self.memory[faddress]

        if rbicode == 13:
            sys.exit() 
        
        self.outputValues[self.output1] = rbicode >> 26  # 6 bit opcode as an input to control unit
        self.outputValues[self.output2] = (rbicode >> 21) & 31 # 25:21
        self.outputValues[self.output3] = (rbicode >> 16) & 31 # 20:16
        self.outputValues[self.output4] = (rbicode >> 11) & 31 # 15:11  as the write register
        self.outputValues[self.output5] = rbicode & 65535 # 15:0 which is the 16 bit offset
        self.outputValues[self.output6] = rbicode  & 63 # 6 bit code to alu unit known as funct 5:0 field 
        self.outputValues[self.output7] = rbicode  & 67108863 # 25:0 jmp address


class TestInstructionMemory(unittest.TestCase):
    def setUp(self):
        self.instructionmemory = InstructionMemory('add.mem')
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['input_one'],
        [],
        []
        )

        self.instructionmemory.connect(
        [(self.testInput, 'input_one')],
        ['opcode','read1','read2','muxlower','signextend','alucontrol','jumpaddress'],
        [],
        []
        )

        self.testOutput.connect(
        [(self.instructionmemory, 'opcode'), (self.instructionmemory, 'read1'),(self.instructionmemory, 'read2'),
        (self.instructionmemory, 'muxlower'),(self.instructionmemory, 'signextend'),(self.instructionmemory, 'alucontrol'),
        (self.instructionmemory, 'jumpaddress') ],
        [],
        [],
        []
        )

    def test_correct_behavior(self):
        
        self.testInput.setOutputValue('input_one', 0xbfc00210)
       
       

        self.instructionmemory.readInput()
        self.instructionmemory.writeOutput()

        self.testOutput.readInput()
    

        output_data = self.testOutput.inputValues['read2']   # read1 = muxloer = 10, read2 = 9  alucontrol = 32 opcode = 0
    

        
        self.assertEqual(output_data, 9)  
        


if __name__ == '__main__':
    unittest.main() 



       
   




















       





