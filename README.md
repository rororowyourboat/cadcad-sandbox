# cadCAD Model API Standards

This repository provides a standardized approach for serving cadCAD models via REST APIs.

## Standards for Serving cadCAD Models

### 1. Model Structure

```plaintext
model/
├── __init__.py
├── core_logic.py     # Core system dynamics
├── experiment.py     # Simulation configuration
├── params.py        # Parameter definitions
└── types.py        # Type definitions
```

### 2. API Design Principles

1. **Separation of Concerns**
   - Model logic separate from API layer
   - Raw simulation data separate from analysis
   - Clear interface between components

2. **Standard Endpoints**
   ```plaintext
   GET /healthcheck   # System health
   GET /metadata     # Model parameters and configuration
   POST /run         # Execute simulation
   ```

3. **Parameter Management**
   - All parameters documented in metadata
   - Default values provided
   - Valid ranges specified
   - Clear descriptions

4. **Response Format**
   ```json
   {
     "success": true,
     "data": {
       "results": [],      // Simulation results
       "parameters": {},   // Used parameters
       "config": {}       // Run configuration
     },
     "metadata": {
       "execution_time": "",
       "timestamp": ""
     }
   }
   ```

### 3. Container Standards

1. **Base Image**
   - Use Python slim images
   - Pin specific versions
   - Minimize layer count

2. **Dependencies**
   - Use requirements.txt or pyproject.toml
   - Pin all versions
   - Use deterministic builds (uv/pip-tools)

3. **Security**
   - Run as non-root user
   - Minimal dependencies
   - No credentials in image

## Quick Start

```bash
# Build and run with Docker
docker build -t cadcad-model .
docker run -p 8000:8000 cadcad-model
```

## Testing Docker Containers

### 1. Build Testing

```bash
# Test build process
docker build -t cadcad-model:test .

# Check image size
docker images cadcad-model:test

# Inspect layers
docker history cadcad-model:test
```

### 2. Runtime Testing

```bash
# Run container with test config
docker run -d --name test-model -p 8000:8000 cadcad-model:test

# Check container status
docker ps
docker logs test-model

# Test endpoints
curl http://localhost:8000/healthcheck
curl http://localhost:8000/metadata

# Run simulation
curl -X POST http://localhost:8000/run \
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

# Stop container
docker stop test-model
docker rm test-model
```

### 3. Integration Testing

```bash
# Test with different configurations
./test_scripts/run_integration_tests.sh

# Load testing (requires k6)
k6 run test_scripts/load_test.js
```

### 4. Common Issues

1. Port Conflicts
   ```bash
   # Find and stop conflicting containers
   docker ps | grep 8000
   docker stop <container_id>
   ```

2. Resource Limits
   ```bash
   # Run with memory limits
   docker run -m 512m -p 8000:8000 cadcad-model
   ```

3. Persistence
   ```bash
   # Use volumes for data persistence
   docker run -v data:/app/data -p 8000:8000 cadcad-model
   ```

## API Documentation

[Previous API documentation remains unchanged...]

## Development

### Project Structure
```plaintext
.
├── model/              # Core model logic
├── tests/              # Test suite
├── Dockerfile          # Container definition
├── metadata.json      # Model configuration
├── pyproject.toml     # Project metadata
├── requirements.txt   # Dependencies
└── serve_model.py     # API server
```

### Adding New Models

1. Implement core logic in `model/core_logic.py`
2. Define parameters in `model/params.py`
3. Configure experiment in `model/experiment.py`
4. Update metadata.json with parameters
5. Test endpoints
6. Build and verify container

## Deployment

### Environment Variables

- `PORT`: Server port (default: 8000)
- `LOG_LEVEL`: Logging level (default: info)
- `MAX_WORKERS`: Uvicorn workers (default: 1)

### Health Monitoring

1. Use /healthcheck endpoint
2. Monitor container metrics
3. Set up alerting for failures

### Performance Optimization

1. Profile memory usage
2. Monitor execution times
3. Optimize simulation parameters
4. Scale horizontally as needed
