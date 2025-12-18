use std::io::{self, Read};
use std::time::Instant;

fn digits_u64(mut n: u64, buf: &mut [u8; 20]) -> &[u8] {
    if n == 0 {
        buf[19] = 0;
        return &buf[19..20];
    }
    let mut i = 20;
    while n != 0 {
        i -= 1;
        buf[i] = (n % 10) as u8;
        n /= 10;
    }
    &buf[i..20]
}

#[inline(always)]
fn is_periodic(d: &[u8], p: usize) -> bool {
    // Checks d[i] == d[i - p] for all i >= p
    for i in p..d.len() {
        if d[i] != d[i - p] {
            return false;
        }
    }
    true
}

#[inline(always)]
fn is_invalid_part1_digits(d: &[u8]) -> bool {
    let len = d.len();
    if (len & 1) != 0 {
        return false;
    }
    let half = len / 2;
    for i in 0..half {
        if d[i] != d[i + half] {
            return false;
        }
    }
    true
}

#[inline(always)]
fn is_invalid_part2_digits(d: &[u8]) -> bool {
    let len = d.len();
    for p in 1..=(len / 2) {
        if len % p == 0 && is_periodic(d, p) {
            return true;
        }
    }
    false
}

fn main() {
    // Read all stdin
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let input = input.trim();
    if input.is_empty() {
        return;
    }

    let start_time = Instant::now();

    let mut buf = [0u8; 20];
    let mut total_part_1: u128 = 0;
    let mut total_part_2: u128 = 0;

    for range in input.split(',') {
        let range = range.trim();
        if range.is_empty() {
            continue;
        }
        let (a_str, b_str) = range
            .split_once('-')
            .expect("Each range must look like a-b");

        let a: u64 = a_str.trim().parse().unwrap();
        let b: u64 = b_str.trim().parse().unwrap();

        for i in a..=b {
            let d = digits_u64(i, &mut buf);

            if is_invalid_part1_digits(d) {
                total_part_1 += i as u128;
            }
            if is_invalid_part2_digits(d) {
                total_part_2 += i as u128;
            }
        }
    }

    println!("{total_part_1}");
    println!("{total_part_2}");

    let duration = start_time.elapsed();
    println!("Time elapsed in main() is: {:?}", duration);
}

