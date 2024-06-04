#! /usr/bin/python3

# ITERATION_01:
# - Removed sliding window
# - Added capability to compress/decompress (length > back-distance) cases
# - MAX lenghth and back-distance encoded.
# - Search algo is attrociously slow

decompressed_stream = ""
output_stream = ""
search_buffer = "AYABRACADABRAABRALOUISISGAYABRACAABCABCABCABCABCABC"

string_idx = 0

def stupid_match(string_idx):
	global search_buffer

	MIN_MATCH_LEN = 4
	MAX_MATCH_LEN = 255
	MAX_SEARCH_DIST = 4

	possible_matches = []

	start_location = string_idx - MAX_SEARCH_DIST if string_idx > MAX_SEARCH_DIST else 0

	# Step 1: Find the first character that matches
	for x in range(start_location, string_idx-1):
		if search_buffer[string_idx] != search_buffer[x]:
			continue

		# Step 2: If a match is found, find the length of the match.
		y = 1

		# Clever trick: Allows for going past string idx, i.e. distance < length.
		# WARN: String out-of-range guard not included. Python is immune to this, but heed in other languages.
		for _ in range(0, MAX_MATCH_LEN):
			if search_buffer[string_idx:string_idx+y] != search_buffer[x:x+y]:
				break
			else:
				y += 1

		# Append a tuple (back-distance, length)
		possible_matches.append((string_idx-x, y-1))

	# Step 3: Find the match with max length and return it.
	if not possible_matches:
		return (0, 0)
	
	max_len_tup = (possible_matches[0][0], possible_matches[0][1])

	for tup in possible_matches:
		if tup[1] > max_len_tup[1]:
			max_len_tup = (tup[0], tup[1])

	if max_len_tup[1] < MIN_MATCH_LEN:
		return (0, 0)
	else:
		return max_len_tup

def emit(inp):
	global output_stream

	if type(inp) == type((0, 0)):
		output_stream += "!"+str(chr(inp[0]))+str(chr(inp[1]))
	elif inp == "!":
		output_stream += "!!"
	else:
		output_stream += inp

	return


def LZcompress():
	global sliding_window, string_idx
	match_func = stupid_match

	while string_idx < len(search_buffer):
		ld_pair = match_func(string_idx)
		
		if(ld_pair != (0, 0)):
			emit(ld_pair)
			print(ld_pair, end="")
			string_idx += ld_pair[1]
			continue
		
		emit(search_buffer[string_idx])
		print(search_buffer[string_idx], end="")

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

	

LZcompress()
LZdecompress()

print("\n")

print("ORIGINAL:")
print(search_buffer)
print("DECOMPRESSED:")
print(decompressed_stream)

