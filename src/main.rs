#![allow(non_snake_case)]

use std::fs;

fn stupid_match(search_buffer: String, search_loc: usize) -> (i32, i32) {
	let MIN_MATCH_LEN = 4;
	let MAX_MATCH_LEN = 256;
	let MAX_SEARCH_DIST = 256;

    let mut possible_matches: Vec<(i32, i32)> = Vec::new();

    // Decide start location of the search_window
    let start_loc = match search_loc > MAX_SEARCH_DIST {
        true  => search_loc - MAX_SEARCH_DIST,
        false => 0,
    };

    for i in start_loc..search_loc {
        // Step 1: find the first character that matches
        if search_buffer.chars().nth(i).unwrap() !=  search_buffer.chars().nth(search_loc).unwrap() {
            continue;
        }

        // Step 2: If match is found, find the length of the match
        let mut y = 1

        for _ 0..MAX_MATCH_LEN
    }

    return (0, 0);
}

fn main() {
    let bytes = fs::read("../sample_file.txt").unwrap();
    // Process the bytes here
    println!("Read {} bytes from the file", bytes.len());


    let block_len = if bytes.len() > 4096 {4096} else {bytes.len()};

    // declare a string
    let search_buffer = String::from_utf8(bytes[..block_len].to_vec()).unwrap();

    stupid_match(search_buffer, 0);
}