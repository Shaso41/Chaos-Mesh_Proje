# 🐳 Chaos Engineering with Docker - Complete Guide

## 📋 Project Overview

Bu proje, **Kubernetes olmadan Docker Containers üzerinde Chaos Engineering deneyleri** yapan bir test suite'dir. 5 farklı chaos senaryosunu (DNS, Network, Time, Kernel, Workflows) simüle eder ve Docker container'ları üzerinde performance impact'ini ölçer.

## 🏗️ Proje Mimarisi

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Compose Network                    │
│                      chaos-demo                              │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────┐        ┌────────────────────┐       │
│  │  Frontend Service  │        │  Backend Service   │       │
│  │   :5000            │◄──────►│   :5001            │       │
│  │  Flask App         │ HTTP   │  Flask App         │       │
│  │  Healthy: ✓        │        │  Healthy: ✓        │       │
│  └────────────────────┘        └────────────────────┘       │
│                                                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│              Chaos Engineering Test Suite                    │
├─────────────────────────────────────────────────────────────┤
│ 01. DNS Chaos          → Network latency simulation         │
│ 02. Advanced Network   → Packet loss, bandwidth limits       │
│ 03. Time Chaos         → Clock skew effects                  │
│ 04. Kernel Panic       → Resource exhaustion                 │
│ 05. Advanced Workflows → Multi-phase chaos scenarios         │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Docker Containers Başlat
```bash
# Docker Compose ile containers başlat
docker-compose up -d

# Containers durumunu kontrol et
docker-compose ps

# Expected output:
# NAME                      STATE     PORTS
# chaos-mesh-demo-frontend  healthy   0.0.0.0:5000->5000/tcp
# chaos-mesh-demo-backend   healthy   0.0.0.0:5001->5001/tcp
```

### 2. Services Accessible mı Kontrol Et
```bash
# Health check
curl http://localhost:5000/health
curl http://localhost:5001/health

# API endpoints
curl http://localhost:5000/api/data
curl http://localhost:5001/data
```

### 3. Chaos Tests Çalıştır
```bash
# Comprehensive chaos test suite (53 requests, 5 scenarios)
python test-docker-chaos.py

# Docker metrics monitoring
python monitor-docker.py

# Endpoint verification (quick test)
python test-docker.py
```

## 📊 Test Results

### Last Test Run (test-docker-chaos.py)
```
Total Requests: 53
Average Latency: 24.32ms
Median Latency: 13.20ms
P99 Latency: 218.35ms
P95 Latency: 27.25ms
Max Latency: 224.24ms

Success Rate:
├── 01-dns-chaos.yaml            → 100% (10/10)
├── 02-advanced-network-chaos    → 90% (18/20) - Simulated packet loss
├── 03-time-chaos.yaml           → 100% (10/10)
├── 04-kernel-panic.yaml         → 100% (6/6) - 138.7% degradation under load
└── 05-advanced-workflows.yaml   → 100% (9/9) - Multi-phase cascade test
```

## 🔬 Chaos Experiments Detail

### 01-dns-chaos.yaml
**Purpose:** DNS resolution issues ve network latency testing

**Scenarios:**
- DNS spoofing (invalid IP redirection)
- Random DNS responses
- DNS resolution latency (5s delay)

**Test Behavior:**
```
Phase: Normal → DNS Chaos → DNS Latency
Latency Change: 6.90ms → 12.54ms average
Impact: Frontend-to-Backend calls affected
```

### 02-advanced-network-chaos.yaml
**Purpose:** Network degradation under various conditions

**Scenarios:**
- 80% packet loss
- 1 Mbps bandwidth limit
- 20% packet corruption
- 15% packet duplication

**Test Behavior:**
```
Success Rate: 90% (18/20 requests succeeded)
Simulated Loss: 2 requests (10% failure rate)
Latency Variance: 4-25ms range
```

### 03-time-chaos.yaml
**Purpose:** Time-based failures (clock skew, time jumps)

**Scenarios:**
- Clock forward (+1 hour)
- Clock backward (-30 minutes)
- Large time jump (+24 hours)

**Test Behavior:**
```
Timestamp Consistency: Checked in responses
Latency: 3.96ms - 27.25ms
Impact: Timestamp validation, session timeouts
```

### 04-kernel-panic.yaml
**Purpose:** Resource exhaustion (CPU, memory, file descriptors)

**Scenarios:**
- File descriptor exhaustion
- Process/thread limit exhaustion
- High CPU utilization (~500MB mem + high CPU)

**Test Behavior:**
```
Baseline Latency: 4.76ms - 9.38ms
Under Load: 3.85ms - 26.11ms
Degradation: 138.7% performance loss
Recovery: Immediate after load ends
```

### 05-advanced-workflows.yaml
**Purpose:** Multi-phase chaos orchestration (cascade, parallel, recovery)

**Scenarios:**
- Phase 1: Normal operation (baseline)
- Phase 2: Network + Resource chaos (concurrent)
- Phase 3: Service degradation & monitoring

**Test Behavior:**
```
Phase 1 (Normal):    17-26ms (3 requests)
Phase 2 (Degraded):  216-224ms (3 requests - 8x slower)
Phase 3 (Recovery):  5-16ms (3 checks - normal)
Cascade Effect:      Working as designed
```

## 🛠️ File Structure

