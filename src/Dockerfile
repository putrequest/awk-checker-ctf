############################
# STEP 1 build & run interactively
############################
FROM ubuntu:18.04

# Install dependencies
RUN apt-get update && \
	apt-get -y install sudo python3 python3-dev python3-pip

# Create user
RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo
USER docker

# Set working directory
WORKDIR /home/docker

# Install pip requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the project files
COPY . .
