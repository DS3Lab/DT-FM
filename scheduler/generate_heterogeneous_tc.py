import argparse
from generate_sim_com_matrices import *

# No space for IPs!!!!
private_ip = [
    "172.31.29.36",
    "172.31.20.200",
    "172.31.25.144",
    "172.31.42.240",
    "172.31.44.241",
    "172.31.38.238",
    "172.31.39.239",
    "172.31.46.234",
    "172.31.37.237",
    "172.31.44.229",
    "172.31.32.231",
    "172.31.41.101",
    "172.31.39.87",
    "172.31.39.219",
    "172.31.46.213",
    "172.31.36.86",
    "172.31.32.80",
    "172.31.33.84",
    "172.31.40.200",
    "172.31.32.75",
    "172.31.46.195",
    "172.31.46.68",
    "172.31.37.253",
    "172.31.37.64",
    "172.31.45.116",
    "172.31.34.247",
    "172.31.43.241",
    "172.31.46.243",
    "172.31.32.167",
    "172.31.38.169",
    "172.31.34.38",
    "172.31.37.38",
    "172.31.41.164",
    "172.31.35.165",
    "172.31.46.35",
    "172.31.43.164",
    "172.31.42.163",
    "172.31.32.163",
    "172.31.43.161",
    "172.31.35.163",
    "172.31.47.94",
    "172.31.43.33",
    "172.31.40.91",
    "172.31.32.220",
    "172.31.42.12",
    "172.31.43.141",
    "172.31.34.137",
    "172.31.34.138",
    "172.31.37.183",
    "172.31.34.1",
    "172.31.38.181",
    "172.31.39.54",
    "172.31.37.51",
    "172.31.40.52",
    "172.31.37.49",
    "172.31.36.179",
    "172.31.44.175",
    "172.31.38.176",
    "172.31.36.42",
    "172.31.36.45",
    "172.31.35.26",
    "172.31.45.157",
    "172.31.45.142",
    "172.31.37.16"
]


def get_delay_bandwidth(args):
    if args.case == '1':
        return simulate_1_datacenter(args.nodes)
    elif args.case == '2':
        return simulate_2_datacenter_spot_gpu(args.nodes)
    elif args.case == '3':
        return simulate_3_multi_universities(args.nodes)
    elif args.case == '4':
        return simulate_4_regional_geo_distributed(args.nodes)
    elif args.case == '5':
        return simulate_5_worldwide_geo_distributed(args.nodes)
    else:
        assert False


def generate_tc_scripts(args):
    assert args.nodes == len(private_ip)
    delay, bandwidth, _ = get_delay_bandwidth(args)
    with open("../scripts/tc_scripts/heterogeneous_setup_case"+str(args.case)+".sh", 'w') as script:
        tc_setting_dict = {}
        handle_i = 1
        for i in range(len(private_ip)):
            if i != args.rank:
                current_key = (delay[args.rank][i], bandwidth[args.rank][i])
                if current_key not in tc_setting_dict:
                    tc_setting_dict[current_key] = handle_i
                    handle_i += 1
        assert len(tc_setting_dict) <= 16
        # setup delay and bandwidth subclass qdisc
        script.write("sudo tc qdisc add dev ens3 root handle 1: prio bands {}\n"
                     .format(max(3, len(tc_setting_dict))))
        for key in tc_setting_dict.keys():
            current_delay, current_bandwidth = key
            handle_index = tc_setting_dict[key]
            limit_pkts = current_delay * 22500 * current_bandwidth
            script.write("sudo tc qdisc add dev ens3 parent 1:{} handle {}: netem delay {}ms rate {}Gbit limit {}\n"
                         .format(handle_index, handle_index*10, current_delay, current_bandwidth, limit_pkts))
        # setup filter
        for i in range(len(private_ip)):
            if i != args.rank:
                current_key = (delay[args.rank][i], bandwidth[args.rank][i])
                script.write("sudo tc filter add dev ens3 parent 1:0 protocol ip prio 1 u32 match ip dst {}/32 flowid 1:{}\n"
                             .format(private_ip[i], tc_setting_dict[current_key]))


def main():
    parser = argparse.ArgumentParser(description='Test PyTorch Distributed')
    parser.add_argument('--case', type=str, default='4', metavar='R',
                        help='which case to generate.')
    parser.add_argument('--rank', type=int, default=0, metavar='R',
                        help='rank for this IP')
    parser.add_argument('--nodes', type=int, default=64, metavar='R',
                        help='Total number of nodes')
    args = parser.parse_args()
    generate_tc_scripts(args)


if __name__ == '__main__':
    main()
