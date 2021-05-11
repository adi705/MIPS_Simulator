from pc import PC
from add import Add
from mux import Mux
from myregeister import RegisterFile
from myinstructionmem import InstructionMemory
from mydatamemory import DataMemory
from myalu import Alu
from mycontrolunit import ControlUnit
from myleftshift2 import Shift2
from myshift16 import Shift16
from mysignextend import SignExtend
from myalterand import Alterand
from myaltershift import Altershift
from constant import Constant
# what about memory ?


class MySimulator():
    '''Main class for MIPS pipeline simulator.
    
    Provides the main method tick(), which runs pipeline
    for one clock cycle.
    
    '''
    def __init__(self, memoryFile):
        
        self.nCycles = 0 # Used to hold number of clock cycles spent executing instructions
        
        self.datamemory = DataMemory(memoryFile)
        self.instructionmemory = InstructionMemory(memoryFile)
        self.registerfile = RegisterFile()

        self.constant4 = Constant(4)
        
        self.alu = Alu()
        self.controlunit = ControlUnit()
        self.shift2 = Shift2()
        self.shift16 = Shift16()
        self.signextend = SignExtend()
        self.alterand = Alterand()
        self.altershift = Altershift()
       
        self.mux_writereg = Mux()    # 6 multiplexors
        self.mux_regoutput = Mux()
        self.mux_jump = Mux()
        self.mux_branch = Mux()
        self.mux_datamem = Mux()
        self.mux_shift16 = Mux()

        self.adderpc = Add()   # 2 adders
        self.addershift = Add()
        self.pc = PC(0xbfc00000) # hard coded "boot" address
        
        self.elements = [self.constant4, self.adderpc, self.instructionmemory, self.controlunit, self.altershift, self.mux_writereg,
             self.registerfile, self.shift16, self.signextend, self.shift2, self.addershift, self.mux_regoutput, self.alu, self.alterand, 
             self.mux_branch, self.mux_jump, self.datamemory, self.mux_datamem, self.mux_shift16, self.registerfile]
        
        self._connectCPUElements()
        
    def _connectCPUElements(self):
        
        
        self.constant4.connect(
            [],
            ['constant'],
            [],
            []
        )
        
        self.controlunit.connect(
            [(self.instructionmemory, 'ins_31-26'), (self.instructionmemory, 'ins_5-0')],
            [],
            [],
            ['regdst','jump','branch','memread','memtoreg','aluop','memwrite','alusrc','regwrite','branchnotequal','loadui']
        )
        
        

        self.adderpc.connect(
            [(self.pc, 'pcaddress'), (self.constant4, 'constant')],
            ['sum_pc'],
            [],
            []
        )

        self.instructionmemory.connect(
            [(self.pc, 'pcaddress')],
            ['ins_31-26','ins_25-21' , 'ins_20-16', 'ins_15-11', 'ins_15-0', 'ins_5-0', 'ins_25-0'],
            [],
            []
        )

        self.altershift.connect(
            [(self.instructionmemory, 'ins_25-0'), (self.adderpc, 'sum_pc')],
            ['jump_address'],
            [],
            []
        )

        self.signextend.connect(
            [(self.instructionmemory, 'ins_15-0')],
            ['signextend_result'],
            [],
            []
        )

        self.shift2.connect(
            [(self.signextend, 'signextend_result')],
            ['shift2_result'],
            [],
            []
        )
        self.addershift.connect(
            [(self.adderpc, 'sum_pc'), (self.shift2, 'shift2_result')],
            ['sum_addershift'],
            [],
            []
        )
        self.mux_branch.connect(      
            [(self.adderpc, 'sum_pc'), (self.addershift, 'sum_addershift')],
            ['mux_branch_result'],
            [(self.alterand, 'alterand_result')],
            []
        )

        self.mux_jump.connect(      
            [(self.mux_branch, 'mux_branch_result'), (self.altershift, 'jump_address')],
            ['mux_jump_result'],
            [(self.controlunit, 'jump')],
            []
        )
        self.alterand.connect(      
            [],
            [],
            [(self.controlunit, 'branch'), (self.controlunit, 'branchnotequal'), (self.alu, 'alu_zero_result')],
            ['alterand_result']
        )


        
        self.mux_writereg.connect(
            [(self.instructionmemory, 'ins_20-16'), (self.instructionmemory, 'ins_15-11')],
            ['mux_writereg_result'],
            [(self.controlunit, 'regdst')],
            []
        )

        self.registerfile.connect(
            [(self.instructionmemory, 'ins_25-21'), (self.instructionmemory, 'ins_20-16'), (self.mux_writereg, 'mux_writereg_result'), (self.mux_shift16,'mux_shift16_result' )],
            ['reg_data1','reg_data2'],
            [(self.controlunit, 'regwrite')],
            []
        )

        self.mux_regoutput.connect(
            [(self.registerfile, 'reg_data2'), (self.signextend, 'signextend_result')],
            ['mux_regoutput_result'],
            [(self.controlunit, 'alusrc')],
            []
        )
        self.alu.connect(
            [(self.registerfile, 'reg_data1'), (self.mux_regoutput, 'mux_regoutput_result')],
            ['alu_result'],
            [(self.controlunit, 'aluop')],
            ['alu_zero_result']
        )
        self.datamemory.connect(
            [(self.alu, 'alu_result'), (self.registerfile, 'reg_data2')],
            ['datamemory_result'],
            [(self.controlunit, 'memwrite'), (self.controlunit, 'memread')],
            []
        )

        self.mux_datamem.connect(
            [(self.alu, 'alu_result'), (self.datamemory, 'datamemory_result')],
            ['mux_datamemory_result'],
            [(self.controlunit, 'memtoreg')],
            []  
        )

        self.mux_shift16.connect(
            [(self.mux_datamem, 'mux_datamemory_result'), (self.shift16, 'shift16_result')],
            ['mux_shift16_result'],
            [(self.controlunit, 'loadui')],
            []  
        )

        self.shift16.connect(
            [(self.instructionmemory, 'ins_15-0')],
            ['shift16_result'],
            [],
            []
        )





        
        self.pc.connect(
            [(self.mux_jump, 'mux_jump_result')],
            ['pcaddress'],
            [],
            []
        )
    
    def clockCycles(self):
        '''Returns the number of clock cycles spent executing instructions.'''
        
        return self.nCycles
    
    def dataMemory(self):
        '''Returns dictionary, mapping memory addresses to data, holding
        data memory after instructions have finished executing.'''
        
        return self.dataMemory.memory
    
    def registerFile(self):
        '''Returns dictionary, mapping register numbers to data, holding
        register file after instructions have finished executing.'''
        
        return self.registerfile.register
    
    def printDataMemory(self):
        self.dataMemory.printAll()
    
    def printRegisterFile(self):
        self.registerfile.printAll()
    
    def tick(self):
        '''Execute one clock cycle of pipeline.'''
        
        self.nCycles += 1
        
        # The following is just a small sample implementation
        
        self.pc.writeOutput()
        
        for elem in self.elements:
            elem.readControlSignals()
            elem.readInput()
            elem.writeOutput()
            elem.setControlSignals()
            
        self.pc.readInput()
