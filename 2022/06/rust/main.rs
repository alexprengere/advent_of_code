use std::io;

fn main() {
    let mut signal = String::new();
    io::stdin().read_line(&mut signal).unwrap();
    let signal = signal.trim_end();

    let size = 4;  // part 1: put 4 instead

    for n in size..signal.len() + 1 {
        let substring: String = signal[n - size..n].to_string();
        let set: std::collections::HashSet<char> = substring.chars().collect();
        if set.len() == size {
            println!("{}", n);
            break;
        }
    }
}
