#!/bin/bash
set -e

echo "Running integration tests for cadCAD model API"
echo "============================================"

# Ensure container is running
echo "Starting test container..."
docker run -d --name test-model -p 8000:8000 cadcad-model:test

# Wait for container to be ready
echo "Waiting for service to be ready..."
sleep 5

# Test healthcheck
echo -e "\nTesting healthcheck endpoint..."
curl -s http://localhost:8000/healthcheck

# Test metadata
echo -e "\n\nTesting metadata endpoint..."
curl -s http://localhost:8000/metadata

# Test simulation with different parameters
echo -e "\n\nTesting simulation endpoint..."

# Test case 1: Default parameters
echo "Test case 1: Default parameters"
curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "beta": 0.3,
      "gamma": 0.1,
      "population": 1000
    },
    "config": {
      "timesteps": 100,
      "samples": 1
    }
  }'

# Test case 2: High transmission rate
echo -e "\n\nTest case 2: High transmission rate"
curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "beta": 0.8,
      "gamma": 0.1,
      "population": 1000
    },
    "config": {
      "timesteps": 100,
      "samples": 1
    }
  }'

# Test case 3: Multiple samples
echo -e "\n\nTest case 3: Multiple samples"
curl -s -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "parameters": {
      "beta": 0.3,
      "gamma": 0.1,
      "population": 1000
    },
    "config": {
      "timesteps": 100,
      "samples": 5
    }
  }'

# Cleanup
echo -e "\n\nCleaning up..."
docker stop test-model
docker rm test-model

echo -e "\nTests completed successfully!"
