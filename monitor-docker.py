"""
Docker Container Performance Monitoring
Real-time metrics from running Docker containers
"""
import subprocess
import json
import time
from datetime import datetime

def get_docker_stats():
    """Get real-time Docker stats"""
    try:
        result = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            # Parse JSON output
            stats_lines = result.stdout.strip().split('\n')
            containers = []
            for line in stats_lines:
                if line:
                    try:
                        containers.append(json.loads(line))
                    except:
                        pass
            return containers
        return None
    except Exception as e:
        print(f"Error getting Docker stats: {e}")
        return None

def get_container_logs(container_name, lines=20):
    """Get container logs"""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout if result.returncode == 0 else None
    except:
        return None

def monitor_docker():
    """Monitor Docker containers during chaos tests"""
    print("\n" + "=" * 90)
    print("DOCKER CONTAINER MONITORING - REAL-TIME METRICS")
    print("=" * 90)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 90)
    
    # Get stats
    stats = get_docker_stats()
    
    if stats:
        print("\n📊 CONTAINER METRICS:")
        print("-" * 90)
        print(f"{'Container':<40} {'CPU%':<10} {'Memory':<15} {'NET I/O':<25}")
        print("-" * 90)
        
        for stat in stats:
            name = stat.get('Names', 'Unknown')[:35]
            cpu = stat.get('CPUPerc', 'N/A')
            mem = stat.get('MemUsage', 'N/A')
            net = stat.get('NetIO', 'N/A')
            
            print(f"{name:<40} {cpu:<10} {mem:<15} {net:<25}")
    
    # Get container info
    print("\n🐳 DOCKER CONTAINER STATUS:")
    print("-" * 90)
    
    containers = ["chaos-mesh-demo-frontend-1", "chaos-mesh-demo-backend-1"]
    
    for container in containers:
        try:
            result = subprocess.run(
                ["docker", "inspect", container, "--format", 
                 "State: {{.State.Status}} | Health: {{.State.Health.Status}} | Uptime: {{.State.StartedAt}}"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                print(f"\n{container}:")
                print(f"  {result.stdout.strip()}")
            
            # Get recent logs
            logs = get_container_logs(container, 5)
            if logs:
                print(f"  Recent logs:")
                for log_line in logs.strip().split('\n')[:5]:
                    if log_line:
                        print(f"    → {log_line[:80]}")
        
        except Exception as e:
            print(f"\n{container}: Error - {e}")
    
    print("\n" + "=" * 90)
    print("✅ MONITORING COMPLETE")
    print("=" * 90)

if __name__ == "__main__":
    monitor_docker()
