import os
import sys

#pylint: disable-msg=missing-docstring


def list_files(directory=None, default_column_space=5):
	detail = False
	explore_file = -1;
	if directory == None:
		try:
			directory = sys.argv[1]
		except IndexError:
			directory = input("Enter a directory to check: ")
	try:
		default_column_space = int(sys.argv[2])
	except IndexError:
		pass
	try:
		explore_file = int(sys.argv[3])-1
	except IndexError:
		pass
	try:
		detail = str(int(sys.argv[4]) == 1)
	except IndexError:
		pass
	print("Directory: " + directory + "\n\n")
	os.chdir(directory)
	total_lines = 0
	total_lines_without_comments = 0
	total_global_variables = 0
	total_methods = 0
	to_print = []
	list_of_files = []
	for root, dirs, files in os.walk(directory):
		for name in files:
			if(name.endswith(".java")):
				lines, lines_without_comments, global_variables, methods = lines_of_code(os.path.join(root, name), detail)
				if lines == lines_without_comments:
					to_print.append([os.path.join(".\\", name), str(lines) + "/" + str(lines_without_comments), str(global_variables), str(methods)])
				else:
					to_print.append([os.path.join(".\\", name), (str(lines) + "/" + str(lines_without_comments)), str(global_variables) , str(methods), "*****"])
				total_lines += lines
				total_lines_without_comments += lines_without_comments
				list_of_files.append(os.path.join(root, name))
	column_headers = ["File Name","Line Count (No Comments/Comments)", "Global Variables", "Methods"]
	to_print.insert(0,column_headers)
	column_widths = calculate_column_widths(to_print)
	for item in to_print:
		col_index = 0
		for i in item:
			print(i, end="")
			if len(i) < (column_widths[col_index] + default_column_space):
				space_count = (column_widths[col_index] + default_column_space) - len(i)
				while space_count > 0:
					print(" ", end="")
					space_count -= 1
			col_index += 1
		print("")
	print("\nTotal lines: " + str(total_lines) +"/"+str(total_lines_without_comments))
	if explore_file != -1:
		input()
		print("Exploring: " + list_of_files[explore_file])
		display_without_comments(list_of_files[explore_file])

def lines_of_code(fname, detail):
	with open(fname) as examine:
		lines_with_comments = 0
		lines_without_comments = 0
		check = examine.readlines()
		skip = False
		global_search = False
		#None,public,private,protected,static,final,synchronized,volatile,total
		global_variables = [0,0,0,0,0,0,0]
		#None,public,private,protected,static,final,abstract,synchronized,volatile, total
		methods = [0,0,0,0,0,0,0,0,0,0]
		open_parens = 0
		for index in check:
			line = index.strip()
			if not skip:
				if line.startswith("/*") and "*/" not in line:
					skip = True
				if not line.startswith("//") and not skip:
					lines_with_comments += 1
					if "class" in line:
						global_search = True
						open_parens += 1
					else:
						if global_search:
							if ("(" in line and ")" in line and ("{" in line or "abstract" in line)):
								if "=" not in line:
									global_search = False
									analyze_method(line, methods)
									open_parens += 1
								else:
									analyze_global_variable(line, global_variables)
								if "}" in line:
									global_search = True
									open_parens -= 1
							else:
								if len(line) > 0:
									analyze_global_variable(line, global_variables)
						else:
							if "{" in line:
								open_parens += 1
							if "}" in line:
								open_parens -= 1
							if open_parens == 1:
								global_search = True
			else:
				if "*/" in line:
					skip = False
			lines_without_comments += 1
	global_variable_string = variable_breakdown(global_variables, detail)
	method_string = method_breakdown(methods, detail)
	return lines_with_comments, lines_without_comments, global_variable_string, method_string

def calculate_column_widths(items):
	widths = [0] * calculate_number_of_columns(items)
	for item in items:
		widths_index = 0
		for i in item:
			if len(i) > widths[widths_index]:
				widths[widths_index] = len(i)
			widths_index += 1
	return widths

def calculate_number_of_columns(items):
	out = 0
	for item in items:
		if len(item) > out:
			out = len(item)
	return out

def display_without_comments(file):
	with open(file) as examine:
		lines = 0
		lines2 = 0
		check = examine.readlines()
		skip = False
		for index in check:
			line = index.strip()
			if not skip:
				if line.startswith("/*") and "*/" not in line:
					skip = True
				if not line.startswith("//") and not skip:
					lines += 1
					print(index)
			else:
				if "*/" in line:
					skip = False
			lines2 += 1
	return lines, lines2

def analyze_method(line, methods):
	methods[9] += 1
	package = True
	if "public" in line:
		methods[1] += 1
		package = False
	if "private" in line:
		methods[2] += 1
		package = False
	if "protected" in line:
		methods[3] += 1
		package = False
	if "static" in line:
		methods[4] +=1
	if "final" in line:
		methods[5] +=1
	if "abstract" in line:
		methods[6] +=1
	if "synchronized" in line:
		methods[7] +=1
	if "volatile" in line:
		methods[8] +=1
	if package:
		methods[0] += 1

def analyze_global_variable(line, global_variables):
	global_variables[6] += 1
	package = True
	if "public" in line:
		global_variables[1] += 1
		package = False
	if "private" in line:
		global_variables[2] += 1
		package = False
	if "protected" in line:
		global_variables[3] += 1
		package = False
	if "static" in line:
		global_variables[4] +=1
	if "final" in line:
		global_variables[5] +=1
	if package:
		global_variables[0] += 1

def variable_breakdown(global_variables, detail):
	part1 = "Package/Public/Private/Protected: " + str(global_variables[0]) +"/" +str(global_variables[1]) +"/" +str(global_variables[2]) +"/" +str(global_variables[3])
	part2 = "Static/Final: " + str(global_variables[4]) +"/"+ str(global_variables[5])
	part3 = "Total: " + str(global_variables[6])
	if detail:
		return part1 + " " + part2 + " " + part3
	else:
		return part3

def method_breakdown(methods, detail):
	part1 = "Package/Public/Private/Protected: " + str(methods[0]) +"/" +str(methods[1]) +"/" +str(methods[2]) +"/" +str(methods[3])
	part2 = "Static/Final/Abstract/Synchronized/Final: " + str(methods[4]) +"/"+ str(methods[5]) + str(methods[6]) +"/"+ str(methods[6])+"/"+ str(methods[8])
	part3 = "Total: " + str(methods[9])
	if detail:
		return part1 + " " + part2 + " " + part3
	else:
		return part3

if __name__ == '__main__':
	list_files()
