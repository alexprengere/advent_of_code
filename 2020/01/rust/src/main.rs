use itertools::Itertools;
use std::io;

fn main() {
    let mut data = Vec::new();
    for line in io::stdin().lines() {
        data.push(line.unwrap().parse::<i32>().unwrap());
    }

    for numbers in data.iter().combinations(3) {
        if numbers.iter().copied().sum::<i32>() == 2020 {
            println!("{}", numbers.iter().copied().product::<i32>());
        }
    }
}
