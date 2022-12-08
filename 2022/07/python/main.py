import sys


def Node(name, type_=None, size=None):
    return {
        "name": name,
        "type": type_,
        "size": size,
        "children": {},
    }


hist = []

for row in sys.stdin:
    row = row.rstrip()

    if row.startswith("$ cd "):
        dest = row[5:]
        if not hist:
            hist.append(Node(dest, type_="dir"))
        elif dest == "..":
            _ = hist.pop()
        else:
            hist.append(hist[-1]["children"][dest])

    elif row == "$ ls":
        pass
    else:
        size, name = row.split()
        if size == "dir":
            type_, size = "dir", None
        else:
            type_, size = "file", int(size)
        hist[-1]["children"][name] = Node(name=name, type_=type_, size=size)


def show(root):
    stack = [(0, root)]
    while stack:
        depth, node = stack.pop()
        name, type_, size = node["name"], node["type"], node["size"]
        if size is None:
            print(f"{'  ' * depth} - {name} ({type_})")
        else:
            print(f"{'  ' * depth} - {name} ({type_}, size={size})")
        for c in reversed(node["children"].values()):
            stack.append((depth + 1, c))


def set_dir_size(root):
    if root["size"] is None:
        root["size"] = sum(set_dir_size(c) for c in root["children"].values())
    return root["size"]


def find_with(root, func):
    results = []
    stack = [root]
    while stack:
        node = stack.pop()
        if func(node):
            results.append(node)
        for c in node["children"].values():
            stack.append(c)
    return results


# COMMON
#
root = hist[0]
set_dir_size(root)
# show(root)

# PART 1
#
func = lambda n: n["type"] == "dir" and n["size"] <= 100_000
print(sum(node["size"] for node in find_with(root, func)))


# PART 2
#
AVAILABLE = 70_000_000
NEEDED = 30_000_000
to_free = root["size"] + NEEDED - AVAILABLE

func = lambda n: n["type"] == "dir" and n["size"] >= to_free
print(min(node["size"] for node in find_with(root, func)))
