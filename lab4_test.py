from lab4_vm import VirtualMachine
from lab4_main import factorial
from math import factorial as math_factorial
from random import randint

def test_factorial_0(machine = VirtualMachine()):
    factorial(0, machine)
    assert machine.registers[0] == 1, "factorial of 0 is 1"

def test_factorial_1(machine = VirtualMachine()):
    factorial(1, machine)
    assert machine.registers[0] == 1, "factorial of 1 is 1"

def test_factorial_random(machine = VirtualMachine()):
    number = randint(2, 20)
    factorial(number, machine)
    desired = math_factorial(number)
    assert machine.registers[0] == desired, f"factorial of {number} is {desired}"