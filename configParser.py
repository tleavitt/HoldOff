

token_mapper = {
	"Q" : 
	""
}

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parseConfigFile(confFileName):

	questionTree = {}

	with open(confFileName) as configFile:
		lines = config.Readlines
		for line in lines:
			tokens = line.split(" ")
			case("Q")


