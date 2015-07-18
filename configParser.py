
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parseConfigFile(confFileName):

    questionTree = {}

    with open(confFileName) as configFile:
        lines = configFile.readlines()
        build_tree(questionTree, lines, 0, len(lines))

    return questionTree

def get_next_vals(lines, i):
    tokens = lines[i].strip().split(" ")
    print tokens[0], " ".join(tokens[1:]), i + 1
    return tokens[0], " ".join(tokens[1:]), i + 1

# returns the line number that the function ended at
def build_tree(cur_node, lines, i, max_len):
    if (i >= max_len): return i
    flag, value, i = get_next_vals(lines, i)
    if (flag == "#"):
        cur_node["#"] = value
        flag, value, i = get_next_vals(lines, i)
        cur_node["A"] = value
        flag, value, i = get_next_vals(lines, i)
        cur_node["N"] = int(value)
        return i
    if (flag == "Q"):
        cur_node["Q"] = value
        flag, value, i = get_next_vals(lines, i)
        cur_node["A"] = value
        flag, value, i = get_next_vals(lines, i)
        cur_node["N"] = int(value)
        for child_num in xrange(1, cur_node["N"] + 1):
            cur_node[str(child_num)] = new_child = {} 
            i = build_tree(new_child, lines, i, max_len)
        return i