source ./ip_dict.sh

for ip in "${!ip_region_dict[@]}"; do
  region=${ip_region_dict[$ip]}
  echo "IP $ip in region $region"
  scp -i ../pems/YOUR_PEM_FILE_"$region".pem  ../swan/sysctl.conf ubuntu@"$ip":~/swan_conf/sysctl.conf
  scp -i ../pems/YOUR_PEM_FILE_"$region".pem  ../swan/"$ip"_ipsec.conf ubuntu@"$ip":~/swan_conf/ipsec.conf
  scp -i ../pems/YOUR_PEM_FILE_"$region".pem  ../swan/"$ip"_ipsec.secrets ubuntu@"$ip":~/swan_conf/ipsec.secrets &
done