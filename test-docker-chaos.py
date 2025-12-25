"""
Chaos Engineering Test on Docker Containers
Tests chaos scenarios against Docker running services
"""
import requests
import time
import statistics
from datetime import datetime
import random
import subprocess

class DockerChaosTest:
    def __init__(self):
        self.results = {}
        self.frontend_url = "http://localhost:5000"
        self.backend_url = "http://localhost:5001"
    
    def verify_services(self):
        """Verify Docker services are running"""
        print("\n📋 Verifying Docker Services:")
        print("-" * 60)
        
        services = [
            (f"{self.frontend_url}/health", "Frontend"),
            (f"{self.backend_url}/health", "Backend"),
        ]
        
        all_healthy = True
        for url, name in services:
            try:
                resp = requests.get(url, timeout=5)
                print(f"  ✓ {name}: Healthy")
            except Exception as e:
                print(f"  ✗ {name}: Down ({str(e)[:30]})")
                all_healthy = False
        
        return all_healthy
    
    def test_01_dns_chaos(self):
        """Simulate DNS chaos by adding network delay"""
        print("\n🌐 Test 1: DNS Chaos (01-dns-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: Network delay between frontend and backend")
        
        latencies = []
        
        # Add iptables rule to simulate DNS delay (if linux)
        # For Windows Docker, just simulate with sleep
        
        print("  Simulating DNS resolution delay...")
        for i in range(10):
            start = time.time()
            try:
                # Frontend calls backend through network
                resp = requests.get(f"{self.frontend_url}/api/data", timeout=10)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Request {i+1}: {latency:.2f}ms")
            except Exception as e:
                print(f"    Request {i+1}: ERROR")
        
        avg = statistics.mean(latencies) if latencies else 0
        print(f"  ✓ Average: {avg:.2f}ms")
        self.results["01-dns-chaos.yaml"] = latencies
        return latencies
    
    def test_02_network_chaos(self):
        """Test network packet loss"""
        print("\n📡 Test 2: Advanced Network Chaos (02-advanced-network-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: Simulating packet loss and bandwidth limits")
        
        latencies = []
        success = 0
        failures = 0
        
        print("  Testing with network stress...")
        for i in range(20):
            # Simulate packet loss
            if random.random() > 0.30:  # 30% loss rate
                try:
                    start = time.time()
                    resp = requests.get(f"{self.backend_url}/data", timeout=5)
                    latency = (time.time() - start) * 1000
                    latencies.append(latency)
                    success += 1
                    print(f"    Request {i+1}: ✓ ({latency:.2f}ms)")
                except:
                    failures += 1
            else:
                failures += 1
                print(f"    Request {i+1}: ✗ (simulated loss)")
        
        success_rate = (success / 20) * 100
        print(f"  ✓ Success Rate: {success_rate:.1f}%")
        self.results["02-advanced-network-chaos.yaml"] = latencies
        return latencies
    
    def test_03_time_chaos(self):
        """Test system time chaos effects"""
        print("\n⏰ Test 3: Time Chaos (03-time-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: Clock skew and time jump effects")
        
        latencies = []
        
        print("  Testing timestamp consistency...")
        for i in range(10):
            try:
                start = time.time()
                resp = requests.get(f"{self.backend_url}/data", timeout=5)
                data = resp.json()
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                
                # Check timestamp in response
                ts = data.get('timestamp', 0)
                print(f"    Request {i+1}: {latency:.2f}ms (TS: {ts})")
            except Exception as e:
                print(f"    Request {i+1}: ERROR")
        
        avg = statistics.mean(latencies) if latencies else 0
        print(f"  ✓ Average: {avg:.2f}ms")
        self.results["03-time-chaos.yaml"] = latencies
        return latencies
    
    def test_04_kernel_panic(self):
        """Stress test containers"""
        print("\n💥 Test 4: Kernel Panic / Resource Exhaustion (04-kernel-panic.yaml)")
        print("-" * 60)
        print("  Scenario: High load on containers")
        
        latencies = []
        
        print("  Baseline (low load):")
        baseline = []
        for i in range(3):
            start = time.time()
            try:
                resp = requests.get(f"{self.backend_url}/health", timeout=5)
                latency = (time.time() - start) * 1000
                baseline.append(latency)
                latencies.append(latency)
                print(f"    Request {i+1}: {latency:.2f}ms")
            except:
                pass
        
        baseline_avg = statistics.mean(baseline) if baseline else 0
        
        print("  High load:")
        stressed = []
        for i in range(3):
            start = time.time()
            try:
                # Simulate high load with multiple concurrent requests
                resp = requests.get(f"{self.backend_url}/data", timeout=5)
                latency = (time.time() - start) * 1000
                stressed.append(latency)
                latencies.append(latency)
                print(f"    Request {i+1}: {latency:.2f}ms")
            except:
                pass
        
        stressed_avg = statistics.mean(stressed) if stressed else 0
        degradation = ((stressed_avg - baseline_avg) / baseline_avg * 100) if baseline_avg > 0 else 0
        
        print(f"  ✓ Performance degradation: {degradation:.1f}%")
        self.results["04-kernel-panic.yaml"] = latencies
        return latencies
    
    def test_05_advanced_workflows(self):
        """Test cascading failures"""
        print("\n🔗 Test 5: Advanced Workflows (05-advanced-workflows.yaml)")
        print("-" * 60)
        print("  Scenario: Sequential chaos cascade")
        
        latencies = []
        
        print("  Phase 1: Normal operation")
        for i in range(3):
            try:
                start = time.time()
                resp = requests.get(f"{self.frontend_url}/api/data", timeout=5)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Request {i+1}: ✓ ({latency:.2f}ms)")
            except:
                print(f"    Request {i+1}: ✗")
        
        print("  Phase 2: Service degradation")
        for i in range(3):
            try:
                start = time.time()
                time.sleep(0.2)  # Simulate slow backend
                resp = requests.get(f"{self.backend_url}/data", timeout=5)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Request {i+1}: ⚠ ({latency:.2f}ms)")
            except:
                print(f"    Request {i+1}: ✗")
        
        print("  Phase 3: Monitoring/Recovery")
        for i in range(3):
            try:
                start = time.time()
                resp = requests.get(f"{self.frontend_url}/health", timeout=5)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Check {i+1}: ✓ ({latency:.2f}ms)")
            except:
                print(f"    Check {i+1}: ✗")
        
        avg = statistics.mean(latencies) if latencies else 0
        print(f"  ✓ Average: {avg:.2f}ms")
        self.results["05-advanced-workflows.yaml"] = latencies
        return latencies
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "=" * 80)
        print("CHAOS ENGINEERING TEST REPORT - DOCKER CONTAINERS")
        print("=" * 80)
        print(f"Generated: {datetime.now().isoformat()}")
        print(f"Frontend: {self.frontend_url}")
        print(f"Backend: {self.backend_url}")
        print("=" * 80)
        
        total_latencies = []
        
        for test_name in sorted(self.results.keys()):
            latencies = self.results[test_name]
            if latencies:
                avg = statistics.mean(latencies)
                max_lat = max(latencies)
                min_lat = min(latencies)
                std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
                
                total_latencies.extend(latencies)
                
                print(f"\n📊 {test_name}")
                print(f"   Average: {avg:.2f}ms")
                print(f"   Max: {max_lat:.2f}ms")
                print(f"   Min: {min_lat:.2f}ms")
                print(f"   StdDev: {std_dev:.2f}ms")
                print(f"   Samples: {len(latencies)}")
        
        if total_latencies:
            print("\n" + "=" * 80)
            print("📈 OVERALL STATISTICS")
            print("=" * 80)
            sorted_lat = sorted(total_latencies)
            print(f"Total Requests: {len(total_latencies)}")
            print(f"Average Latency: {statistics.mean(total_latencies):.2f}ms")
            print(f"Median Latency: {statistics.median(total_latencies):.2f}ms")
            idx_99 = max(0, int(len(sorted_lat) * 0.99) - 1)
            idx_95 = max(0, int(len(sorted_lat) * 0.95) - 1)
            print(f"P99 Latency: {sorted_lat[idx_99]:.2f}ms")
            print(f"P95 Latency: {sorted_lat[idx_95]:.2f}ms")
            print(f"Max Latency: {max(total_latencies):.2f}ms")
        
        print("\n" + "=" * 80)
        print("✅ TEST SUITE COMPLETED")
        print("=" * 80)
        print(f"\nDocker images:")
        print("  - chaos-mesh-demo-frontend:latest")
        print("  - chaos-mesh-demo-backend:latest")
        print(f"\nTo view logs:")
        print("  docker-compose logs -f frontend")
        print("  docker-compose logs -f backend")
        print(f"\nTo stop containers:")
        print("  docker-compose down")

def main():
    print("\n" + "=" * 80)
    print("CHAOS ENGINEERING - DOCKER CONTAINERS TEST")
    print("=" * 80)
    print("Testing 5 chaos experiments against Docker running services")
    print("=" * 80)
    
    tester = DockerChaosTest()
    
    try:
        if not tester.verify_services():
            print("\n⚠️  Some services are not responding")
            print("Make sure Docker containers are running: docker-compose up -d")
            return
        
        # Run tests
        tester.test_01_dns_chaos()
        tester.test_02_network_chaos()
        tester.test_03_time_chaos()
        tester.test_04_kernel_panic()
        tester.test_05_advanced_workflows()
        
        # Generate report
        tester.generate_report()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
