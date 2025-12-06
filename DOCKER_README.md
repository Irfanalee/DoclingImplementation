# Docling Server - Docker Deployment Guide

This guide explains how to run the Docling Server as a containerized microservice.

## 📋 Prerequisites

- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (comes with Docker Desktop)

## 🚀 Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Place your PDF files** in the `./data` folder

2. **Start the service:**
   ```bash
   docker-compose up -d
   ```

3. **Process documents via API:**
   ```bash
   curl -X POST http://localhost:8000/process
   ```

4. **Check the output** in the `./output` folder

5. **Stop the service:**
   ```bash
   docker-compose down
   ```

### Option 2: Using Docker Directly

1. **Build the Docker image:**
   ```bash
   docker build -t docling-server .
   ```

2. **Run the container:**
   ```bash
   docker run -d \
     --name docling-server \
     -p 8000:8000 \
     -v $(pwd)/data:/app/input:ro \
     -v $(pwd)/output:/app/output \
     docling-server
   ```

3. **Stop the container:**
   ```bash
   docker stop docling-server
   docker rm docling-server
   ```

## 🔌 API Endpoints

The Docling Server exposes a REST API on port 8000:

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Process Documents
```bash
curl -X POST http://localhost:8000/process
```

**Response:**
```json
{
  "status": "success",
  "message": "Processed 3 PDF file(s)",
  "output_folder": "/app/output/run_20231206_143022",
  "timestamp": "20231206_143022"
}
```

### 3. Get Latest Summary
```bash
curl http://localhost:8000/summary
```

### 4. List All Processing Runs
```bash
curl http://localhost:8000/runs
```

### 5. Delete a Specific Run
```bash
curl -X DELETE http://localhost:8000/runs/run_20231206_143022
```

### 6. API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

## 📁 Output Structure

Each processing run creates a timestamped folder:

```
output/
└── run_20231206_143022/
    ├── tables/
    │   ├── document1_table_1.csv
    │   └── document2_table_1.csv
    ├── images/
    │   ├── document1/
    │   │   ├── page1_img1.png
    │   │   └── page2_img1.jpg
    │   └── document2/
    │       └── page1_img1.png
    ├── markdown/
    │   ├── document1.md
    │   └── document2.md
    └── summary_report.txt
```

## 🔧 Configuration

### Environment Variables

You can customize the service using environment variables in `docker-compose.yml`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=info
```

### Volume Mounts

- `./data:/app/input:ro` - Mount your data folder as read-only input
- `./output:/app/output` - Mount output folder to persist results

## 🏗️ Microservice Architecture Integration

### Using with Kubernetes

Create a deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docling-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: docling-server
  template:
    metadata:
      labels:
        app: docling-server
    spec:
      containers:
      - name: docling-server
        image: docling-server:latest
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: input
          mountPath: /app/input
        - name: output
          mountPath: /app/output
      volumes:
      - name: input
        persistentVolumeClaim:
          claimName: docling-input-pvc
      - name: output
        persistentVolumeClaim:
          claimName: docling-output-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: docling-server
spec:
  selector:
    app: docling-server
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

### Using with Docker Swarm

```bash
docker stack deploy -c docker-compose.yml docling
```

### Integration Examples

#### Python Client
```python
import requests

# Process documents
response = requests.post("http://localhost:8000/process")
print(response.json())

# Get summary
summary = requests.get("http://localhost:8000/summary")
print(summary.json())
```

#### JavaScript/Node.js Client
```javascript
// Process documents
fetch('http://localhost:8000/process', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data));

// Get summary
fetch('http://localhost:8000/summary')
  .then(response => response.json())
  .then(data => console.log(data));
```

## 🐛 Troubleshooting

### Check Container Logs
```bash
docker-compose logs -f
```

### Inspect Container
```bash
docker exec -it docling-server bash
```

### Rebuild Image
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Check Disk Space
```bash
docker system df
```

### Clean Up
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Full cleanup
docker system prune -a
```

## 📊 Performance Tips

1. **Resource Limits**: Add resource limits in docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 4G
   ```

2. **Scaling**: Run multiple instances:
   ```bash
   docker-compose up -d --scale docling-server=3
   ```

3. **Caching**: Mount a cache directory for faster processing:
   ```yaml
   volumes:
     - ./.docling:/root/.docling
   ```

## 🔒 Security Considerations

1. **Read-only Input**: Input folder is mounted as read-only (`:ro`)
2. **No Root User**: Consider adding a non-root user in the Dockerfile
3. **Network Isolation**: Use Docker networks to isolate services
4. **Secrets Management**: Use Docker secrets for sensitive data

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docling Documentation](https://github.com/DS4SD/docling)

## 🆘 Support

For issues and questions, please check:
- Container logs: `docker-compose logs`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
