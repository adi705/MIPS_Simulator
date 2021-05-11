import unittest
from cpuElement import CPUElement
import common
from testElement import TestElement

class ControlUnit(CPUElement):
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)


        assert(len(inputSources) == 2), 'control unit should have 2 input'
        assert(len(outputValueNames) == 0), 'control unit has  0 output'
        assert(len(control) == 0), 'control unit has no control signal'
        assert(len(outputSignalNames) == 11), 'control unit has 11  control output signals'

        self.inputZero = inputSources[0][1] # opcode
        self.inputOne = inputSources[1][1] # instruction[5:0]
       
      
        self.regdst = outputSignalNames[0]  
        self.jump = outputSignalNames[1]   
        self.branch = outputSignalNames[2]   
        self.memread = outputSignalNames[3]
        self.memtoreg = outputSignalNames[4]
        self.aluop = outputSignalNames[5]         # 4 bit control direct signal
        self.memwrite = outputSignalNames[6]
        self.alusrc = outputSignalNames[7]
        self.regwrite = outputSignalNames[8] 
        
        self.branchnotequal = outputSignalNames[9]
        self.loadui = outputSignalNames[10]

    def writeOutput(self):

        if self.inputValues[self.inputZero] == 0 :  #Rtype add, sub, and,or, slt, addu, subu 
            self.outputControlSignals[self.regdst] = 1
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 0
            self.outputControlSignals[self.regwrite] = 1
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
           
            if self.inputValues[self.inputOne] == 32:  # add instruction
                self.outputControlSignals[self.aluop] = 2
           
            if self.inputValues[self.inputOne] == 33:  # add unsigned instruction
                self.outputControlSignals[self.aluop] = 3     

            if self.inputValues[self.inputOne] == 34:  # sub instruction
                self.outputControlSignals[self.aluop] = 6  

            if self.inputValues[self.inputOne] == 35:  # sub unsigned instruction
                self.outputControlSignals[self.aluop] = 8       

            if self.inputValues[self.inputOne] == 36:  # and instruction
                self.outputControlSignals[self.aluop] = 0   

            if self.inputValues[self.inputOne] == 37:  # or instruction
                self.outputControlSignals[self.aluop] = 1      


            if self.inputValues[self.inputOne] == 42:  # set on less than instruction
                self.outputControlSignals[self.aluop] = 7  

        

        if self.inputValues[self.inputZero] == 8 : # add immediate 
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 1     
            self.outputControlSignals[self.regwrite] = 1
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 2

        if self.inputValues[self.inputZero] == 9 : # add  immediate unsigned    
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 1     
            self.outputControlSignals[self.regwrite] = 1
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 3   # same as add unsigned

        if self.inputValues[self.inputZero] == 35 :   #load word 
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 1
            self.outputControlSignals[self.memtoreg] = 1
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 1     
            self.outputControlSignals[self.regwrite] = 1
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 2

        if self.inputValues[self.inputZero] == 43 :   #store word 
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 1
            self.outputControlSignals[self.alusrc] = 1     
            self.outputControlSignals[self.regwrite] = 0
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 2   # addition 

        if self.inputValues[self.inputZero] == 4 :   # branch equal
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 1
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 0     
            self.outputControlSignals[self.regwrite] = 0
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 6  # subtraction 

        if self.inputValues[self.inputZero] == 5 :   # branch not equal
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 0     
            self.outputControlSignals[self.regwrite] = 0
            self.outputControlSignals[self.branchnotequal] = 1
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 6  # subtraction     

        if self.inputValues[self.inputZero] == 2 :   # jump
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 1
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 0     
            self.outputControlSignals[self.regwrite] = 0
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 0
            self.outputControlSignals[self.aluop] = 2  # add independent of any operation

        if self.inputValues[self.inputZero] == 15 :   # load upper immediate
            self.outputControlSignals[self.regdst] = 0
            self.outputControlSignals[self.jump] = 0
            self.outputControlSignals[self.branch] = 0
            self.outputControlSignals[self.memread] = 0
            self.outputControlSignals[self.memtoreg] = 0
            self.outputControlSignals[self.memwrite] = 0
            self.outputControlSignals[self.alusrc] = 0     
            self.outputControlSignals[self.regwrite] = 1
            self.outputControlSignals[self.branchnotequal] = 0
            self.outputControlSignals[self.loadui] = 1
            self.outputControlSignals[self.aluop] = 2  # add independent of any operation    

        #print('ControlUnit branch: %d' % self.outputControlSignals[self.branch])
        


