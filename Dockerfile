FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
# Update requirements to include pyyaml if not already there, but we checked it is there.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set default PORT environment variable and expose validation port
ENV PORT=8080
EXPOSE 8080

# Run the application
# Using shell form to expand PORT variable and bind to all interfaces
CMD ["sh", "-c", "adk web --host 0.0.0.0 --port ${PORT:-8080}"]
