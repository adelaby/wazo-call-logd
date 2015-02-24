Dockerfile for XiVO call-logd

## Install Docker

To install docker on Linux :

    curl -sL https://get.docker.io/ | sh
 
 or
 
     wget -qO- https://get.docker.io/ | sh

## Build

To build the image, simply invoke

    docker build -t xivo-call-logd github.com/xivo-pbx/xivo-call-logs

Or directly in the sources in contribs/docker

    docker build -t xivo-call-logd .
  
## Usage

To run the container, do the following:

    docker run -d -v /conf/call-logd:/etc/xivo-call-logs/conf.d xivo-call-logd

On interactive mode :

    docker run -v /conf/call-logd:/etc/xivo-call-logd/conf.d -it xivo-call-logd bash

After launch xivo-call-logd.

    xivo-call-logd -f -v

## Infos

- Using docker version 1.5.0 (from get.docker.io) on ubuntu 14.04.
- If you want to using a simple webi to administrate docker use : https://github.com/crosbymichael/dockerui

To get the IP of your container use :

    docker ps -a
    docker inspect <container_id> | grep IPAddress | awk -F\" '{print $4}'