class TestControl(unittest.TestCase):
    def setUp(self):
        self.control_unit = ControlUnit()
        self.testInput = TestElement()
        self.testOutput = TestElement()

        self.testInput.connect(
        [],
        ['input_opcode ', 'input_two'],      
        [],
        []
        )

        

        self.control_unit.connect(
        [(self.testInput, 'input_opcode'),(self.testInput, 'input_two')],
        [],
        [],
        ['regdst','jump','branch', 'memread','memtoreg','aluop','memwrite','alusrc','regwrite','branchnotequal','loadui']
        )

        self.testOutput.connect(
        [],
        [],
        [(self.control_unit, 'regdst'),(self.control_unit, 'jump'), (self.control_unit, 'branch'),(self.control_unit, 'memread'),
         (self.control_unit, 'memtoreg'),(self.control_unit, 'aluop'), (self.control_unit, 'memwrite'),(self.control_unit, 'alusrc'),         
         (self.control_unit, 'regwrite'),(self.control_unit, 'branchnotequal'), (self.control_unit, 'loadui')  ],
        []
        )

    def test_correct_behavior(self):
        self.testInput.setOutputValue('input_opcode', 0)   # r type add
        self.testInput.setOutputValue('input_two', 32)
     

        self.control_unit.readInput()
        self.control_unit.writeOutput()
        self.testOutput.readControlSignals()

    

        regdst = self.testOutput.controlSignals['regdst'] 
        jump = self.testOutput.controlSignals['jump'] 
        branch = self.testOutput.controlSignals['branch']  
        memread = self.testOutput.controlSignals['memread']
        memtoreg = self.testOutput.controlSignals['memtoreg']
        aluop = self.testOutput.controlSignals['aluop']        # 4 bit control direct signal
        memwrite = self.testOutput.controlSignals['memwrite']
        alusrc = self.testOutput.controlSignals['alusrc']
        regwrite = self.testOutput.controlSignals['regwrite']  
        branchnotequal = self.testOutput.controlSignals['branchnotequal'] 
        loadui = self.testOutput.controlSignals['loadui']              

        self.assertEqual(regdst, 1)  
        self.assertEqual(jump, 0) 
        self.assertEqual(branch, 0)  
        self.assertEqual(memread, 0)
        self.assertEqual(memtoreg, 0)  
        self.assertEqual(aluop, 2) 
        self.assertEqual(memwrite, 0)  
        self.assertEqual(alusrc, 0)
        self.assertEqual(regwrite, 1) 
        self.assertEqual(branchnotequal,0)  
        self.assertEqual(loadui, 0)

        self.testInput.setOutputValue('input_opcode', 8)   #  add immediate
        self.control_unit.readInput()
        self.control_unit.writeOutput()
        self.testOutput.readControlSignals()

        regdst = self.testOutput.controlSignals['regdst'] 
        jump = self.testOutput.controlSignals['jump'] 
        branch = self.testOutput.controlSignals['branch']  
        memread = self.testOutput.controlSignals['memread']
        memtoreg = self.testOutput.controlSignals['memtoreg']
        aluop = self.testOutput.controlSignals['aluop']        # 4 bit control direct signal
        memwrite = self.testOutput.controlSignals['memwrite']
        alusrc = self.testOutput.controlSignals['alusrc']
        regwrite = self.testOutput.controlSignals['regwrite']  
        branchnotequal = self.testOutput.controlSignals['branchnotequal'] 
        loadui = self.testOutput.controlSignals['loadui']

        self.assertEqual(regdst, 0)  
        self.assertEqual(jump, 0) 
        self.assertEqual(branch, 0)  
        self.assertEqual(memread, 0)
        self.assertEqual(memtoreg, 0)  
        self.assertEqual(aluop, 2) 
        self.assertEqual(memwrite, 0)  
        self.assertEqual(alusrc, 1)
        self.assertEqual(regwrite, 1) 
        self.assertEqual(branchnotequal,0)  
        self.assertEqual(loadui, 0)

        self.testInput.setOutputValue('input_opcode', 31)   #  load ui
        self.control_unit.readInput()
        self.control_unit.writeOutput()
        self.testOutput.readControlSignals()

        regdst = self.testOutput.controlSignals['regdst'] 
        jump = self.testOutput.controlSignals['jump'] 
        branch = self.testOutput.controlSignals['branch']  
        memread = self.testOutput.controlSignals['memread']
        memtoreg = self.testOutput.controlSignals['memtoreg']
        aluop = self.testOutput.controlSignals['aluop']        # 4 bit control direct signal
        memwrite = self.testOutput.controlSignals['memwrite']
        alusrc = self.testOutput.controlSignals['alusrc']
        regwrite = self.testOutput.controlSignals['regwrite']  
        branchnotequal = self.testOutput.controlSignals['branchnotequal'] 
        loadui = self.testOutput.controlSignals['loadui']

        self.assertEqual(regdst, 0)  
        self.assertEqual(jump, 0) 
        self.assertEqual(branch, 0)  
        self.assertEqual(memread, 0)
        self.assertEqual(memtoreg, 0)  
       # self.assertEqual(aluop, 6) 
        self.assertEqual(memwrite, 0)  
        self.assertEqual(alusrc, 0)
        self.assertEqual(regwrite, 0) 
        self.assertEqual(branchnotequal,0)  
        self.assertEqual(loadui, 1)


        
        


if __name__ == '__main__':
    unittest.main() 
















