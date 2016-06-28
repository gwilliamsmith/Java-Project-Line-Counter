import os,glob,sys

def listFiles(directory = None, defaultColumnSpace = 5):
	if directory == None:
		try:
			directory = sys.argv[1]
		except IndexError:
			directory = input("Enter a directory to check: ")
	try:
		defaultColumnSpace = int(sys.argv[2])
	except IndexError:
		pass
	exploreFile = -1;
	try:
		exploreFile = int(sys.argv[3])
	except IndexError:
		pass
	print("Directory: \n" + directory)
	os.chdir(directory)
	totallines = 0
	total2 = 0
	toPrint = []
	listOfFiles = []
	for root,dirs,files in os.walk(directory):
		for name in files:
			if(name.endswith(".java")):
				lines,lines2 = linesOfCode(os.path.join(root,name))
				if lines == lines2:
					toPrint.append([os.path.join(root,name),str(lines) + "/" + str(lines2)])
				else:
					toPrint.append([os.path.join(root,name),(str(lines) + "/" + str(lines2)),"*****"])
				totallines += lines
				total2 += lines2
				listOfFiles.append(os.path.join(root,name))
	columnWidths = calculateColumnWidths(toPrint)
	for item in toPrint:
		colIndex = 0
		for i in item:
			print(i,end="")
			if len(i) < (columnWidths[colIndex] + defaultColumnSpace):
				spaceCount = (columnWidths[colIndex] + defaultColumnSpace) - len(i)
				while spaceCount > 0:
					print(" ",end="")
					spaceCount -= 1
			colIndex+=1
		print("")
	print("\nTotal lines: " + str(totallines) +"/"+str(total2))
	input()
	if exploreFile != -1:
		print("Exploring: " + listOfFiles[exploreFile])
		displayWithoutComments(listOfFiles[exploreFile])

def linesOfCode(fname):
	with open(fname) as f:
		lines = 0
		lines2 = 0
		check = f.readlines()
		skip = False
		for l in check:
			line = l.strip()
			if not skip:
				if line.startswith("/*") and "*/" not in line:
					skip = True
				if not line.startswith("//") and not skip:
					lines += 1
			else:
				if "*/" in line:
					skip = False
			lines2 += 1
	return lines,lines2

def calculateColumnWidths(items):
	widths = [0] * calculateNumberOfColumns(items)
	for item in items:
		widthsIndex = 0;
		for i in item:
			if len(i) > widths[widthsIndex]:
				widths[widthsIndex] = len(i)
			widthsIndex += 1
	return widths

def calculateNumberOfColumns(items):
	out = 0
	for item in items:
		if len(item) > out:
			out = len(item)
	return out

def displayWithoutComments(file):
	with open(file) as f:
		lines = 0
		lines2 = 0
		check = f.readlines()
		skip = False
		for l in check:
			line = l.strip()
			if not skip:
				if line.startswith("/*") and "*/" not in line:
					skip = True
				if not line.startswith("//") and not skip:
					lines += 1
					print(l)
			else:
				if "*/" in line:
					skip = False
			lines2 += 1
	return lines,lines2

if __name__ == '__main__':
	listFiles()