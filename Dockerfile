# Use the official Ubuntu base image
FROM ubuntu:latest

# Set the maintainer label
LABEL maintainer="your-email@example.com"

# Update package list and install the required network tools
RUN apt-get update && apt-get install -y \
    traceroute \
    iperf3 \
    iputils-ping \
    curl \
    wget \
    net-tools \
    dnsutils \
    tcpdump \
    nmap \
    mtr \
    iproute2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the default command to bash
CMD ["bash"]

