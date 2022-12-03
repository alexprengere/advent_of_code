use std::io;

#[derive(PartialEq, Eq)]
enum Shape {
    Rock,
    Paper,
    Scissors,
}

impl Shape {
    fn score(&self) -> i32 {
        match *self {
            Shape::Rock => 1,
            Shape::Paper => 2,
            Shape::Scissors => 3,
        }
    }
}

fn outcome(a: Shape, b: Shape) -> i32 {
    match (a, b) {
        (Shape::Rock, Shape::Paper) => 0,
        (Shape::Paper, Shape::Scissors) => 0,
        (Shape::Scissors, Shape::Rock) => 0,
        (x, y) if x == y => 3,
        (_, _) => 6,
    }
}

fn main() {
    let mut score = 0;
    for line in io::stdin().lines() {
        let op_move = line.as_ref().unwrap().chars().nth(0).unwrap();
        let my_move = line.as_ref().unwrap().chars().nth(2).unwrap();

        let op_shape = match op_move {
            'A' => Shape::Rock,
            'B' => Shape::Paper,
            'C' => Shape::Scissors,
            _ => panic!("Unknown move"),
        };
        let my_shape = match my_move {
            'X' => Shape::Rock,
            'Y' => Shape::Paper,
            'Z' => Shape::Scissors,
            _ => panic!("Unknown move"),
        };
        score += my_shape.score() + outcome(my_shape, op_shape);
    }
    println!("{score}");
}
