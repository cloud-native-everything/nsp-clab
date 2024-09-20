# NSP Containerlab Settings

The Nokia NSP (Network Services Platform) is an advanced software solution providing intent-based network optimization and automation across multi-vendor environments. It ensures efficient resource utilization, reduces operational complexity, and enhances network performance through intelligent, automated decision-making and actions.

Containerlab is a lightweight tool designed for creating, managing, and operating network labs using containerized network devices. It supports multi-vendor environments, offering a flexible and efficient platform for network development, testing, and validation activities.

Utilizing Nokia NSP’s intent-based capabilities alongside Containerlab, one can establish a robust test automation environment, accommodating multi-vendor network devices. This setup enables seamless orchestration, real-time optimization, and automated validation, ensuring network configurations meet desired intents. It significantly reduces manual effort, accelerates development cycles, and enhances the reliability and performance of network services across various vendor equipment, streamlining operations and maintenance.


## Considerations

* We assume you have a fresh install of NSP with reachibility to the clab and with the adaptors already loaded.

### Loading adaptors

Files must be downloaded from customer support site and loaded to NSP from the deployer as it's shown in the next example (you must download the version you have for SROS, the same for SRL or others)

```
cp sros-common-23_8_v3.zip /tmp/.
cp sros-23-3-r1-23_8_v2.zip /tmp/.
cp *telemetry*sros-23_8_v2.zip /tmp/.
cd /tmp
unzip nsp-mdm-telemetry-sros-23_8_v2.zip
unzip nsp-telemetry-yang-sros-23_8_v2.zip 
cd /opt/nsp/NSP-CN-DEP-23.8.0-rel.2823/NSP-CN-23.8.0-rel.2707/tools/mdm/bin/
./yang-files.bash --add /tmp/sros/*
./json-files.bash --add /tmp/*.json
./adaptor-suite.bash --install /tmp/sros-common-23_8_v3.zip /tmp/sros-23-3-r1-23_8_v2.zip
```

## Settings things up

Before start your topology, do not forget to start the linux bridges for clab (details should be in the topo file)
```
sudo ip link add R11-R12 type bridge 
sudo ip link set R11-R12 up
```

## Install Dockers (Rocky Linux release 9.2)

Dockers is a little tricky in RedHat systems, I fix mine with this.
```
sudo yum remove docker  docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engin podman runc
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl start docker
sudo systemctl status docker
sudo systemctl enable docker
```
## Node images

You can create your own SROS image using using https://github.com/hellt/vrnetlab repo. You will need to download the QCOW2 file and have a license. Remember ti install make:

```
sudo dnf -y install make
```
Most of the new linux system would require ip_tables for SROS
Activate iptables (Rocky Linux release 9.2) like this, before to start the lab
```
sudo modprobe ip_tables
sudo modprobe ip6_tables
```

Now it's time to play

## iperf3 Helm Chart

This Helm chart deploys `iperf3` server and client instances to Kubernetes clusters. It provides a flexible setup for deploying multiple server instances across different NodePorts and corresponding clients that connect to those server instances.

### Prerequisites

- Kubernetes cluster
- Helm 3.x
- Local Docker images for `iperf3-client` and `iperf3-server` available in the cluster nodes

### Installation

#### 1. Deploying `iperf3` Servers

To deploy the `iperf3` servers, run the following command:

```bash
sudo kubectl config use-context kind-k8s01
sudo helm install my-iperf3-client iperf3-chart --set server.enabled=false -f values.yaml
```

#### 2. Deploying `iperf3` Clients

To deploy the `iperf3` clients, run the following command:

```bash
sudo kubectl config use-context kind-k8s02
sudo helm install my-iperf3-server iperf3-chart --set client.enabled=false -f values.yaml
```

Replace `<node-ip>` with the actual IP address of the node where the `iperf3` servers are running.

#### 3. Uninstalling the Helm Release

To uninstall the `iperf3` Helm release:

```bash
helm uninstall my-iperf3-server
```

### Configuration

The chart can be customized using the following parameters in the `values.yaml` file:

- **image.serverRepository**: Docker image for the `iperf3` server.
- **image.clientRepository**: Docker image for the `iperf3` client.
- **image.tag**: Tag for both the server and client Docker images.
- **server.enabled**: Enable or disable the deployment of server instances.
- **client.enabled**: Enable or disable the deployment of client instances.
- **server.instances**: List of server instances, each with a unique name and NodePort.
- **client.serverIPs**: List of server IPs where each client instance will connect.
- **client.serverPorts**: List of NodePorts corresponding to each server instance.

#### Example `values.yaml`:

```yaml
image:
  clientRepository: iperf3-client
  serverRepository: iperf3-server
  tag: 0.1a
  pullPolicy: IfNotPresent

server:
  enabled: true
  instances:
    - name: iperf3-server-1
      port: 30001
    - name: iperf3-server-2
      port: 30002
    - name: iperf3-server-3
      port: 30003
    - name: iperf3-server-4
      port: 30004
  containerPort: 5201

client:
  enabled: true
  replicas: 4
  flows: 4
  duration: 0
  serverIPs:
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
  serverPorts:
    - 30001
    - 30002
    - 30003
    - 30004
```

To apply changes to the Helm chart configuration, update the `values.yaml` file as needed, and then redeploy the Helm release using the `helm upgrade` command:

```bash
sudo kubectl config use-context kind-k8s02
sudo helm upgrade my-iperf3-server iperf3-chart --set client.enabled=false -f values.yaml
sudo kubectl config use-context kind-k8s01
sudo helm upgrade my-iperf3-client iperf3-chart --set server.enabled=false -f values.yaml
```

### Custom Configuration Example: Deploying 12 Instances

To deploy 12 `iperf3` server instances with corresponding clients, you can use a custom values file like the following:

```yaml
image:
  clientRepository: iperf3-client
  serverRepository: iperf3-server
  tag: 0.1a
  pullPolicy: IfNotPresent

server:
  enabled: true
  instances:
    - name: iperf3-server-1
      port: 30001
    - name: iperf3-server-2
      port: 30002
    - name: iperf3-server-3
      port: 30003
    - name: iperf3-server-4
      port: 30004
    - name: iperf3-server-5
      port: 30005
    - name: iperf3-server-6
      port: 30006
    - name: iperf3-server-7
      port: 30007
    - name: iperf3-server-8
      port: 30008
    - name: iperf3-server-9
      port: 30009
    - name: iperf3-server-10
      port: 30010
    - name: iperf3-server-11
      port: 30011
    - name: iperf3-server-12
      port: 30012
  containerPort: 5201

client:
  enabled: true
  replicas: 12
  flows: 4
  duration: 0  # 0 means run indefinitely
  serverIPs:
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
    - 172.254.102.101
  serverPorts:
    - 30001
    - 30002
    - 30003
    - 30004
    - 30005
    - 30006
    - 30007
    - 30008
    - 30009
    - 30010
    - 30011
    - 30012
```

To use this configuration, save it as `custom-values.yaml` and deploy the Helm chart with:

```bash
sudo kubectl config use-context kind-k8s02
sudo helm install my-iperf3-server iperf3-chart --set client.enabled=false -f custom-values.yaml
sudo kubectl config use-context kind-k8s01
sudo helm install my-iperf3-client iperf3-chart --set server.enabled=false -f custom-values.yaml
```

This will deploy 12 `iperf3` server instances and 12 `iperf3` client instances, each connecting to a unique server.
