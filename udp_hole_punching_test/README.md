# UDP Hole Punching for NCCL

This directory gives an example about how to use Swan VPN to conduct UDP hole punching to enable NCCL communication among two AWS instances cross different regions. 
In principle, this suggests we can use NCCL among any two GPU machine across machines across the world. 

## Setup:

- Setup AWS instances:
  - If you use our AWS AMI, no further setup, just activate the environment:

        source activate pytorch_p38
  
  - If you use AWS deep learning base AMI, you need to :

        pip3 install torch==1.9.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
        pip3 install cupy-cuda110==8.6.0

- Set up swan ipsec VPN
  - Install strongswan if necessary:
      
        sudo apt install strongswan
  
  - Update IP addresses in [generate_swan_ipsec_secrets_conf.py](./generate_swan_ipsec_secrets_conf.py);
  
  - Update IP addresses in [ip_dict.sh](./run_vpn_benchmark_script/ip_dict.sh);
  
  - Sync secret/conf file, run:
        
        python generate_swan_ipsec_secrets_conf.py
        bash swan_upload_conf.sh
  
  - Start vpn: in root mode of each instance, run:
        
         bash swan_start_vpn.sh
    or use our scripts, run:
  
         bash aws_cluster_run_cmd.sh swan_start_vpn.sh

- Set network interface (please use ifconfig to make sure your network interface is named ens3):

      export NCCL_SOCKET_IFNAME=ens3
      export GLOO_SOCKET_IFNAME=ens3


- (Optimal) tune NCCL FLAGs:

      export NCCL_SOCKET_NTHREADS=1
      export NCCL_NSOCKS_PERTHREAD=8/16
      export NCCL_DEBUG=INFO


## Benchmark:

- On each node, run:

      python pytorch_send_recv_test.py --iter 5 --dist-url tcp://XX.XX.XX.XX:9000 --world-size 2 --dist-backend cupy_nccl --use-cuda True --rank 0/1

- Or use our [scripts](./run_vpn_benchmark_script).

