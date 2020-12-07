use std::io::{self, BufRead};

fn process_line(line: Vec<&str>) -> bool {
    let (range, letter, password) = (line[0], line[1], line[2]);
    let range: Vec<&str> = range.split("-").collect();
    let first = range[0].parse::<usize>().unwrap();
    let last = range[1].parse::<usize>().unwrap();
    let letter = letter.chars().nth(0).unwrap();

    let mut validated = 0;
    for &pos in &[first, last] {
        if password.chars().nth(pos - 1).unwrap() == letter {
            validated += 1
        }
    }
    validated == 1
}

fn main() {
    let stdin = io::stdin();

    let mut total_valid = 0;
    for line in stdin.lock().lines() {
        let is_valid = process_line(line.unwrap().split(' ').collect());
        if is_valid {
            total_valid += 1;
        }
    }
    println!("{}", total_valid);
}
