#! /usr/bin/python3

decompressed_stream = ""
output_stream = ""
sliding_window = ""
search_buffer = "AYABRACADABRAABRALOUISISGAYABRACA"

string_idx = 0

def stupid_match(string_idx):
	global sliding_window, search_buffer
	MIN_MATCH_LEN = 3
	possible_matches = []

	# Step 1: Find the first character that matches
	for x in range(0, len(sliding_window)):
		if search_buffer[string_idx] != sliding_window[x]:
			continue

		# Step 2: If a match is found, find the length of the match.
		temp = 1

		for y in range(x, len(sliding_window)):
			if search_buffer[string_idx:string_idx+temp] != sliding_window[x:y+1]:
				break
			else:
				temp += 1

		# Append a tuple (back-distance, length)
		possible_matches.append((string_idx-x, temp-1))

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

match_func = stupid_match

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

	while string_idx < len(search_buffer):
		sliding_window = search_buffer[0:string_idx]

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
				decompressed_stream += decompressed_stream[-back_distance : -back_distance + length]
				idx += 3

	return

	

LZcompress()
LZdecompress()

print("\n")

print("ORIGINAL:")
print(search_buffer)
print("DECOMPRESSED:")
print(decompressed_stream)

