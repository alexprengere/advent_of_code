import os
import sys
import operator
from itertools import chain
from collections import ChainMap
from dataclasses import dataclass, field

try:
    import pydot
except ImportError:
    print("Please install pydot with `pip install pydot`")
    pydot = None

OPERATORS = {
    "AND": operator.and_,
    "OR": operator.or_,
    "XOR": operator.xor,
    "ADD": operator.add,  # for testing purposes
}
PYDOT_DATA = {
    operator.and_: ("AND", "red"),
    operator.or_: ("OR", "blue"),
    operator.xor: ("XOR", "orange"),
}


_values, _gates = sys.stdin.read().split("\n\n")

input_ = {}
for row in _values.splitlines():
    wire, b = row.split(": ")
    input_[wire] = int(b)


gates = {}
for row in _gates.splitlines():
    _wires, w_out = row.split(" -> ")
    w1, op_name, w2 = _wires.split(" ")
    gates[w_out] = w1, w2, OPERATORS[op_name]


@dataclass(slots=True)
class Circuit:
    # input is a dict of the xXX and yXX wires values
    # gates is a dict of the gates: {zXX: (w1, w2, operator)}
    # output is a dict storing the computed values of the wires,
    # it is actually not necessary, it just avoids recomputing the same
    # wire value multiple times when backtracking from zXX.
    input_: dict
    gates: dict
    output: dict = field(default_factory=dict)

    def set_input(self, xy, value):
        bit = 0
        while (wire := f"{xy}{bit:02d}") in self.input_:
            self.input_[wire] = (value >> bit) & 1
            bit += 1

    def output_wires(self):
        bit = 0
        while (wire := f"z{bit:02d}") in self.gates:
            yield wire
            bit += 1

    def compute_output(self):
        # Evaluate all output wires and return the z value.
        self.output.clear()
        z = 0
        for bit, wire in enumerate(self.output_wires()):
            z |= self.evaluate(wire) << bit
        return z

    def evaluate(self, wire):
        # Recursively evaluate the wire value, base case is the input value.
        # Output is stored in a cache to avoid recomputing the same wire.
        if wire in self.input_:
            return self.input_[wire]
        w1, w2, op = self.gates[wire]
        self.output[wire] = op(
            self.evaluate(w1),
            self.evaluate(w2),
        )
        return self.output[wire]

    def swap(self, g1, g2):
        # Swaps two gates in place
        self.gates[g1], self.gates[g2] = self.gates[g2], self.gates[g1]

    def topo_sort(self):
        # After swapping gates, we need to check if the circuit has a cycle.
        # We use Kahn algorithm to detect if a cycle exists.
        # If you look at the circuit as a graph, the nodes are all the wires.
        # We can have them without recursion by iterating the input and gates output.
        in_degree = dict.fromkeys(ChainMap(self.gates, self.input_), 0)

        # No need to iterate inputs, as those are the roots of the graph.
        for wire in self.gates:
            w1, w2, _ = self.gates[wire]
            for w in (w1, w2):
                in_degree[w] += 1

        stack = [wire for wire, degree in in_degree.items() if degree == 0]
        topo_order = []
        while stack:
            wire = stack.pop()
            topo_order.append(wire)
            if wire not in self.gates:  # an input
                continue
            w1, w2, _ = self.gates[wire]
            for w in (w1, w2):
                in_degree[w] -= 1
                if in_degree[w] == 0:
                    stack.append(w)

        return topo_order

    def has_cycle(self):
        return len(self.topo_sort()) != (len(self.gates) + len(self.input_))

    def gates_impacting(self, wire):
        # Get all gates participating in the evaluation of a wire.
        stack = [wire]
        visited = set()
        while stack:
            wire = stack.pop()
            visited.add(wire)
            yield wire
            w1, w2, _ = self.gates[wire]
            for w in (w1, w2):
                if w in self.gates:  # not an input
                    stack.append(w)

    expected = OPERATORS[os.getenv("OPNAME", "ADD")]  # set to AND on the test input

    def test(self, bit):
        # This method tests the circuit for a given bit.
        # We test some particular cases to ensure the circuit is working as expected.
        h = (2 << bit) - 1  # 0b111111111

        for x, y in [(0, 0), (0, h), (h, 0), (h, h), (h, 1), (1, h)]:
            self.set_input("x", x)
            self.set_input("y", y)
            # When comparing computing vs expected, we ignore bits above 'bit'
            if self.compute_output() & h != self.expected(x, y) & h:
                return False
        return True


