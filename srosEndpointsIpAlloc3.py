import yaml
from ipaddress import ip_network

# Extract /30 subnets from a given prefix
def allocate_p2p_subnets(prefix):
    main_net = ip_network(prefix, strict=False)
    
    # Check if it's a valid prefix for allocation
    if main_net.prefixlen > 30:
        raise ValueError("Prefix too small for /30 allocation.")
    
    # Generate a list of /30 subnets
    subnets = list(main_net.subnets(new_prefix=30))
    return subnets

# Given a YAML file, allocate /30 prefixes for each endpoint pair
def allocate_endpoints(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    # Extract all endpoint pairs
    endpoints = [link['endpoints'] for link in data['topology']['links'] if 'endpoints' in link]

    # Get /30 subnets from a given prefix
    subnet_pool = allocate_p2p_subnets('192.168.1.0/24')

    # Allocate subnets for each endpoint pair
    allocations = {}
    for endpoint_pair in endpoints:
        if subnet_pool:
            subnet = subnet_pool.pop(0)
            min_host, max_host = get_min_max_host(subnet)

            # Define the "to" endpoint for each
            to_endpoint1 = "to_" + endpoint_pair[0].split(":")[0]
            to_endpoint2 = "to_" + endpoint_pair[1].split(":")[0]

            # Store allocations in desired format
            allocations[endpoint_pair[0]] = (to_endpoint2, str(min_host) + '/30')
            allocations[endpoint_pair[1]] = (to_endpoint1, str(max_host) + '/30')
        else:
            print("Ran out of /30 subnets!")
            break
    
    return allocations

def get_min_max_host(subnet):
    hosts = list(subnet.hosts())
    return hosts[0], hosts[-1]    

# Read and process the YAML file
yaml_file = 'topo-SR.yml'
allocations = allocate_endpoints(yaml_file)
for endpoint, (to, ip) in allocations.items():
    print(f"'{endpoint}' -> '{to}', '{ip}'")
