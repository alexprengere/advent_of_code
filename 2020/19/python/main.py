import sys

rules = {}
messages = []
part = 1
for row in sys.stdin:
    row = row.rstrip()
    if not row:  # blank lines means we read messages now
        part = 2
        continue
    if part == 1:
        name, data = row.split(": ")
        if '"' in data:
            rules[name] = data.strip('"')
        else:
            rules[name] = [sub.split() for sub in data.split(" | ")]
    elif part == 2:
        messages.append(row)


def match(rules, rule, message):
    if isinstance(rule, str):  # looks like "a"
        if message and message[0] == rule:
            yield 1
        return
    for first, *rest in rule:  # looks like [['1', '3'], ['3', '1']]
        for p in match(rules, rules[first], message):
            for p_rest in match(rules, [rest], message[p:]) if rest else [0]:
                yield p + p_rest


def complete_match(rules, rule_name, message):
    return len(message) in match(rules, [[rule_name]], message)


# PART 1
#
print(sum(complete_match(rules, "0", m) for m in messages))


# PART 2
#
rules.update(
    {  # Manual override
        "8": [["42"], ["42", "8"]],
        "11": [["42", "31"], ["42", "11", "31"]],
    }
)
print(sum(complete_match(rules, "0", m) for m in messages))
