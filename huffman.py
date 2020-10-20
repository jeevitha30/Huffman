#!/usr/local/bin/python3
import sys
import argparse
import shutil

encode_map={}

# structure of Node
class Node:
	def __init__(self, key, value):
		self.left = None
		self.right = None
		self.key = key
		self.value = value
		self.code=None

# create encoded map using root node of tree
def Huffman_code(root):
	global encode_map
	if(root != None):
		Huffman_code(root.left)
		if root.code != None:
			encode_map[root.key]=root.code
		Huffman_code(root.right)

# inorder_traversal of tree
def inorder_traversal(root, encoding, count):
	if(root != None):
		if root.left != None:
			encoding.insert(count, 0)
			inorder_traversal(root.left, encoding, count+1)
		if root.right != None:
			encoding.insert(count, 1)
			inorder_traversal(root.right, encoding, count+1)
		if root.left == None and root.right == None:
			encode=str()
			for itr in range(count):
				encode += str(encoding[itr])
			root.code=encode

# encode the input files
def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	file1 = open(input_file, 'r')
	count = 0
	charcounts = {}
	# count the frequency of character in file
	while 1:
		char = file1.read(1)
		if (not char in charcounts):
			charcounts[char] = 0
		charcounts[char]  =charcounts[char]+  1
		if not char:
			break
	from queue import PriorityQueue
	myQueue = PriorityQueue()
	# create priority queue inorder to maintain sorted order
	for char,count in charcounts.items():
		root = Node(char, count)
		myQueue.put((count, char, root))
	global encode_map
	last_node = []
	encoding = []
	counter = 1
	file1.close()
	# iterate over priority queue for creating tree by taking first two elements in myQueue
	while not myQueue.empty():
		if counter == 1:
			left = myQueue.get()
		if counter == 2:
			right = myQueue.get()
		if myQueue.qsize() == 0 :
			if counter != 1:
				frequency = left[0] + last_node.value
				char = left[1] + last_node.key
				new_node = Node(char, frequency)
				new_node.left = left[2]
				new_node.right = last_node
				last_node = new_node
		if counter == 3:
			frequency = left[0] + right[0]
			counter = 0
			char = left[1] + right[1]
			new_node = Node(char, frequency)
			new_node.left = left[2]
			new_node.right = right[2]
			last_node = new_node
			if myQueue.qsize() != 0 :
				myQueue.put((frequency, char, new_node))
		counter = counter + 1
	counter = 0
	# Traversing over the root node of tree inorder to set the encode string for tree elements
	inorder_traversal(last_node, encoding, counter)
	Huffman_code(last_node)
	file1 = open(input_file, 'r')
	file_content = file1.read()
	file1.close()
	file2 = open(output_file, 'w+')
	code = str()
	encode = str()
	# write the encoded input file data into output file
	for line in file_content:
		code += line
		if code in encode_map.keys():
			encode += encode_map[code]
			code = str()
	file2.write(encode)
	file2.close()
	file = open('encode_map.txt', 'w')
	for char,encode in encode_map.items():
		if char != '':
			file.write(str(char))
			file.write(str(encode))
			file.write('`')
	file.close()

# decode the input files
def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	encode_map = {}
	file1 = open('encode_map.txt', 'r')
	char_str = str()
	# Read the encoded map from file
	while 1:
		char = file1.read(1)
		if char == '`':
			encode_map[char_str[1:]] = char_str[0]
			char_str = str()
		else:
			char_str += char
		if not char:
			break
	file1.close()
	file1 = open(input_file, 'r')
	file_content = file1.read()
	file2 = open(output_file, 'w+')
	key = str()
	# write the decoded data to output file
	for line in file_content:
		key += line
		if key in encode_map.keys():
			file2.write(encode_map[key])
			key = str()

def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options
if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)
