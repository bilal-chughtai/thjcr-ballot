import os

def copyIndex(dest, key):
	fIn = open("template/index.html")
	fOut = open(os.path.join(dest, 'index.html'), "w")
	for line in fIn:
		if "REPLACE_THIS_WITH_KEY" in line:
			line = line.replace("REPLACE_THIS_WITH_KEY", key)
		fOut.write(line)
	fIn.close()
	fOut.close()


# TODO