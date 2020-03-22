// command line arguments: 
//NAME: orth_to_surprisals
// SUMMARY: script for running python functions successively 
// args[0] - this file
// args[1] - python compiler, e.g. "~\\Python\\Python38-32\\python.exe"
// args[2] - folder which contains kroot.csv e.g. "~\\Chapters\\Minimal_Root\\tables"
// args[3] - folder which contains py scripts kComp, kEntropy, 
//              kSurprisal lex_io, orth_to_ipa.py, produce_segmental_configurations_list.py.
//           e.g. "~\\src\\py"
use std::env;
use std::process;

fn main() {
   let args: Vec<String> = env::args().collect();
   // confirm that there are two command line argument
    if args.len() != 4 {
        panic!("Wrong number of command line arguments!")
    }
    //set relevant strings

    let orth_to_ipa_dir = args[3].to_string() + "\\orth_to_ipa.py";
    let kcomp_dir = args[3].to_string() + "\\kComp.py";
    let seg_config_dir = args[3].to_string() + "\\produce_segmental_configurations_list.py";

    //orth to ipa procedure
    let kroot_path = args[2].to_string() + "\\kroot.csv";
    let rule_path = args[2].to_string() + "\\rules.csv";

    let mut cmd_status = process::Command::new(&args[1])
    .args(&[&orth_to_ipa_dir, &kroot_path, &rule_path])
    .status()
    .expect("Python script could not be executed.");
    if !cmd_status.success() {
        println!("{:?}", cmd_status.code());
        panic!("Python script did not exit with 0 status.")
    }
    // produce segmental configurations procedure
    let syl_dir = args[2].to_string() + "\\phon_syls.txt";
    cmd_status = process::Command::new(&args[1])
    .args(&[&seg_config_dir, &syl_dir])
    .status()
    .expect("Python script could not be executed");
    if !cmd_status.success() {
        println!("{:?}", cmd_status.code());
        panic!("Python script did not exit with 0 status")
    }
    // finally, produce information theory docs. it takes phon_syls and phon_configs.txt as arguments
    let configs_dir = args[2].to_string() + "\\phon_configs.txt";
    cmd_status = process::Command::new(&args[1])
    .args(&[&kcomp_dir, &syl_dir, &configs_dir])
    .status()
    .expect("Python script could not be executed");
    if !cmd_status.success() {
        println!("{:?}", cmd_status.code());
        panic!("Python script did not exit with 0 status")
    }
    println!("Doucments were produced successfully at {}", args[2]);
}