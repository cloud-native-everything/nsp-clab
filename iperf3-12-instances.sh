sudo kubectl config use-context kind-k8s02
sudo helm install my-iperf3-server iperf3-chart --set client.enabled=false -f ./12-instances-values.yml
sudo kubectl config use-context kind-k8s01
sudo helm install my-iperf3-client iperf3-chart --set server.enabled=false -f ./12-instances-values.yml
