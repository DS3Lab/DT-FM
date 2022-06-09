source ./ip_list.sh

case=$1

for ip in "${ips[@]}"
do
  echo "Issue command in $ip"
  ssh -i ../YOUR_PEM_FILE.pem ubuntu@"$ip" "bash -s" < ./local_scripts/local_start_heter_tc.sh "$case" &
done
wait