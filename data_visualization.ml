open Core

(* Save data to a CSV file *)
let save_data_to_csv data output_file =
  Out_channel.with_file output_file ~f:(fun oc ->
    List.iter data ~f:(fun (x, y) ->
      Printf.fprintf oc "%f,%f\n" x y
    )
  )

let () =
  let args = Sys.get_argv () in
  if Array.length args <> 2 then
    Printf.printf "Usage: %s <data_file.csv>\n" args.(0)
  else
    let data_file = args.(1) in
    let data = In_channel.read_lines data_file
               |> List.mapi ~f:(fun i line -> (Float.of_int i, Float.of_string line)) in
    save_data_to_csv data "visualized_data.csv";
    Printf.printf "Data saved to visualized_data.csv\n"
