use std::io;

#[derive(PartialEq, Eq, Clone, Copy)]
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

    fn wins(&self) -> Shape {
        match *self {
            Shape::Rock => Shape::Scissors,
            Shape::Paper => Shape::Rock,
            Shape::Scissors => Shape::Paper,
        }
    }

    fn loses(&self) -> Shape {
        match *self {
            Shape::Rock => Shape::Paper,
            Shape::Paper => Shape::Scissors,
            Shape::Scissors => Shape::Rock,
        }
    }

    fn draws(&self) -> Shape {
        *self
    }
}

enum Outcome {
    Lose,
    Draw,
    Win,
}

impl Outcome {
    fn score(&self) -> i32 {
        match *self {
            Outcome::Lose => 0,
            Outcome::Draw => 3,
            Outcome::Win => 6,
        }
    }
}



fn main() {
    let mut score = 0;
    for line in io::stdin().lines() {
        let op_move = line.as_ref().unwrap().chars().next().unwrap();
        let outcome_code = line.as_ref().unwrap().chars().nth(2).unwrap();

        let op_shape = match op_move {
            'A' => Shape::Rock,
            'B' => Shape::Paper,
            'C' => Shape::Scissors,
            _ => panic!("Unknown move"),
        };
        let outcome = match outcome_code {
            'X' => Outcome::Lose,
            'Y' => Outcome::Draw,
            'Z' => Outcome::Win,
            _ => panic!("Unknown outcome"),
        };
        let my_shape = match outcome {
            Outcome::Lose => op_shape.wins(),
            Outcome::Draw => op_shape.draws(),
            Outcome::Win => op_shape.loses(),
        };
        score += my_shape.score() + outcome.score();
    }
    println!("{score}");
}
