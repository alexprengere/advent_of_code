use std::io;

fn main() {
    let mut data = Vec::new();
    let mut acc = 0;
    for line in io::stdin().lines() {
        match line.unwrap().parse::<i32>() {
            Ok(n) => acc += n,
            _ => {
                data.push(acc);
                acc = 0;
            },
        }
    }
    data.push(acc);
    data.sort();
    println!("{:?}", data.iter().rev().take(3).sum::<i32>());
}
