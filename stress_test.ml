open Core

(* Load historical data from a CSV file *)
let load_data filename =
  In_channel.read_lines filename
  |> List.tl_exn (* Skip header *)
  |> List.map ~f:(fun line -> 
      match String.split ~on:',' line with
      | [date; close] -> (date, Float.of_string close)
      | _ -> failwith "Invalid data format"
    )

(* Calculate returns *)
let calculate_returns data =
  let rec aux prev = function
    | [] -> []
    | (_, close) :: tail -> (close -. prev) /. prev :: aux close tail
  in
  match data with
  | [] | [_] -> []
  | (_, first_close) :: tail -> aux first_close tail

(* Perform stress test *)
let stress_test data =
  let returns = calculate_returns data in
  let mean = List.fold ~init:0.0 ~f:(+.) returns /. Float.of_int (List.length returns) in
  let stddev = 
    returns 
    |> List.map ~f:(fun r -> (r -. mean) ** 2.0) 
    |> List.fold ~init:0.0 ~f:(+.) 
    |> (fun sum -> sum /. Float.of_int (List.length returns)) 
    |> sqrt
  in
  let sharpe_ratio = mean /. stddev in
  let max_drawdown =
    let rec aux max_so_far min_so_far = function
      | [] -> max_so_far -. min_so_far
      | x :: xs -> 
        let max_so_far = Float.max max_so_far x in
        let min_so_far = Float.min min_so_far x in
        aux max_so_far min_so_far xs
    in
    aux Float.neg_infinity Float.infinity returns
  in
  (sharpe_ratio, max_drawdown)

let () =
  let data = load_data "historical_data.csv" in
  let (sharpe_ratio, max_drawdown) = stress_test data in
  printf "Sharpe Ratio: %f\nMax Drawdown: %f\n" sharpe_ratio max_drawdown
