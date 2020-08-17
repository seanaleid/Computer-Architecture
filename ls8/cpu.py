"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # RAM --> random access memory --> 8 bit
        self.ram = [0]*256
        # program counter --> counter
        self.pc = 0
        # register --> local variable holders
        self.register = [0]*8
        # if the program is running
        self.running = True

    def ram_read(self, address):
        # look in the RAM at the address passed through 
        return self.ram[address]

    def ram_write(self, value, address):
        # takes the address and updates the value at that address
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""
        address = 0
        filename = sys.argv[1]
        with open(filename) as f:
            for line in f:
                line = line.split('#')
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                # print(v)
                self.ram[address] = v
                address+=1
        print(self.ram[:15])

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        #elif op == "SUB": etc

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == 'MUL':
            self.register[reg_a] *= self.register[reg_b]
        elif op == "ADIVDD":
            self.register[reg_a] /= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        commands = {
            'LDI': 0b10000010,
            'PRN': 0b01000111,
            'HLT': 0b00000001,
            'MUL': 0b10100010
        }

        while self.running:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)

            if IR == commands['HLT']:
                print(f"HALTED")
                self.running = False
            elif IR == commands['LDI']:
                address = operand_a
                value = operand_b
                self.register[address] = value
                print(f'REGISTER {self.register}')
                self.pc+=3
            elif IR == commands['PRN']:
                address = operand_a
                value = self.register[address]
                print(value)
                self.pc+=2
            elif IR == commands['MUL']:
                self.alu('MUL', operand_a, operand_b)
                self.pc+=3
            else:
                print(f'NOT KNOWN {IR} AT ADDRESS {self.pc}')
                sys.exit(1)