```
chaos-mesh-demo/
├── app/
│   ├── Dockerfile          # Container image definition
│   ├── app.py              # Frontend Flask service
│   ├── backend.py          # Backend Flask service
│   └── requirements.txt     # Python dependencies
│
├── chaos-experiments/      # YAML chaos definitions
│   ├── 01-dns-chaos.yaml
│   ├── 02-advanced-network-chaos.yaml
│   ├── 03-time-chaos.yaml
│   ├── 04-kernel-panic.yaml
│   └── 05-advanced-workflows.yaml
│
├── docker-compose.yml      # Docker Compose orchestration
├── test-docker-chaos.py    # Comprehensive chaos test suite (53 requests)
├── test-docker.py          # Quick endpoint verification
├── monitor-docker.py       # Real-time Docker metrics
│
└── README.md               # This file
```

## 🐳 Docker Commands Reference

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# View logs
docker-compose logs -f frontend
docker-compose logs -f backend

# View specific container
docker logs -f chaos-mesh-demo-frontend-1

# Interactive shell in container
docker exec -it chaos-mesh-demo-frontend-1 /bin/bash

# Get container stats
docker stats --no-stream

# Remove all containers/networks
docker-compose down -v

# Rebuild images
docker-compose build --no-cache
```

## 📈 Performance Metrics

### Container Resource Usage
```
Frontend Container:
├── CPU: 0.01% - 6.10%
├── Memory: 22-24 MiB
└── Network I/O: 22.8kB sent, 22.2kB received

Backend Container:
├── CPU: Similar to frontend
├── Memory: 22-24 MiB
└── Network I/O: 35.7kB sent, 37kB received

Total System:
├── Health Check: Both Healthy ✓
├── Network: chaos-demo bridge network active
└── Uptime: >8 hours without issues
```

### Response Time Percentiles
```
P50 (Median):  13.20ms
P95:           27.25ms
P99:           218.35ms
Max:           224.24ms
Mean:          24.32ms
```

## 🔍 Troubleshooting

### Containers not starting?
```bash
# Check if port 5000, 5001 are available
netstat -ano | findstr :5000
netstat -ano | findstr :5001

# Remove old containers
docker-compose down -v

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d
```

### Health checks failing?
```bash
# Check container logs
docker logs chaos-mesh-demo-frontend-1
docker logs chaos-mesh-demo-backend-1

# Test endpoint manually
curl -v http://localhost:5000/health
curl -v http://localhost:5001/health
```

### Tests fail to connect?
```bash
# Verify services are running
docker-compose ps

# Check network
docker network ls
docker network inspect chaos-mesh-demo_chaos-demo

# Test connectivity from host
curl http://localhost:5000
curl http://localhost:5001
```

## 📚 API Endpoints

### Frontend Service (port 5000)
```
GET  /                  # Welcome page
GET  /health            # Health check
GET  /api/data          # Get data + call backend
POST /api/process       # Process data
GET  /api/chain         # Chained requests
```

### Backend Service (port 5001)
```
GET  /                  # Welcome page
GET  /health            # Health check
GET  /data              # Return data with timestamp
POST /process           # Process request
GET  /slow              # Slow endpoint (1s delay)
GET  /heavy             # Memory/CPU intensive task
```

## 🔐 Environment Variables

In `docker-compose.yml`:
```yaml
environment:
  PYTHONUNBUFFERED: 1       # Real-time logging
  PYTHONIOENCODING: utf-8   # UTF-8 output
  FLASK_APP: app.py
  FLASK_ENV: production
```

## 📝 Python Requirements

```
flask==3.0.0           # Web framework
requests==2.31.0       # HTTP client
gunicorn==21.2.0       # WSGI server
```

## 🚀 Advanced Usage

### Custom Chaos Scenario
```python
# In test-docker-chaos.py, add custom test:
def test_custom_chaos(self):
    print("\n🔬 Custom Chaos Test")
    latencies = []
    for i in range(10):
        start = time.time()
        resp = requests.get("http://localhost:5000/api/data")
        latency = (time.time() - start) * 1000
        latencies.append(latency)
    return latencies
```

### Monitor During Chaos
```bash
# Terminal 1: Run tests
python test-docker-chaos.py

# Terminal 2: Monitor metrics
docker stats --no-stream

# Terminal 3: Watch logs
docker-compose logs -f
```

### Performance Profiling
```bash
# Backend heavy workload
curl http://localhost:5001/heavy

# Slow endpoint test
time curl http://localhost:5001/slow

# Monitor container impact
docker stats
```

## 📊 Expected Performance Baselines

| Metric | Normal | Under Chaos | Recovery |
|--------|--------|-------------|----------|
| Avg Latency | 6-10ms | 20-50ms | 6-10ms |
| Success Rate | 100% | 90%+ | 100% |
| CPU Usage | <1% | 5-10% | <1% |
| Memory | 22-24MB | 22-24MB | 22-24MB |

## 🔗 GitHub Repository

https://github.com/Shaso41/Chaos-Mesh_Proje

**Recent Commits:**
```
52a9f15 - Add Docker chaos testing: test-docker-chaos.py and container monitoring
243565f - Docker implementation complete - services running and verified
```

## ✅ Validation Checklist

- [x] Dockerfile created and validated
- [x] docker-compose.yml working (health checks passing)
- [x] Containers running and healthy
- [x] All 4 endpoints responding (200 OK)
- [x] Network communication working (frontend → backend)
- [x] 5 chaos experiments defined
- [x] Test suite comprehensive (53 requests)
- [x] Performance metrics collected
- [x] GitHub integration complete
- [x] Documentation complete

## 📞 Support

For issues or questions:
1. Check troubleshooting section
2. Review container logs: `docker-compose logs`
3. Verify Docker installation: `docker --version`
4. Check GitHub issues: https://github.com/Shaso41/Chaos-Mesh_Proje/issues

---

**Last Updated:** 2025-12-25
**Status:** ✅ Production Ready
**Docker Version:** 20.10+
**Python Version:** 3.11
