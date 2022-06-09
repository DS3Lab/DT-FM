source ./ip_list.sh

scp -i ../YOUR_PEM_FILE.pem ubuntu@"${ips[0]}":"/YOUR_PATH/logs/*_rank0*" ../logs