#!/usr/local/bin/python3
import sys
import argparse
import shutil
from queue import PriorityQueue
from collections import defaultdict

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
	def Huffman_code(self):
		global encode_map
		if(self != None):
			if self.left != None:
				self.left.Huffman_code()
			if self.code != None:
				encode_map[self.key]=self.code
			if self.right != None:
				self.right.Huffman_code()

	# inorder_traversal of tree
	def inorder_traversal(self, encoding, count):
		if(self != None):
			if self.left != None:
				encoding.insert(count, 0)
				self.left.inorder_traversal(encoding, count+1)
			if self.right != None:
				encoding.insert(count, 1)
				self.right.inorder_traversal( encoding, count+1)
			if self.left == None and self.right == None:
				encode=str()
				for itr in range(count):
					encode += str(encoding[itr])
				self.code=encode

# count the frequency of character in file
def get_frequencies(content):
	charcounts = defaultdict(int)
	for char in content:
		charcounts[char] = charcounts[char]+  1
		if not char:
			break
	return charcounts
# create priority queue inorder to maintain sorted order
def generate_PriorityQueue(myQueue, charcounts):
		for char,count in charcounts.items():
			root = Node(char, count)
			myQueue.put((count, char, root))

# encode the input files
def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	file1 = open(input_file, 'r')
	contents = file1.read()
	charcounts = get_frequencies(contents)
	file1.close()
	# create priority queue inorder to maintain sorted order
	myQueue = PriorityQueue()
	generate_PriorityQueue(myQueue, charcounts)
	global encode_map
	last_node = []
	encoding = []
	# iterate over priority queue for creating tree by taking first two elements in myQueue
	counter = 1
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
	# Traversing over the root node of tree inorder to set the encode string for tree elements
	counter = 0
	last_node.inorder_traversal(encoding, counter)
	last_node.Huffman_code()
	# write the encoded data to output file
	write_outputfile(input_file,output_file,encode_map)
	file = open(output_file, 'a+')
	file.write("`")
	for char,encode in encode_map.items():
		if char != '':
			file.write(str(char))
			file.write(str(encode))
			file.write('`')
	file.close()

def write_outputfile(input_file,output_file,encode_map):
	file1 = open(input_file, 'r')
	file_content = file1.read()
	file1.close()
	file2 = open(output_file, 'w+')
	char = str()
	# write the encoded/decoded data to output file
	for line in file_content:
		char += line
		if char in encode_map.keys():
			file2.write(encode_map[char])
			char = str()
		if char == '`':
			break
	file2.close()

# decode the input files
def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	encode_map = {}
	file1 = open(input_file, 'r')
	char_str = str()
	count = 0
	# Read the encoded map from input file
	while 1:
		char = file1.read(1)
		# separating the encode and map by special character
		if char == '`':
			count = count + 1
			if count != 1:
				encode_map[char_str[1:]] = char_str[0]
			char_str = str()
		else:
			char_str += char
		if not char:
			break
	file1.close()
	write_outputfile(input_file,output_file,encode_map)

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
