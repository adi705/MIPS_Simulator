from cpuElement import CPUElement
from memory import Memory
import unittest
from testElement import TestElement

class DataMemory(Memory):
    def __init__(self, filename):
        Memory.__init__(self, filename)
    
    def connect(self, inputSources, outputValueNames, control, outputSignalNames):
        CPUElement.connect(self, inputSources, outputValueNames, control, outputSignalNames)

        assert(len(inputSources) == 2), '   DataMemory should have 2 inputs'
        assert(len(outputValueNames) == 1), ' DataMemory has only 1 output'
        assert(len(control) == 2), 'DataMemory has 2 control signal'
        assert(len(outputSignalNames) == 0), 'DataMemory does not have any control output'

        self.inputZero = inputSources[0][1] # read address port'
        self.inputOne = inputSources[1][1]  # write data port'
        self.output1 = outputValueNames[0]  # read data port'
        self.controlName1 = control[0][1]   # memwrite contol signal'
        self.controlName2 = control[1][1]   # memread contol signal'
    
    def writeOutput(self):

        # daddress is one of the serialized memory locations available in the data memory
        daddress = self.inputValues[self.inputZero] 
        # each dadress corresponds or maps to a specific data value stored in the variable named outputdata
        
        
        if self.controlSignals[self.controlName2] == 1:
             outputdata = self.memory.get(daddress,0) # data item at address daddress else NULL
             self.outputValues[self.output1] = outputdata # 32 bit  data read from the datamemory if it is a memread.

        if self.controlSignals[self.controlName1] == 1:
             self.memory[daddress] =  self.inputValues[self.inputOne] # 32 bit data item stored at daddress if it is a memwrite

   

class TestDataMemory(unittest.TestCase):
    
    def setUp(self):
      self.testInput =  TestElement()
      self.testOutput = TestElement()
      self.datamemory = DataMemory('add.mem')

      self.testInput.connect(
        [],
        ['inputaddress','write_data'],
        [],
        ['mem_write', 'mem_read']

        )

      self.datamemory.connect(
        [(self.testInput, 'inputaddress'), (self.testInput, 'write_data')],
        ['data_memory_output'],
        [(self.testInput, 'mem_write'), (self.testInput, 'mem_read')],
        []
        )

      self.testOutput.connect(
        [(self.datamemory, 'data_memory_output')],
        [],
        [],
        []
        )

    def test_correct_behaviour(self):
        self.testInput.setOutputValue('inputaddress', 0x00208)
        self.testInput.setOutputValue('write_data', 20)

        self.datamemory.memory[0x00208] = 19

        self.testInput.setOutputControl('mem_read', 1)
        self.testInput.setOutputControl('mem_write', 0)
        self.datamemory.readInput()
        self.datamemory.readControlSignals()
        self.datamemory.writeOutput()
        self.testOutput.readInput()


        output = self.testOutput.inputValues['data_memory_output']
        self.assertEqual(output, 19)

        self.testInput.setOutputControl('mem_write', 1)
        self.testInput.setOutputControl('mem_read', 0)

        self.datamemory.readInput()
        self.datamemory.readControlSignals()
        self.datamemory.writeOutput()
        self.testOutput.readInput()

        self.testInput.setOutputControl('mem_read', 1)
        self.testInput.setOutputControl('mem_write', 0)
        self.datamemory.readInput()
        self.datamemory.readControlSignals()
        self.datamemory.writeOutput()
        self.testOutput.readInput()

        output = self.testOutput.inputValues['data_memory_output']
        self.assertEqual(output, 20)
 








if __name__ == '__main__':
    unittest.main()




           