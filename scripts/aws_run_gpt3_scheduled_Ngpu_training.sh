source ./ip_list.sh


world_size=64

script=$1
gpu_count_mode=$2

if [ $gpu_count_mode -eq 1 ]
then
  nodes_per_node=(8 8 8 8 8 8 8 8)
elif [ $gpu_count_mode -eq 2 ]
then
  nodes_per_node=(1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4)
else
  echo "Error! Not valid arguments."
  exit 1
fi

# Random seed 2022
# rank_map=(0 2 32 33 4 10 7 45 36 8 51 26 11 5 53 1 40 23 37 14 13 43 54 21 57 35 63 18 6 24 16 22 38 3 58 61 44 27 52 30 15 9 39 47 48 41 31 20 12 28 34 42 17 55 19 25 56 60 59 50 49 46 29 62)
# Random seed 2023
rank_map=(0 42 36 19 15 13 55 11 1 10 43 45 39 12 63 5 37 59 35 31 20 27 17 28 41 3 62 21 47 32 22 51 46 2 9 44 16 61 30 52 8 50 58 57 25 6 40 14 49 48 18 54 33 38 23 60 53 4 29 34 56 7 26 24)
# Random seed 2024
# rank_map=(0 35 24 52 16 49 41 4 18 7 45 13 22 60 14 15 51 25 17 8 47 55 19 63 21 57 44 26 5 58 20 50 30 6 54 43 23 34 46 27 39 10 40 62 29 12 32 53 48 31 38 61 3 11 36 2 42 56 37 28 1 33 59 9)

ga_step=$3
num_layers=$4
batch_size=$5

log_mode=$6

declare -i rank_index=0

for node_rank in "${!ips[@]}"
do
  echo "Issue command $script in Rank-${node_rank} node: ${ips[node_rank]}"
  if [ $# -eq 6 ]
  then
    echo "Running in default network."
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      # echo ${rank_map[rank_index]}
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "${rank_map[rank_index]}" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" &
      rank_index+=1
    done
  elif [ $# -eq 7 ]
  then
    case=$7
    echo "Running in heterogeneous network: Case-$case"
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "${rank_map[rank_index]}" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" "$case" &
      rank_index+=1
    done
  elif [ $# -eq 8 ]
  then
    delay_ms=$7
    rate_gbit=$8
    echo "Running homogeneous TC setting."
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "${rank_map[rank_index]}" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" "$delay_ms" "$rate_gbit" &
      rank_index+=1
    done
  else
    echo "Error! Not valid arguments."
    exit 1
  fi
done
wait