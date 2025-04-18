#!/bin/bash

set -e

# Print colored text
print_color() {
  case $1 in
    "info") COLOR="\033[0;36m" ;;    # Cyan
    "success") COLOR="\033[0;32m" ;; # Green
    "warning") COLOR="\033[0;33m" ;; # Yellow
    "error") COLOR="\033[0;31m" ;;   # Red
    *) COLOR="\033[0m" ;;            # No Color
  esac
  echo -e "${COLOR}$2\033[0m"
}

# Stop containers and remove networks
print_color "info" "Stopping any running containers..."
docker-compose down --remove-orphans
docker-compose -f docker-compose.frontend.yml down --remove-orphans

# Create the shared network
print_color "info" "Creating shared network..."
if ! docker network ls | grep -q "app-network"; then
  docker network create app-network
  print_color "success" "Created app-network"
else
  print_color "info" "app-network already exists"
fi

# Build and start the backend services
print_color "info" "Starting backend services..."
docker-compose up -d --build

# Check if backend is running
if [ $? -eq 0 ]; then
  print_color "success" "Backend services started successfully"
else
  print_color "error" "Failed to start backend services"
  exit 1
fi

# Build and start the frontend service
print_color "info" "Starting frontend service..."
docker-compose -f docker-compose.frontend.yml up -d --build

# Check if frontend is running
if [ $? -eq 0 ]; then
  print_color "success" "Frontend service started successfully"
else
  print_color "error" "Failed to start frontend service"
  exit 1
fi

print_color "success" "All services are running!"
print_color "info" "Backend API available at: http://localhost:8000"
print_color "info" "Frontend available at: http://localhost:3000" 