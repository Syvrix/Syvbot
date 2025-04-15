# Use a lightweight Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files into container
COPY . .
COPY .env .env


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python3", "-u","bot.py"]

# 2. Build docker image
from project root:
'docker build -t syvbot .'

# 3. Run the bot container (with auto-start)
'docker run -d \
  --name syvbot \
  --restart unless-stopped \
  -v $PWD/servers:/app/servers \
  syvbot'

  # Explanation:
'-d: detached mode (runs in background)

--restart unless-stopped: restarts bot if EC2 reboots

-v: mounts your servers/ folder for persistent storage'

# 4. Check if it works
'docker ps        # See if the container is running
docker logs syvbot  # See bot output logs
'