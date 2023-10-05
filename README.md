# NSP Containerlab Settings


##Considerations

* You have a fresh install of NSP with reachibility to the clab and with the adaptors already loaded

##Settings things up

Creating the Bridges
```
sudo nmcli con add type vlan ifname eno5-vlan16 dev eno5 id 16
sudo nmcli con add type vlan ifname eno5-vlan17 dev eno5 id 17
sudo nmcli connection add type bridge con-name br-vlan16 ifname br-vlan16
sudo nmcli connection add type bridge con-name br-vlan17 ifname br-vlan17
sudo nmcli connection modify vlan-eno5-vlan16 master br-vlan16
sudo nmcli connection modify vlan-eno5-vlan17 master br-vlan17
sudo nmcli con mod br-vlan16 ipv4.method manual ipv4.addresses 10.2.16.224/24
sudo nmcli con mod br-vlan17 ipv4.method manual ipv4.addresses 10.2.17.224/24
```

Create bridges for clab
```
sudo ip link add R11-R12 type bridge 
sudo ip link set R11-R12 up
```

Install Dockers (Rocky Linux release 9.2)
```
sudo yum remove docker  docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engin podman runc
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl status docker
sudo systemctl enable docker
```

Install make to create SROS images using https://github.com/hellt/vrnetlab repo
```
sudo dnf -y install make
```

Activate iptables (Rocky Linux release 9.2)
```
sudo modprobe ip_tables
sudo modprobe ip6_tables
```

## Upload SROS and SRL Adaptors
Download adaptors from the support site

### For NE discovery

You need to have the adaptor for the specific release of the NE and the common
```
cd NSP-CN-23.8.0-rel.2707/tools/mdm/
./adaptor-suite.bash --install /tmp/sros-common-23_8_v3.zip /tmp/sros-23-3-r1-23_8_v2.zip /tmp/srl-common-23_8_v2.zip /tmp/srl-23-7-1-23_8.zip
```

### Create routes in K801 for 172.18.1.0/24

```
ip add route 172.18.1.0/24 via 10.2.16.224
```