source ./ip_list.sh

for ip in "${ips[@]}"
do
  echo "Issue command in $ip"
  ssh -i ../YOUR_PEM_FILE.pem ubuntu@"$ip" "bash -s" < ./tc_scripts/clear.sh &
done
wait