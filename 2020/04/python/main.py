import sys

REQUIRED = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL = {"cid"}

NUMBERS = set("0123456789")
HEX = set("0123456789abcdef")
EYE_COLORS = set("amb blu brn gry grn hzl oth".split())


def split_passeports(rows):
    passeport = []
    for row in rows:
        fields = row.strip().split()
        if not fields:  # new passeport
            yield passeport
            passeport = []
        else:
            passeport += fields
    yield passeport


def is_valid(passeport):
    data = {}
    for entry in passeport:
        key, value = entry.split(":")
        data[key] = value

    if not REQUIRED.issubset(data):  # missing fields
        return False

    if len(data["byr"]) != 4:
        return False
    byr = int(data["byr"])
    if not 1920 <= byr <= 2002:
        return False

    if len(data["iyr"]) != 4:
        return False
    iyr = int(data["iyr"])
    if not 2010 <= iyr <= 2020:
        return False

    if len(data["eyr"]) != 4:
        return False
    eyr = int(data["eyr"])
    if not 2020 <= eyr <= 2030:
        return False

    hgt = data["hgt"]
    if hgt.endswith("cm"):
        height = int(hgt[:-2])
        if not 150 <= height <= 193:
            return False
    elif hgt.endswith("in"):
        height = int(hgt[:-2])
        if not 59 <= height <= 76:
            return False
    else:
        return False

    if data["hcl"][0] != "#":
        return False
    hcl = data["hcl"][1:]
    if len(hcl) != 6:
        return False
    if not set(hcl).issubset(HEX):
        return False

    if data["ecl"] not in EYE_COLORS:
        return False

    if len(data["pid"]) != 9:
        return False
    if not set(data["pid"]).issubset(NUMBERS):
        return False

    return True


print(sum(is_valid(p) for p in split_passeports(sys.stdin)))
