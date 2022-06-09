source ./ip_list.sh

case=$1
world_size=${#ips[@]}

if [ $# -eq 1 ]
then
  for rank in "${!ips[@]}"
  do
    echo "Issue command in ${ips[rank]}"
    ssh -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[rank]}" "bash -s" < ./local_scripts/local_generate_heter_tc.sh $case $rank $world_size&
  done
else
  echo "Error! Not valid arguments. (Please specify which simulation case!)"
fi
wait
