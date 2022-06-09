# Decentralized Training of Foundation Models

We explore how to deploy the training of foundation models over a heterogeneous decentralized environment. 
This is a research project developed by [DS3Lab@ETH Zurich](https://ds3lab.inf.ethz.ch/) and [CRFM@Stanford](https://crfm.stanford.edu/).

## Overview 

- [Udp_hole_punching_test](./udp_hole_punching_test) directory includes our sample script for doing udp hole punching test, detail instruction about running hole punching test is provided.

- The other modules are self-document to support the distributed training within the scope of pipeline parallelism and data parallelism.


## Cite Our Paper

```bibtex
@article{yuan2022decentralized,
  title={Decentralized Training of Foundation Models in Heterogeneous Environments}, 
  author={Binhang Yuan, Yongjun He, Jared Quincy Davis, Tianyi Zhang, Tri Dao, Beidi Chen, Percy Liang, Christopher Re, and Ce Zhang},
  year={2022},
  eprint={2206.01288},
  archivePrefix={arXiv},
  primaryClass={cs.DC}
}
```

## AWS AMI

You can directly use our AWS AMI for easy configuration: 

| AMI Name | AMI ID                | Region    | Recommended Instances                |
|----------|-----------------------|-----------|--------------------------------------|
| DT-FM    | ami-0652205be6faa6e2d | us-west-2 | p3.2xlarge, p3.8xlarge, p3.16xlarge  |

## Run our system:
### Setup:

- If you use our AMI, you can ignore this section.


- Use AWS Deep Learning Base AMI


- Install PyTorch env: 

      pip3 install torch==1.9.0+cu111 torchtext -f https://download.pytorch.org/whl/torch_stable.html
      pip3 install cupy-cuda110==8.6.0


- Download glue-qqp dataset for throughput benchmark.


- Setup network configuration:

      export GLOO_SOCKET_IFNAME=ens3
      export NCCL_SOCKET_IFNAME=ens3

### Manually run cmd on each instance (not recommended)

- Use TC scripts to control network delay and bandwidth.
  

- From each terminal, run cmd:
      
      python dist_runner.py --dist-url tcp://XXX.XXX.XXX.XXX:9000 --world-size N --rank i (i=0,...,N-1)

### Run with Advanced Scripts (recommended)

- Go to the [scripts](./scripts) directory


- First update the public IPs and private IP of the rank-0 node in [ip_list.sh](./scripts/ip_list.sh).


- Allow SSH connects, on your local machine run: 

      bash accept_ssh_keys.sh

      
- Enable environment: (This is optional but load conda env seems to be slow for the first time)

      bash aws_foo_load_lib.sh

- Setup heterogeneous network:

  - Update the private IPs in [generate_heterogeneous_tc.py](./scheduler/generate_heterogeneous_tc.py);

  - Sync the code to AWS, make sure this python script is updated with the IPs in all nodes. 
  
  - Run:

          bash aws_generate_heter_tc.sh #HETER_CASE (3/4/5)

- Run Schedulers experiments (optional):

  - Go to [scheduler/heuristic_evolutionary_solver directory](./scheduler/heuristic_evolutionary_solver)
  
  - To get assignments and estimated cost, run Schedulers 
  
         python scheduler.py


- Run Tasks (e.g.,):

      bash aws_run_batch_gpt3_optimal.sh 3/4/5
      bash aws_run_batch_gpt3_random.sh 3/4/5
