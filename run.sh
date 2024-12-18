#!/bin/bash

docker network create my_network

docker-compose -f docker-compose.yml up --build -d

cd fake_fns

docker-compose -f docker-compose.yml up --build -d