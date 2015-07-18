
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parseConfigFile(confFileName):

	questionTree = {}

	with open(confFileName) as configFile:
		build_tree(questionTree, configFile)

	return questionTree

def get_next_vals(f):
	cur_line = f.readline()
	if cur_line == "":
		return None, None
	tokens = cur_line.strip().split(" ")
	return tokens[0], " ".join(tokens[1:])

def build_tree(cur_node, configFile):
	flag, value = get_next_vals(configFile)
	print flag, value
	child_count = 0
	if flag is None:
		return
	elif (flag == "#"):
		cur_node[flag] = value
		return
	elif (is_number(flag) or flag == "Q" or flag == "$"):
		while True:
			cur_node[flag] = value
			child_count += 1
			cur_node[child_count] = child_node = {}
			build_tree(child_node, configFile)
			flag, value = get_next_vals(configFile)
			print flag, value
			if flag is None: return
