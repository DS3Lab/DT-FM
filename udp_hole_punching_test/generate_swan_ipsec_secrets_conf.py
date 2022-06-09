ip_region_dict = {}
ip_private_dict = {}

ip_region_dict['34.210.166.14']='oregon'
ip_private_dict['34.210.166.14']='172.31.32.123'

ip_region_dict['34.239.149.103']='virginia'
ip_private_dict['34.239.149.103']='172.31.84.109'

ip_region_dict['52.14.154.37']='ohio'
ip_private_dict["52.14.154.37"]='172.31.18.48'

ip_region_dict['54.238.207.166']='tokyo'
ip_private_dict['54.238.207.166']='172.31.21.127'

ip_region_dict['3.38.106.7']='seoul'
ip_private_dict['3.38.106.7']='172.31.5.28'

ip_region_dict['13.212.11.226']='singapore'
ip_private_dict['13.212.11.226']='172.31.19.162'

ip_region_dict['54.206.163.141']='sydney'
ip_private_dict['54.206.163.141']='172.31.1.165'

ip_region_dict['18.134.207.251']='london'
ip_private_dict['18.134.207.251']='172.31.16.34'

ip_region_dict['18.194.249.150']='frankfurt'
ip_private_dict['18.194.249.150']='172.31.29.106'

ip_region_dict['54.170.34.28']='ireland'
ip_private_dict['54.170.34.28']='172.31.31.5'

shared_key = "\"NOU9h8KOiStPeTp1Uj9StrAjE/ScGzPuB77a98EK1/QcDh1q9EaxTzV/+wCQA/ptZl6R5AUnOgIM3asDGEMWng==\""

for public_ip in ip_private_dict.keys():
    with open("./swan/"+public_ip+"_ipsec.secrets", 'w') as secret_f:
        secret_f.write("# This file holds shared secrets or RSA private keys for authentication.\n")
        secret_f.write("# RSA private key for this host, authenticating it to any other host")
        secret_f.write("# which knows the public part.\n")
        for other_public_ip in ip_private_dict.keys():
            if other_public_ip != public_ip:
                secret_f.write(public_ip+" "+other_public_ip+" : PSK "+shared_key+"\n")

    with open("./swan/"+public_ip+"_ipsec.conf", 'w') as conf_f:
        conf_f.write("# basic configuration\n")
        conf_f.write("config setup\n")
        conf_f.write("\tcharondebug=\"all\"\n")
        conf_f.write("\tuniqueids=yes\n")
        conf_f.write("\tstrictcrlpolicy=no\n")

        conf_f.write("# connection to different region below:\n")
        for other_public_ip in ip_private_dict.keys():
            if other_public_ip != public_ip:
                conf_f.write("conn "+ip_region_dict[public_ip]+"-to-"+ip_region_dict[other_public_ip]+"\n")
                conf_f.write("\tauthby=secret\n")
                conf_f.write("\tleft=%defaultroute\n")
                conf_f.write("\tleftid="+public_ip+"\n")
                conf_f.write("\tleftsubnet=" + ip_private_dict[public_ip] + "/24\n")
                conf_f.write("\tright="+other_public_ip+"\n")
                conf_f.write("\trightsubnet=" + ip_private_dict[other_public_ip] + '/24\n')
                conf_f.write("\tike=aes256-sha1-modp1024,aes128-sha1-modp1024,3des-sha1-modp1024!\n")
                conf_f.write("\tesp=null\n")
                conf_f.write("\tkeyingtries=0\n")
                conf_f.write("\tikelifetime=1h\n")
                conf_f.write("\tlifetime=8h\n")
                conf_f.write("\tdpddelay=30\n")
                conf_f.write("\tdpdtimeout=120\n")
                conf_f.write("\tdpdaction=restart\n")
                conf_f.write("\tauto=start\n")
                conf_f.write("\treplay_window = -1\n")
                conf_f.write("\n")


