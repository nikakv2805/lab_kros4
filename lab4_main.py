from lab4_vm import VirtualMachine
import pytest

def factorial(number, vm=VirtualMachine(), verbose=False):
    commands = [0x00,
                0x02,
                0x05,
                0x02,
                0x07,
                0x02,
                0x02,
                0x03,
                0x06,
                0x05,
                0x07,
                0x04,
                0x06,
                0x03,
                0x06,
                0x05,
                0x06,
                0x01]
    arguments = [0, number,
                 0, 2, 4,
                 0, 1,
                 11, 24,
                 1, number,
                 2, -1,
                 1, 1, 2,
                 1,
                 1, 1, 2,
                 5, 11,
                 0, 0, 1,
                 0,
                 1, 1, 2,
                 1,
                 1, -5, -11,
                 0]
    vm.run(commands, arguments)


if __name__ == '__main__':
    machine = VirtualMachine()

    # checking how it works
    factorial(0, machine, verbose=True)

    # testing
    pytest.main(['lab4_test.py'])