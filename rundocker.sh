#!/bin/bash

# 1. Build Docker image
docker build -t syvbot .

# 2. Run Docker container with auto-restart and mounted volume
docker run -d \
  --name syvbot \
  --restart unless-stopped \
  -v $PWD/servers:/app/servers \
  syvbot

# 3. Show running containers
docker ps

# 4. Show logs
docker logs -f syvbot
