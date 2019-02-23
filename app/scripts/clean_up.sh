#!/usr/bin/env bash

# kill container and remove image
for x in $(docker ps -a | awk '{print $1}' | grep -v 'CONTAINER'); do
    docker kill $x
    docker rm $x
done

# remove all images
for x in $(docker images | awk '{print $3}' | grep -v 'IMAGE'); do
    docker rmi $x
done

docker network rm studio_xkcd

rm -rf /opt/python/studio/mysql

