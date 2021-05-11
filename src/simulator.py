'''
Code written for inf-2200, University of Tromso
'''

import sys
#from mipsSimulator import MIPSSimulator
from mysimulator import MySimulator
def runSimulator(sim):
    # Replace this with your own main loop!
    while (1):
        sim.tick()
        print(hex(sim.pc.currentAddress()))
        sim.printRegisterFile()

        # For checking selectionsort
        #print()
        #print(sim.datamemory.memory[0xc0000000])
        #print(sim.datamemory.memory[0xc0000004])
        #print(sim.datamemory.memory[0xc0000008])
        #print(sim.datamemory.memory[0xc000000c])
        #print(sim.datamemory.memory[0xc0000010])
        #print(sim.datamemory.memory[0xc0000014])
        #print(sim.datamemory.memory[0xc0000018])
        #print(sim.datamemory.memory[0xc000001c])
        #print(sim.datamemory.memory[0xc0000020])
        #print(sim.datamemory.memory[0xc0000024])
        #print(sim.datamemory.memory[0xc0000028])
        #print(sim.datamemory.memory[0xc000002c])
        #print(sim.datamemory.memory[0xc0000030])
        #print()

if __name__ == '__main__':
    assert(len(sys.argv) == 2), 'Usage: python %s memoryFile' % (sys.argv[0],)
    memoryFile = sys.argv[1]
    
   # simulator = MIPSSimulator(memoryFile)
    simulator = MySimulator(memoryFile)
        
    try:
        runSimulator(simulator)
    except:
        simulator.datamemory.printAll()
