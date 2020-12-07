use itertools::Itertools;
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();

    let mut data = Vec::new();
    for line in stdin.lock().lines() {
        data.push(line.unwrap().parse::<i32>().unwrap());
    }

    for numbers in data.iter().combinations(3) {
        if numbers.iter().map(|&x| x).sum::<i32>() == 2020 {
            println!("{}", numbers.iter().fold(1, |a, &b| a * b));
        }
    }
}
