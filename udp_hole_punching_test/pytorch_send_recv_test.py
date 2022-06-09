import random
import torch
import argparse
import time
import torch.distributed as dist
from nccl_backend import NCCLCommunicator


def test_sync_send_recv_delay(args, device, communicator):
    print("<==== Test delay ====>")
    if args.rank == 1:
        send_tensor = torch.ones(1, dtype=torch.float32, device=device)
        send_tensor += random.random()
        if args.dist_backend == 'nccl':
            dist.barrier(device_ids=[args.cuda_id])
            torch.cuda.synchronize()
        else:
            dist.barrier()
        if args.use_cuda:
            torch.cuda.synchronize()
        start_time = time.time()

        communicator.send(send_tensor, dst=0)

        if args.use_cuda:
            torch.cuda.synchronize()
        end_time = time.time()
        estimated_delay = (end_time - start_time)/2
        print('Send tensor is done: estimated delay:', estimated_delay * 1000, "ms.")
    elif args.rank == 0:
        recv_tensor = torch.zeros(1, dtype=torch.float32, device=device)
        if args.dist_backend == 'nccl':
            dist.barrier(device_ids=[args.cuda_id])
        else:
            dist.barrier()
        if args.use_cuda:
            torch.cuda.synchronize()
        start_time = time.time()

        communicator.recv(recv_tensor, src=1)

        if args.use_cuda:
            torch.cuda.synchronize()
        end_time = time.time()
        estimated_delay = (end_time - start_time)/2
        print('Recv tensor is done: estimated delay:', estimated_delay * 1000, "ms.")
        recv_tensor += random.random()
        if args.use_cuda:
            torch.cuda.synchronize()
    return estimated_delay


def test_sync_send_recv_bandwidth(args, device, communicator, estimated_delay=0):
    print("<==== Test bandwidth ====>")
    if args.rank == 1:
        send_tensor = torch.arange(args.dim, dtype=torch.float32, device=device)

        if args.dist_backend == 'nccl':
            dist.barrier(device_ids=[args.cuda_id])
        else:
            dist.barrier()
        if args.use_cuda:
            torch.cuda.synchronize()
        start_time = time.time()

        communicator.send(send_tensor, dst=0)

        if args.use_cuda:
            torch.cuda.synchronize()
        end_time = time.time()
        total_time = end_time - start_time
        estimated_bandwidth = 8 * 4 * args.dim / (total_time - estimated_delay) / 1024 / 1024 / 1024
        print('Send tensor is done: tensor size:<', args.dim, "> takes:", total_time, "second, estimated bandwidth:",
              estimated_bandwidth, "Gbps.")
    elif args.rank == 0:
        recv_tensor = torch.zeros(args.dim, dtype=torch.float32, device=device)
        if args.dist_backend == 'nccl':
            dist.barrier(device_ids=[args.cuda_id])
        else:
            dist.barrier()
        if args.use_cuda:
            torch.cuda.synchronize()
        start_time = time.time()

        communicator.recv(recv_tensor, src=1)

        if args.use_cuda:
            torch.cuda.synchronize()
        end_time = time.time()
        total_time = end_time - start_time
        estimated_bandwidth = 8 * 4 * args.dim / (total_time - estimated_delay) / 1024 / 1024 / 1024
        print('Recv tensor is done: tensor size:<', args.dim, "> takes:", total_time, "second, estimated bandwidth:",
              estimated_bandwidth, "Gbps.")
        print(recv_tensor[args.dim//2]==args.dim//2)
        print(recv_tensor[args.dim-1]==args.dim-1)

        recv_tensor += random.random()
        if args.use_cuda:
            torch.cuda.synchronize()
    return estimated_bandwidth, total_time


def main():
    parser = argparse.ArgumentParser(description='Test PyTorch Distributed')
    parser.add_argument('--dist-backend', type=str, default='cupy_nccl', metavar='S',
                        help='PyTorch backend type')
    parser.add_argument('--dist-url', type=str, default='tcp://127.0.0.1:9000', metavar='S',
                        help='master ip for distributed PyTorch')
    parser.add_argument('--world-size', type=int, default=2, metavar='D',
                        help='world size (default: 2)')
    parser.add_argument('--rank', type=int, default=0, metavar='R',
                        help='rank for distributed PyTorch')
    parser.add_argument('--dim', type=int, default=4*2048*2048, metavar='R',
                        help='size of the tensor to be sent.') # this is an approximated size of a macro-bench
    parser.add_argument('--use-cuda', default=True, type=lambda x: (str(x).lower() == 'true'),
                        help='if this is set to True, will use cuda to train')
    parser.add_argument('--cuda-id', type=int, default=0, metavar='N',
                        help='cuda index, if the instance has multiple GPUs.')
    parser.add_argument('--iter', type=int, default=20, metavar='R',
                        help='number of iterations for benchmark.')
    args = parser.parse_args()

    if args.iter <= 10:
        print("Too few iters, increase your iter number!")
        assert False

    if args.use_cuda:
        assert (torch.cuda.is_available())
        device = torch.device('cuda', args.cuda_id)
    else:
        device = torch.device('cpu')
    if args.dist_backend == 'cupy_nccl':
        communicator = NCCLCommunicator(rank=args.rank, intra_gpu_rank=args.cuda_id,
                                        world_size=args.world_size, master_ip=args.dist_url)
    else:
        dist.init_process_group(backend=args.dist_backend, init_method=args.dist_url,
                                rank=args.rank, world_size=args.world_size)
        communicator = dist

    estimated_delay = 0
    estimated_bandwidth = 0
    e2e_time = 0
    for i in range(args.iter):
        if i < 10:
            test_sync_send_recv_bandwidth(args, device, communicator, estimated_delay)
        else:
            current_bandwidth, current_time = test_sync_send_recv_bandwidth(args, device, communicator, estimated_delay)
            estimated_bandwidth += current_bandwidth
            e2e_time += current_time
        time.sleep(1)
    estimated_bandwidth /= (args.iter - 10)
    e2e_time /= (args.iter - 10)
    print("This is Rank-", args.rank, "see the result in Rank 0 node.")
    if args.rank == 0:
        print("This is the right result (recv side):")
    else:
        print("Record the result in the other side !!!!!!!!!")
    print("<=====Averaged estimated bandwidth: ", estimated_bandwidth, "Gbps=====>")
    print("<=====Averaged end to end time: ", e2e_time, "s for sending <", 4 * args.dim / 1024/1024,
          "> MB data=====>")


if __name__ == '__main__':
    main()
