REGISTERS_SIZE = 16

VALID_COMMANDS = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]
VALID_COMMANDS_NAMES = ['IDLE', 'END', 'LOAD', 'SUM', 'MUL', 'JMP_IF', 'PRT', 'JMP']

class VirtualMachine:
    '''

    Nika Kotsiubynska's virtual machine.

    The machine has following commands:
    0x00 IDLE, no ops - do nothing
    0x01 END, no ops - end execution
    0x02 LOAD, 2 ops - set R(op1) to op2
    0x03 SUM, 3 ops - set R(op1) to R(op2) + R(op3)
    0x04 MUL, 3 ops - set R(op1) to R(op2) * R(op3)
    0x05 JMP_IF, 3 ops - go op2 steps forward in commands and op3 steps forward in args if R(op1) > 0
    0x06 PRT, 1 op - print R(op)
    0x07, JMP, 2 ops - go op1 steps forward in commands and op2 steps forward in args
    '''
    def __init__(self):
        self.command_pointer = 0
        self.arg_pointer = 0
        self.registers = [0] * 16

    def __get_arg(self, arguments):
        arg = arguments[self.arg_pointer]
        self.arg_pointer += 1
        return arg

    def __print_command(self, command, verbose=False):
        if verbose:
            print(VALID_COMMANDS_NAMES[command])

    def run(self, commands, arguments, debug=False, verbose=False):
        self.command_pointer = 0
        self.arg_pointer = 0

        while self.command_pointer < len(commands):
            if debug:
                print(f"Command pointer: {self.command_pointer}")
                print(f"Argument pointer: {self.arg_pointer}")

            command = commands[self.command_pointer]
            self.command_pointer += 1

            if command not in VALID_COMMANDS:
                raise Exception("Command is not valid")
            elif command == 0x00:
                self.__print_command(command, verbose)
            elif command == 0x01:
                self.__print_command(command, verbose)
                break
            elif command == 0x02:
                self.__print_command(command, verbose)

                register_index = self.__get_arg(arguments)
                new_val = self.__get_arg(arguments)

                print(f"Trying to set R[{register_index}] to {new_val}")

                if register_index < 0 or register_index >= REGISTERS_SIZE:
                    raise Exception("Register index is out of bounds")

                self.registers[register_index] = new_val
            elif command == 0x03:
                self.__print_command(command, verbose)

                target_register = self.__get_arg(arguments)
                sum_arg1 = self.__get_arg(arguments)
                sum_arg2 = self.__get_arg(arguments)

                print(f"Trying to set R[{target_register}] to R[{sum_arg1}] + R[{sum_arg2}]")

                if target_register < 0 or target_register >= REGISTERS_SIZE:
                    raise Exception("Target register index is out of bounds")
                if sum_arg1 < 0 or sum_arg1 >= REGISTERS_SIZE:
                    raise Exception("First argument register index is out of bounds")
                if sum_arg2 < 0 or sum_arg2 >= REGISTERS_SIZE:
                    raise Exception("Second argument register index is out of bounds")

                self.registers[target_register] = self.registers[sum_arg1] + self.registers[sum_arg2]
            elif command == 0x04:
                self.__print_command(command, verbose)

                target_register = self.__get_arg(arguments)
                mul_arg1 = self.__get_arg(arguments)
                mul_arg2 = self.__get_arg(arguments)

                print(f"Trying to set R[{target_register}] to R[{mul_arg1}] * R[{mul_arg2}]")

                if target_register < 0 or target_register >= REGISTERS_SIZE:
                    raise Exception("Target register index is out of bounds")
                if mul_arg1 < 0 or mul_arg1 >= REGISTERS_SIZE:
                    raise Exception("First argument register index is out of bounds")
                if mul_arg2 < 0 or mul_arg2 >= REGISTERS_SIZE:
                    raise Exception("Second argument register index is out of bounds")

                self.registers[target_register] = self.registers[mul_arg1] * self.registers[mul_arg2]
            elif command == 0x05:
                self.__print_command(command, verbose)

                conditional_reg = self.__get_arg(arguments)
                com_delta = self.__get_arg(arguments)
                arg_delta = self.__get_arg(arguments)

                if conditional_reg < 0 or conditional_reg >= REGISTERS_SIZE:
                    raise Exception("Register index is out of bounds")
                if -com_delta > self.command_pointer and com_delta < 0:
                    raise Exception("We can't go this number of commands back")
                if -arg_delta > self.arg_pointer and arg_delta < 0:
                    raise Exception("We can't go this number of arguments back")
                if self.command_pointer + com_delta >= len(commands) and com_delta > 0:
                    raise Exception("We can't go this number of commands forward")
                if self.arg_pointer + arg_delta >= len(arguments)  and arg_delta > 0:
                    raise Exception("We can't go this number of arguments forward")

                print(f"Command pointer was {self.command_pointer}, Arg pointer was {self.arg_pointer}")

                if self.registers[conditional_reg] > 0:
                    self.command_pointer += com_delta
                    self.arg_pointer += arg_delta

                print(f"Command pointer is {self.command_pointer}, Arg pointer is {self.arg_pointer} now")
            elif command == 0x06:
                self.__print_command(command, verbose)

                reg_num = self.__get_arg(arguments)

                if reg_num < 0 or reg_num >= REGISTERS_SIZE:
                    raise Exception("Register index is out of bounds")

                print(f"R[{reg_num}] = {self.registers[reg_num]}")
            elif command == 0x07:
                self.__print_command(command, verbose)

                com_delta = self.__get_arg(arguments)
                arg_delta = self.__get_arg(arguments)

                if -com_delta > self.command_pointer and com_delta < 0:
                    raise Exception("We can't go this number of commands back")
                if -arg_delta > self.arg_pointer and arg_delta < 0:
                    raise Exception("We can't go this number of arguments back")
                if self.command_pointer + com_delta >= len(commands) and com_delta > 0:
                    raise Exception("We can't go this number of commands forward")
                if self.arg_pointer + arg_delta >= len(arguments) and arg_delta > 0:
                    raise Exception("We can't go this number of arguments forward")

                print(f"Command pointer was {self.command_pointer}, Arg pointer was {self.arg_pointer}")

                self.command_pointer += com_delta
                self.arg_pointer += arg_delta

                print(f"Command pointer is {self.command_pointer}, Arg pointer is {self.arg_pointer} now")
            else:
                self.__print_command(command)
                raise Exception("Unimplemented")