import os
import re
import string
import sys

# Extract the meaningful part of the run command
def purify(run_command):
	# Prune the redirection
	redirect_index = run_command.find("<")
	if redirect_index != -1:
		run_command = run_command[:redirect_index-1]
	run_command = run_command.rstrip()
	return run_command

# Strip the useless characters and unify the output
def unify(raw_output):
	# Get rid of the prepend words
	colon_index = raw_output.find(":")
	raw_output = raw_output[colon_index+1:]
	# Replace the commas with white space 
	raw_output = raw_output.replace(",", " ")
	# Split the raw output
	output_in_list = raw_output.split()
	return output_in_list

# Check if two lists are the same
def same_list(list1, list2):
	len1 = len(list1)
	len2 = len(list2)
	if len1 != len2:
		return False
	for i in range(0, len1):
		if list1[i] != list2[i]:
			return False
	return True

# Check the output content against the answer
def check_lab1_output(test_index):
	# Unify the output file content
	output_file = open('output' + str(test_index), 'r')
	literals_in_output = output_file.readline()
	numerics_in_output = output_file.readline()
	op_brack_in_output = output_file.readline()
	cl_brack_in_output = output_file.readline()
	output_file.close()
	unified_literals = unify(literals_in_output)
	unified_numerics = unify(numerics_in_output)
	unified_op_brack = unify(op_brack_in_output)
	unified_cl_brack = unify(cl_brack_in_output)
	# Get the correct answer
	answer_file = open('../output/output' + str(test_index), 'r')
	literals_in_answer = answer_file.readline()
	numerics_in_answer = answer_file.readline()
	op_brack_in_answer = answer_file.readline()
	cl_brack_in_answer = answer_file.readline()
	answer_file.close()
	correct_literals = unify(literals_in_answer)
	correct_numerics = unify(numerics_in_answer)
	correct_op_brack = unify(op_brack_in_answer)
	correct_cl_brack = unify(cl_brack_in_answer)
	# Verify the correctness of the output
	if not same_list(unified_literals, correct_literals):
		print("Literals are different.")
		return
	if not same_list(unified_numerics, correct_numerics):
		print("Numerics are different.")
		return
	if not same_list(unified_op_brack, correct_op_brack):
		print("Open parenthesis are different.")
		return
	if not same_list(unified_cl_brack, correct_cl_brack):
		print("Closing parenthesis are different.")
		return
	print("Correct!")

def check_lab2_output_simple(case_index):
	raw_answer_file = open('../output/output' + str(case_index), 'r')
	raw_output_file = open('output' + str(case_index), 'r')
	raw_answer = raw_answer_file.read().strip()
	raw_output = raw_output_file.read().strip()
	raw_answer_file.close()
	raw_output_file.close()
	if raw_answer == raw_output:
		print 'case ' + str(case_index) + ': pass'
	else:
		print 'case ' + str(case_index) + ': fail'
		print raw_output


def check_lab2_output(case_index):
	"""Check the correctness of lab2 output case [index]"""
	raw_answer_file = open('../output/output' + str(case_index), 'r')
	raw_output_file = open('output' + str(case_index), 'r')
	good_answer_file = open('good_answer' + str(case_index), 'w')
	good_output_file = open('good_output' + str(case_index), 'w')

	# Unify the raw output and the raw answer
	raw_answer = raw_answer_file.read()
	good_answer = raw_answer + " "
	good_answer = good_answer.replace(".", " . ")
	good_answer = good_answer.replace("(", " ( ")
	good_answer = good_answer.replace(")", " ) ")
	good_answer = re.sub(" +", " ", good_answer)
	good_answer = good_answer.replace("\n", "")
	good_answer_file.write(good_answer)
	raw_answer_file.close()
	good_answer_file.close()

	raw_output = raw_output_file.read()
	good_output = raw_output + " "
	good_output = good_output.replace(".", " . ")
	good_output = good_output.replace("(", " ( ")
	good_output = good_output.replace(")", " ) ")
	good_output = re.sub(" +", " ", good_output)
	good_output = good_output.replace("\n", "")
	good_output_file.write(good_output)
	raw_output_file.close()
	good_output_file.close()
	
	if good_answer == good_output:
		print 'case ' + str(case_index) + ': pass'
	else:
		print 'case ' + str(case_index) + ': fail'
		print good_output

#os.system('diff good_output' + str(case_index) + 
#						' good_answer' + str(case_index))

# Run the program against all the input test cases
def test_program(num_of_test_cases):
	# Get the correct run command
	if os.path.isfile('Runfile'):
		runfile = open('Runfile', 'r')
	elif os.path.isfile('Runfile.txt'):
		runfile = open('Runfile.txt', 'r')
	elif os.path.isfile('runfile'):
		runfile = open('runfile', 'r')
	elif os.path.isfile('runfile.txt'):
		runfile = open('runfile.txt', 'r')
	else:
		print('Bad runfile.')
		return
	run_cmd = runfile.readline()
	runfile.close()
	run_cmd = purify(run_cmd)
	# Run the program against every test input
	for index in range(1, num_of_test_cases + 1):
		cur_cmd = run_cmd + " < ../input/input" + str(index) \
							+ " > output" + str(index)
		os.system(cur_cmd)
		# Get the info out of the output file
		check_lab2_output_simple(index)


# Global variables
case_nr = 50

# Iterate over the directories
for dir_name in os.listdir("."):
	# Only consider directories
	if not os.path.isdir("./" + dir_name):
		continue
	# Ignore input and output folder
	if dir_name == "input" or dir_name == "output":
		continue
	# Dive into the directory
	os.chdir("./" + dir_name)
	# Test the program
	sys.stderr.write("Testing [" + dir_name + "]")
	test_program(case_nr)
	sys.stderr.write("\n")
	# Go back to root directory
	os.chdir("..")

