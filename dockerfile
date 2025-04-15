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