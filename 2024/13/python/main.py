import sys

machines = []
for rows in sys.stdin.read().split("\n\n"):
    machine = []
    for row in rows.splitlines():
        if row.startswith("Button"):
            button, params = row.split(":")
            X, Y = params.split(",")
            X = int(X.split("+")[1])
            Y = int(Y.split("+")[1])
            machine.append((X, Y))
        else:
            prize, params = row.split(":")
            X, Y = params.split(",")
            X = int(X.split("=")[1])
            Y = int(Y.split("=")[1])
            machine.append((X, Y))
    machines.append(machine)


def solve(a_button, b_button, prize):
    a_x, a_y = a_button
    b_x, b_y = b_button
    p_x, p_y = prize

    det = a_x * b_y - a_y * b_x
    # For the record having a null determinant does not mean there are
    # no solutions, it means there are infinite solutions, or none.
    # In that case the two vectors are colinear, and if the prize is
    # on the same line, then there are infinite solutions, otherwise
    # there are none. We can split the ties by using the minimum cost.
    # But it turns out in AoC input, none of the matrices are colinear.
    assert det != 0

    # Now that we know the determinant is not null, we also know that
    # the solution is unique, so we do not bother with the "minimum cost".
    a_sol = (p_x * b_y - p_y * b_x) / det
    b_sol = (a_x * p_y - a_y * p_x) / det

    if a_sol.is_integer() and b_sol.is_integer():
        a_sol = int(a_sol)
        b_sol = int(b_sol)
        return a_sol * 3 + b_sol

    return 0  # only non-integer solutions


# PART 1
#
print(sum(solve(*machine) for machine in machines))


# PART 2
#
offset = 10_000_000_000_000

total_cost = 0
for a_button, b_button, prize in machines:
    p_x, p_y = prize
    total_cost += solve(a_button, b_button, (p_x + offset, p_y + offset))
print(total_cost)


# BONUS PART
#
# This is a more general solution using z3. It is not needed for AoC.
#
def solve_with_z3(a_button, b_button, prize):
    import z3

    a_x, a_y = a_button
    b_x, b_y = b_button
    p_x, p_y = prize

    A = z3.Int("a")
    B = z3.Int("b")

    optimizer = z3.Optimize()
    optimizer.add(a_x * A + b_x * B == p_x)
    optimizer.add(a_y * A + b_y * B == p_y)
    optimizer.minimize(A * 3 + B)

    if optimizer.check() == z3.sat:
        model = optimizer.model()
        a_opt = model[A].as_long()
        b_opt = model[B].as_long()
        return a_opt * 3 + b_opt

    return 0
