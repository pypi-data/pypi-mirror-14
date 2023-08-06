#!/bin/bash

# This is not the final version and it's a stop gap implementation
# to get things up and running on gate
echo "networking-plumgrid packages pre-reqs installation"
sudo apt-get update; sudo apt-get -y install $(grep -vE "^\s*#" ../tools/debs/general  | tr "\n" " ")
sudo apt-get -y install $(grep -vE "^\s*#" ../tools/debs/dev  | tr "\n" " ")
