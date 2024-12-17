import sys
from enum import IntEnum
from heapq import heappop, heappush, heapify
from dataclasses import dataclass


class Op(IntEnum):
    adv = 0
    bxl = 1
    bst = 2
    jnz = 3
    bxc = 4
    out = 5
    bdv = 6
    cdv = 7


@dataclass(slots=True)
class Machine:
    A: int = 0
    B: int = 0
    C: int = 0

    def combo(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.A
        if operand == 5:
            return self.B
        if operand == 6:
            return self.C
        raise ValueError(f"Invalid combo operand {operand}")

    def run(self, program, trace=False):
        i, i_last = 0, len(program) - 1

        while i <= i_last:
            opcode, operand, jump = program[i], program[i + 1], None

            if trace:
                reg = f"A={self.A:<10} B={self.B:<10} C={self.C:<10}"
                print(f"{reg} | {Op(opcode).name} {operand}")

            if opcode == Op.adv:
                self.A //= 2 ** self.combo(operand)
            elif opcode == Op.bdv:
                self.B = self.A // 2 ** self.combo(operand)
            elif opcode == Op.cdv:
                self.C = self.A // 2 ** self.combo(operand)
            elif opcode == Op.bxl:
                self.B ^= operand
            elif opcode == Op.bxc:
                self.B ^= self.C
            elif opcode == Op.bst:
                self.B = self.combo(operand) % 8
            elif opcode == Op.out:
                yield self.combo(operand) % 8
            elif opcode == Op.jnz and self.A != 0:
                jump = operand

            if jump is not None:
                i = jump
            else:
                i += 2

    def compile(self, program):
        # Never used, just for fun if you want to visualize your program :)
        def _combo(operand):
            if operand <= 3:
                return operand
            if operand == 4:
                return "A"
            if operand == 5:
                return "B"
            if operand == 6:
                return "C"

        for n, (opcode, operand) in enumerate(zip(program[::2], program[1::2])):
            if opcode == Op.adv:
                code = f"({n}) A //= 2 ** {_combo(operand)}"
            elif opcode == Op.bdv:
                code = f"({n}) B = A // 2 ** {_combo(operand)}"
            elif opcode == Op.cdv:
                code = f"({n}) C = A // 2 ** {_combo(operand)}"
            elif opcode == Op.bxl:
                code = f"({n}) B ^= {operand}"
            elif opcode == Op.bxc:
                code = f"({n}) B ^= C"
            elif opcode == Op.bst:
                code = f"({n}) B = {_combo(operand)} % 8"
            elif opcode == Op.out:
                code = f"({n}) print({_combo(operand)} % 8)"
            elif opcode == Op.jnz:
                code = f"({n}) goto ({operand}) if A != 0"

            yield f"{code:<30} # [{opcode}] {Op(opcode).name} {operand}"


_reg, _prog = sys.stdin.read().rstrip().split("\n\n")

registers = {}
for line in _reg.splitlines():
    name, value = line.split(": ")
    registers[name[-1]] = int(value)

_prog = _prog.split(": ")[1]
program = list(map(int, _prog.split(",")))


# PART 0
#
code = list(Machine(**registers).compile(program))
print("\n".join(code))


# PART 1
#
output = list(Machine(**registers).run(program))
print(",".join(map(str, output)))


# PART 2
#
def compiled_program(A):
    # NOT USED! Just for fun :) Also it runs 10x faster than the Machine.run
    # This is the hand-compiled version of 2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0
    # You can use Machine.compile to generate this code for any program.
    #
    # bst 4
    # bxl 5
    # cdv 5
    # bxl 6
    # adv 3
    # bxc 1
    # out 5
    # jnz 0 => back to beginning unless A == 0
    #
    while True:
        B = A % 8
        B ^= 5
        C = A // (2**B)
        B ^= 6
        A = A // (2**3)
        B = B ^ C
        yield B % 8
        if A == 0:
            break


# We want to find A so that run(A) = 2,4,1,5,7,5,1,6,0,3,4,1,5,5,3,0
# After looking at the results produced by the Machine.run on a few million A's,
# we notice that the last values out do not vary much, as they depend on the
# highest bits of A. Looking at compiled code, we can see that the program is
# showing some modulo (8) on the lowest bits, then dividing A by 8, and looping.
#
# This means if we can find a number A that outputs the last part of the program,
# for example [5,3,0], then a number that produces [5,5,3,0] has to be in:
#   {A*8, A*8+1, A*8+2, .. A*8+7}
# Because this covers all modulo 8 possibilities, before the division by 8.
# Once A*8+k produces the first value (5), then (A*8+k)//8 (next program iteration)
# is actually A, which produces [5,3,0], and so on.
#
# So the final solution, assuming all AoC inputs are roughly similar programs, should
# be quite generic. We find numbers that produce the last part of the program, then
# consider {A*8, A*8+1, .. A*8+7} as candidates for the next part of the program,
# until the whole program is covered.

m = Machine(**registers)
# A is corrupted, so we need to find it :)
B = m.B
C = m.C

# We use a heap to guarantee we find the smallest A that produces the output first
heap = [*range(8)]  # A's to consider, we cover all possible modulo 8 at first
heapify(heap)

while heap:
    A = heappop(heap)
    m.A = A
    m.B = B
    m.C = C

    output = list(m.run(program))
    length = len(output)
    if output == program[-length:]:
        if length == len(program):
            print(A)
            break
        for k in range(8):
            heappush(heap, A * 8 + k)