def build_dot(circuit, bit_max=None):
    dot = pydot.Dot(graph_type="digraph", rankdir="LR")

    visited = set()
    for bit, wire in enumerate(circuit.output_wires()):
        if bit_max is None or bit <= bit_max:
            _add_node(dot, circuit, wire, visited, root=True)

    return dot


def _add_node(dot, circuit, wire, visited, root=False):
    # For visualization purposes, we build a graph of the circuit.
    if wire in visited:
        return
    visited.add(wire)
    if wire in circuit.input_:
        dot.add_node(
            pydot.Node(
                wire,
                label=f"{wire}={circuit.input_[wire]}",
                style="filled",
                fillcolor="grey",
            )
        )
        return
    w1, w2, op = circuit.gates[wire]
    op_name, color = PYDOT_DATA[op]
    dot.add_node(
        pydot.Node(
            wire,
            label=f"{op_name}={wire}",
            color=color,
            shape="ellipse" if root else "box",
            style="filled" if root else "solid",
        )
    )
    dot.add_edge(pydot.Edge(w1, wire))
    dot.add_edge(pydot.Edge(w2, wire))
    _add_node(dot, circuit, w1, visited)
    _add_node(dot, circuit, w2, visited)


# PART 1
#
circuit = Circuit(input_, gates)
print(circuit.compute_output())


# PART 2
#
def fix_with_swap(circuit, order, bit, suspicious_gates, remaining_gates):
    # This is the function that finds the best swap to fix the circuit.
    # We test first the gates that are highest in the topological order
    for sg in sorted(suspicious_gates, key=lambda x: order[x]):
        for rg in sorted(remaining_gates, key=lambda x: -order[x]):
            if rg == sg:
                continue
            circuit.swap(sg, rg)
            if circuit.has_cycle():
                circuit.swap(rg, sg)  # unswap
                continue
            if not circuit.test(bit):
                circuit.swap(rg, sg)  # unswap
                continue
            return sg, rg

    raise ValueError("No swap found")


# The general algorithm is to test the circuit for each bit, starting
# from the lowest bit. If the test fails, we find the gates that are
# impacting the wire value, and we try to swap them with other gates.
# So we progressively build a circuit that is working from the lowest
# to the highest bit. We stop at the highest bit, as there is no carry.
# There are some optimizations that probably work on all AoC inputs,
# but I am not 100% sure, for example we test gates in a particular order,
# to speed up the process.

# build_dot(circuit, bit_max=None).write_png("circuit.png")
placed_gates = set()  # the gates we are sure are correctly placed
remaining_gates = set(circuit.gates)  # the gates not in placed_gates
swaps = []  # the final list of working swaps that fix the circuit

# The topological order we will use to prioritize the swaps to try
order = {wire: n for n, wire in enumerate(circuit.topo_sort())}

# We do not test the highest bit, as there will be no "carry" to propagate.
output_wires_except_highest = list(circuit.output_wires())[:-1]

for bit, wire in enumerate(output_wires_except_highest):
    # The gates that are impacting the wire value, which is zXX here.
    current_gates = set(circuit.gates_impacting(wire))

    if circuit.test(bit):
        placed_gates |= current_gates
        remaining_gates -= current_gates
        continue

    suspicious_gates = current_gates - placed_gates
    swap = fix_with_swap(circuit, order, bit, suspicious_gates, remaining_gates)
    swaps.append(swap)
    # As the circuit has changed, we need to recompute the topological order
    order = {wire: n for n, wire in enumerate(circuit.topo_sort())}
    print(f"Bit {bit} fails, fixed with {swap} ({len(suspicious_gates)})")

print(",".join(sorted(chain.from_iterable(swaps))))
# build_dot(circuit, bit_max=None).write_png("circuit_fixed.png")
