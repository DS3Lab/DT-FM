RATE_GBIT=$1
LIMIT_PKTS=$(echo "$RATE_GBIT * 1500 * 10 * 1.5" | bc -q)
echo "TC set up bandwidth to $1 Gbit."
sudo tc qdisc add dev ens3 root netem rate ${RATE_GBIT}Gbit limit ${LIMIT_PKTS}