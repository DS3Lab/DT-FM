source ./ip_list.sh


world_size=64

script=$1
gpu_count_mode=$2

if [ $gpu_count_mode -eq 1 ]
then
  nodes_per_node=(8 8 8 8 8 8 8 8)
elif [ $gpu_count_mode -eq 1 ]
then
  nodes_per_node=(1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4 1 1 1 1 4)
else
  echo "Error! Not valid arguments."
  exit 1
fi

ga_step=$3
num_layers=$4
batch_size=$5

log_mode='optimal_map'

declare -i rank=0
for node_rank in "${!ips[@]}"
do
  echo "Issue command $script in Rank-${node_rank} node: ${ips[node_rank]}"
  if [ $# -eq 5 ]
  then
    echo "Running in default network."
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "$rank" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" &
      rank+=1
    done
  elif [ $# -eq 6 ]
  then
    case=$6
    echo "Running in heterogeneous network: Case-$case"
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "$rank" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" "$case" &
      rank+=1
    done
  elif [ $# -eq 7 ]
  then
    delay_ms=$6
    rate_gbit=$7
    echo "Running homogeneous TC setting."
    for (( i=0; i<${nodes_per_node[$node_rank]}; i++))
    do
      ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[node_rank]}" "bash -s" < ./local_scripts/"${script}" "$master_ip" "$world_size" "$rank" "$i" "$ga_step" "$num_layers" "$batch_size" "$log_mode" "$delay_ms" "$rate_gbit" &
      rank+=1
    done
  else
    echo "Error! Not valid arguments."
    exit 1
  fi
done
wait
