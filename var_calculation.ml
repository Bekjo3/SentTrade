open Core

let calculate_var returns confidence_level =
  let sorted_returns = List.sort ~compare:Float.compare returns in
  let index = Float.to_int (Float.of_int (List.length sorted_returns) *. (1.0 -. confidence_level)) in
  List.nth_exn sorted_returns index

let () =
  let args = Sys.get_argv () in
  if Array.length args <> 3 then
    Printf.printf "Usage: %s <returns_file.csv> <confidence_level>\n" args.(0)
  else
    let returns_file = args.(1) in
    let confidence_level = Float.of_string args.(2) in
    let returns = In_channel.read_lines returns_file
                  |> List.map ~f:Float.of_string in
    let var = calculate_var returns confidence_level in
    Printf.printf "Value at Risk (VaR) at %.2f confidence level: %.2f\n" confidence_level var
