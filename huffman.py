#!/usr/local/bin/python3
import sys
import argparse
import shutil
from queue import PriorityQueue
from collections import defaultdict

# structure of Tree Node
class Node:
	def __init__(self, key, value):
		self.left = None
		self.right = None
		self.key = key
		self.value = value
		self.code=None
	# traversing over tree for setting the encode string
	def inorder_traversal(self, encoding, count, encode_map):
		if(self != None):
			if self.left != None:
				encoding.insert(count, 0)
				self.left.inorder_traversal(encoding, count+1, encode_map)
			if self.right != None:
				encoding.insert(count, 1)
				self.right.inorder_traversal( encoding, count+1, encode_map)
			if self.left == None and self.right == None:
				encode=str()
				for itr in range(count):
					encode += str(encoding[itr])
				self.code=encode
				if self.code != None:
					encode_map[self.key]=self.code

# count the frequency of character in file
def get_frequencies(content):
	charcounts = defaultdict(int)
	for char in content:
		charcounts[char] = charcounts[char]+  1
		if not char:
			break
	return charcounts

# create priority queue inorder to maintain sorted order
def generate_priorityqueue(myQueue, charcounts):
		for char,count in charcounts.items():
			root = Node(char, count)
			myQueue.put((count, char, root))

# iterate over priority queue for generating tree
def  generate_tree(myQueue):
	counter = 1
	last_node = []
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
			# Taking first two elements in myQueue for generating tree
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
	return last_node

# write the encoded information to output file
def encode_outputfile(input_file, output_file, encode_map):
	# write the encode map length and contents to output file
	file = open(output_file, 'wb+')
	file.write(len(encode_map).to_bytes(1, byteorder='big', signed=False))
	for char,encode in encode_map.items():
		if char != '':
			file.write(str(char).encode())
			file.write(str(encode).encode())
			file.write(str('`').encode())
	# create the encoded data using map
	file1 = open(input_file, 'r')
	file_content = file1.read()
	file1.close()
	char = str()
	encode_data =''
	encode_data = ''.join([encode_map[char] for char in file_content])
	# zero padding the encoded data inorder to write as bytes in output file
	pad_size = 8 - len(encode_data) % 8
	if pad_size == 8:
		pad_size = 0
	pad_data = '0' * pad_size
	encode_data = encode_data + pad_data
	# write the zero pad size into output file
	file.write(str(pad_size).encode())
	# write the encoded data into output file
	byte_content = bytearray()
	for i in range(0, len(encode_data), 8):
		byte_content.append(int(encode_data[i:i+8], 2))
	file.write(bytes(byte_content))
	file.close()

# convert the binary to string
def convert_to_char(input_str):
	size = int('0b'+input_str, 2)
	char = size.to_bytes((size.bit_length() + 7) // 8, 'big').decode()
	return char

# get the encoded map and encoded data from input file
def decode_inputfile(input_file, encode_map):
	with open(input_file, 'rb') as input_fp:
		byte_data = str()
		# read the input file as bytes
		byte = input_fp.read(1)
		while len(byte) > 0:
			byte_data += f"{bin(ord(byte))[2:]:0>8}"
			byte = input_fp.read(1)
		# get the encoded map length
		map_datasize = byte_data[:8]
		map_size = int(map_datasize, base=2)
		# get the map content as string
		index = 1
		count = 0
		char_str = str()
		map_str =  str()
		while(count < map_size):
			char = convert_to_char(byte_data[index*8:(index+1)*8])
			index += 1
			if char == '`':
				map_str += char_str + char
				count += 1
				char_str = str()
			else:
				char_str += char
		# generate encode_map from string
		for char in map_str:
			if char == '`':
				encode_map[char_str[1:]] = char_str[0]
				char_str = str()
			else:
				char_str += char
			if not char:
				break
		# get the pad data
		pad_data = byte_data[index*8:(index+1)*8]
		# get the encoded_data by rempving the pad data
		encoded_data = byte_data[(index+1)*8:]
		encoded_data = encoded_data[:-int(convert_to_char(pad_data))]
		return encoded_data

# write the original data by decoding the encoded data using map
def write_outputfile(output_file, encode_map, encoded_data):
	with open(output_file, 'w+') as output_fp:
		char = str()
		for line in encoded_data:
			char += line
			if char in encode_map.keys():
				# decode using map value
				output_fp.write(encode_map[char])
				char = str()
			if char == '`':
				break

# encode the input files
def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	file1 = open(input_file, 'r')
	# counting the character frequecies of input file
	charcounts = get_frequencies(file1.read())
	file1.close()
	# create priority queue(inorder to maintain sorted order) using frequency count
	myQueue = PriorityQueue()
	generate_priorityqueue(myQueue, charcounts)
	# iterate over priority queue for generating tree by taking first two elements in myQueue
	last_node = generate_tree(myQueue)
	# Traversing over the root node of tree inorder to set the encode string for tree elements and generate encode map
	counter = 0
	encoding = []
	encode_map = {}
	last_node.inorder_traversal(encoding, counter, encode_map)
	# write the encoded information to output file
	encode_outputfile(input_file, output_file, encode_map)

# decode the input files
def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	encode_map ={}
	# get the encoded map and encoded data from input file
	encoded_data = decode_inputfile(input_file, encode_map)
	# write the original data by decoding the encoded data using map
	write_outputfile(output_file, encode_map, encoded_data)
	return True

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
