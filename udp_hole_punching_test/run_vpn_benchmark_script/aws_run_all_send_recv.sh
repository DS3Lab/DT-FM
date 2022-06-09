source ./ip_dict.sh

# rank0_ip='13.211.228.136'
for rank0_ip in "${!ip_wg_private_dict[@]}"; do
  for rank1_ip in "${!ip_wg_private_dict[@]}"; do
    if [ "$rank0_ip" !=  "$rank1_ip" ]
    then
        echo "${ip_region_dict[$rank0_ip]} recv, ${ip_region_dict[$rank1_ip]} send."
        ssh -i ../pems/YOUR_PEM_FILE_"${ip_region_dict[$rank0_ip]}".pem ubuntu@"$rank0_ip" "bash -s" < ./aws_instance_run_recv.sh \
        "${ip_wg_private_dict[$rank0_ip]}" "${ip_region_dict[$rank0_ip]}_r_${ip_region_dict[$rank1_ip]}_s" &
        ssh -i ../pems/YOUR_PEM_FILE_"${ip_region_dict[$rank1_ip]}".pem ubuntu@"$rank1_ip" "bash -s" < ./aws_instance_run_send.sh \
        "${ip_wg_private_dict[$rank0_ip]}" &
        wait
    fi
  done
done