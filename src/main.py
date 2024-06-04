#! /usr/bin/python3

# ITERATION_01:
# - Removed sliding window
# - Added capability to compress/decompress (length > back-distance) cases
# - MAX lenghth and back-distance encoded.
# - Search algo is attrociously slow

decompressed_stream = ""
output_stream = ""
search_buffer = "AYABRACADABRAABRALOUISISGAYABRACAABCABCABCABCABCABCQWERT"

def hash_match(string_idx):
	MIN_MATCH_LEN = 4
	MAX_MATCH_LEN = 255
	MAX_SEARCH_DIST = 255

	# Set a static variable
	if not hasattr(hash_match, "hash_map"):
		hash_match.hash_map = {}

	hash_map = hash_match.hash_map
	
	# if the key doesn't exit, add it.
	if not search_buffer[string_idx:string_idx+MIN_MATCH_LEN] in hash_map.keys():
		hash_map[search_buffer[string_idx:string_idx+MIN_MATCH_LEN]] = string_idx

		# Check for dictionary overflow and reconstrain it
		if len(hash_map) > MAX_SEARCH_DIST:
			del hash_map[list(hash_map.keys())[0]]

		return (0, 0)
	
	# Otherwise start looking for the length of the match
	match_idx = hash_map[search_buffer[string_idx:string_idx+MIN_MATCH_LEN]]

	y = MIN_MATCH_LEN

	for _ in range(0, MAX_MATCH_LEN+1):
		if string_idx+y >= len(search_buffer):
			break
		elif search_buffer[match_idx+y] != search_buffer[string_idx+y]:
			break
		else:
			y += 1

	return (string_idx-match_idx, y)

def stupid_match(string_idx):
	MIN_MATCH_LEN = 4
	MAX_MATCH_LEN = 255
	MAX_SEARCH_DIST = 255

	max_len_tup = (0, 0)

	start_location = (string_idx - MAX_SEARCH_DIST) if string_idx > MAX_SEARCH_DIST else 0

	# Step 1: Find the first character that matches
	for x in range(start_location, string_idx):
		if search_buffer[string_idx] != search_buffer[x]:
			continue

		# Step 2: If a match is found, find the length of the match.
		y = 1

		# Clever trick: Allows for going past string idx, i.e. distance < length.
		# WARN: String out-of-range guard not included. Python is immune to this, but heed in other languages.
		for _ in range(0, MAX_MATCH_LEN+1):
			if search_buffer[string_idx+y] != search_buffer[x+y]:
				break
			else:
				y += 1

		if y > max_len_tup[1]:
			max_len_tup = (string_idx-x, y)

		# Append a tuple (back-distance, length)

	# Step 3: Return a valid search result
	if max_len_tup[1] < MIN_MATCH_LEN:
		return (0, 0)
	else:
		return max_len_tup


def emit(inp):
	global output_stream
	PRINT_MODE = False

	if type(inp) == type((0, 0)):
		output_stream += "!"+str(chr(inp[0]))+str(chr(inp[1]))
		if PRINT_MODE: print("!", ord(str(chr(inp[0]))),ord(str(chr(inp[1]))), end=" ", sep=" ")
	elif inp == "!":
		output_stream += "!!"
		if PRINT_MODE: print("!!", end="")
	else:
		output_stream += inp
		if PRINT_MODE: print(ord(inp), end=" ")

	return


def LZcompress():
	match_func = hash_match
	string_idx = 0

	while string_idx < len(search_buffer):
		ld_pair = match_func(string_idx)
		
		# For valid (d, l) pair and 'd' not matching '!' character
		if (ld_pair != (0, 0)) and ld_pair[0] != 33:
			emit(ld_pair)
			string_idx += ld_pair[1]
			continue
		
		emit(search_buffer[string_idx])

		string_idx += 1

	return

def LZdecompress():
	global decompressed_stream

	idx = 0

	while idx < len(output_stream):
		if output_stream[idx] != "!":
			decompressed_stream += output_stream[idx]
			idx += 1
		else:
			if output_stream[idx+1] == "!":
				decompressed_stream += "!"
				idx += 2
			else:
				back_distance, length = ord(output_stream[idx+1]), ord(output_stream[idx+2])

				# Decompress one-by-one, allows (length > distance) cases
				for _ in range(0, length):
					decompressed_stream += decompressed_stream[-back_distance : -back_distance + 1]

				idx += 3

	return

# Read a file into a string
with open("../sample_file.txt", "r") as f:  # Open the file in read mode ("r")
	search_buffer = f.read()  # Read the entire content into a string

LZcompress()
LZdecompress()

if search_buffer == decompressed_stream:
	print("Decompression Successful, matches with source.")
	print(f"Size of Original: {len(search_buffer)}. Size of comressed: {len(output_stream)}")
	print(f"Compression Ratio: {len(search_buffer)/len(output_stream):.3f}")
	print(f"Size Reduction: {(1-len(output_stream)/len(search_buffer))*100:.2f} %")
else:
	if False:
		same_count = 0
		mismatch_idx_list = []

		for x in range(0, min(len(search_buffer), len(decompressed_stream))):
			if search_buffer[x] == decompressed_stream[x]:
				same_count += 1
			else:
				mismatch_idx_list.append(x)
				

		print(f"Decompression Failed, Match count: {same_count} {same_count/len(search_buffer)*100:.3f}%.")
		print(f"Mismatches at: {mismatch_idx_list}")
		
		a = mismatch_idx_list[0]

		print("ORIGINAL: ", end="")

		for x in range(-1, 10):
			print(ord(search_buffer[a+x]), end=" ")
		
		print("\nDECOMPRE: ", end="")

		for x in range(-1, 10):
			print(ord(decompressed_stream[a+x]), end=" ")
	else:
		print("\nORIGINAL:")
		for x in range(0, len(search_buffer)):
			print(ord(search_buffer[x]), end = " ")
		print("\nDECOMPRE:")
		for x in range(0, len(decompressed_stream)):
			print(ord(decompressed_stream[x]), end = " ")


print()