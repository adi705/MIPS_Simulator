'''
Implements base class for memory elements.

Note that since both DataMemory and InstructionMemory are subclasses of the Memory
class, they will read the same memory file containing both instructions and data
memory initially, but the two memory elements are treated separately, each with its
own, isolated copy of the data from the memory file.

Code written for inf-2200, University of Tromso
'''

from cpuElement import CPUElement
import common
import sys

class Memory(CPUElement):
    def __init__(self, filename):
    
        # Dictionary mapping memory addresses to data
        # Both key and value must be of type 'long'
        self.memory = {}
        
        self.initializeMemory(filename)
    
    def initializeMemory(self, filename):
        '''
        Helper function that reads initializes the data memory by reading input
        data from a file.
        '''

        with open(filename, "r") as file:
            for line in file:
                if line[0] != "#" and line[0] != '\n':
                    
                    address = int(line.split()[0], 16)
                  #  print(" %s\t=> " % (hex(int(address))) )
                    self.memory[address] = int(line.split()[1], 16)
        
    def printAll(self):
        for key in sorted(self.memory.keys()):
            print("%s\t=> %s\t(%s)" % (hex(int(key)), common.fromUnsignedWordToSignedWord(self.memory[key]), hex(int(self.memory[key]))))



if __name__ == '__main__':
    assert(len(sys.argv) == 2), 'Usage: python %s memoryFile' % (sys.argv[0],)
    
    memoryFile = sys.argv[1]

    memory = Memory(memoryFile)

    memory.printAll()
