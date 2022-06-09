import numpy as np
seed = 2022  # 2023, 2024


def random_assignment(nodes=64):
    arr = np.arange(1, nodes)
    np.random.shuffle(arr)
    result = arr.tolist()
    result.insert(0, 0)
    print('rank_map=(', end='')
    for i in range(len(result)):
        val = result[i]
        print(val, end='' if i == nodes - 1 else ' ')
    print(')')


def random_assignment_1(nodes=64):
    print("Generate random_assignment")
    np.random.seed(seed)
    gpu_per_instances = min(nodes // 2, 8)
    instances = nodes // gpu_per_instances
    print('nodes_per_node=(', end='')
    for i in range(instances):
        print(gpu_per_instances, end='' if i==instances-1 else ' ')
    print(')')
    random_assignment(nodes)


def random_assignment_2(gpu_per_instances=4, multi_gpu_instances=8, single_gpu_instances=32):
    print("Generate random_assignment_1_datacenter_spot")
    np.random.seed(seed)
    gpus = []
    for i in range(multi_gpu_instances):
        for j in range(single_gpu_instances // multi_gpu_instances):
            gpus.append(1)
        gpus.append(gpu_per_instances)
    print('nodes_per_node=(', end='')
    instances = multi_gpu_instances + single_gpu_instances
    for i in range(instances):
        print(gpus[i], end='' if i == instances - 1 else ' ')
    print(')')
    world_size = gpu_per_instances*multi_gpu_instances+single_gpu_instances
    random_assignment(world_size)


def optimal_assignment_2(gpu_per_instances=4, multi_gpu_instances=8, single_gpu_instances=32):
    print("Generate optimal_assignment_1_datacenter_spot")
    gpus = []
    for i in range(multi_gpu_instances):
        for j in range(single_gpu_instances//multi_gpu_instances):
            gpus.append(1)
        gpus.append(gpu_per_instances)
    print('nodes_per_node=(', end='')
    instances = multi_gpu_instances+single_gpu_instances
    for i in range(instances):
        print(gpus[i], end='' if i==instances-1 else ' ')
    print(')')
    world_size = gpu_per_instances*multi_gpu_instances+single_gpu_instances
    arr = np.arange(world_size)
    result = arr.tolist()
    print('rank_map=(', end='')
    for i in range(len(result)):
        val = result[i]
        print(val, end='' if i==world_size-1 else ' ')
    print(')')


def random_assignment_345(nodes):
    print("Generate random_assignment_345")
    random_assignment(nodes)


def optimal_assignment_1345(nodes):
    # no need to
    print("Generate optimal_assignment_1345")
    print("No special alignment.")


def main():
    print("------------------------------------")
    random_assignment_1()


if __name__ == '__main__':
    main()
