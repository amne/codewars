use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/
fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let n = parse_input!(input_line, i32); // the number of temperatures to analyse
    let mut inputs = String::new();
    io::stdin().read_line(&mut inputs).unwrap();
    let mut temps = Vec::new(); 
    for i in inputs.split_whitespace() {
        let t = parse_input!(i, i32);
        temps.push(t);
    }

    if (n==0) {
        println!("0");
        return;
    }

    let mut smallest_temp = temps[0];

    // find temp in temps array closest to zero and put it in smallest_temp
    for i in 0..temps.len() {
        if temps[i] == 0 {
            smallest_temp = temps[i];
        } else if temps[i].abs() < smallest_temp.abs() {
            smallest_temp = temps[i];
        } else if temps[i].abs() == smallest_temp.abs() && temps[i] > smallest_temp {
            smallest_temp = temps[i];
        }
    }
    


    // Write an answer using println!("message...");
    // To debug: eprintln!("Debug message...");

    println!("{}", smallest_temp);
}

