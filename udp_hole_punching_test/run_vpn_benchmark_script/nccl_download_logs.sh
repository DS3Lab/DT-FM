source ./ip_dict.sh

#ip='13.211.228.136'
for ip in "${!ip_region_dict[@]}"; do
  region=${ip_region_dict[$ip]}
  echo "IP $ip in region $region"
  scp -i ../pems/YOUR_PEM_FILE_"$region".pem ubuntu@"$ip":~/nccl_run_logs/*.log  ../nccl_run_logs/ &
done

wait