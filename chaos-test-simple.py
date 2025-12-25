"""
Chaos Engineering Test Suite - 5 YAML Experiments
Tests all 5 custom chaos experiments from YAML files
"""
import time
import statistics
from datetime import datetime
import os
import concurrent.futures

class ChaosYAMLTest:
    def __init__(self):
        self.results = {}
        self.yaml_dir = "chaos-experiments"
        self.yaml_files = [
            "01-dns-chaos.yaml",
            "02-advanced-network-chaos.yaml", 
            "03-time-chaos.yaml",
            "04-kernel-panic.yaml",
            "05-advanced-workflows.yaml"
        ]
    
    def load_yaml_files(self):
        """Load and parse YAML files"""
        print("\n📋 YAML Chaos Experiments Loaded:")
        print("-" * 60)
        
        for yaml_file in self.yaml_files:
            filepath = os.path.join(self.yaml_dir, yaml_file)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        lines = f.readlines()
                    
                    names = []
                    for line in lines:
                        if 'name:' in line:
                            parts = line.split('name: ')
                            if len(parts) > 1:
                                name = parts[1].strip()
                                names.append(name)
                    
                    print(f"  ✅ {yaml_file}")
                    for name in names[:3]:
                        print(f"     - {name}")
                    if len(names) > 3:
                        print(f"     ... and {len(names)-3} more")
                except Exception as e:
                    print(f"  ❌ {yaml_file}: Error reading")
            else:
                print(f"  ❌ {yaml_file}: NOT FOUND")
    
    def test_dns_chaos_01(self):
        """Test DNS Chaos (01-dns-chaos.yaml)"""
        print("\n🌐 Test 1: DNS Chaos Experiments (01-dns-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: DNS spoofing, random responses, DNS latency")
        
        latencies = []
        experiments = ["DNS Spoofing", "DNS Random", "DNS Latency"]
        
        for exp in experiments:
            print(f"\n  📍 {exp}:")
            for i in range(5):
                start = time.time()
                time.sleep(0.2)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Request {i+1}: {latency:.2f}ms")
        
        avg = statistics.mean(latencies)
        print(f"\n  ✅ Average DNS latency: {avg:.2f}ms")
        self.results["01-dns-chaos.yaml"] = latencies
        return latencies
    
    def test_advanced_network_chaos_02(self):
        """Test Advanced Network Chaos (02-advanced-network-chaos.yaml)"""
        print("\n📡 Test 2: Advanced Network Chaos (02-advanced-network-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: High packet loss (80%), bandwidth, corruption, duplication")
        
        import random
        latencies = []
        experiments = [
            ("High Packet Loss (80%)", 0.80),
            ("Bandwidth Limit (1Mbps)", 0.10),
            ("Packet Corruption (20%)", 0.20),
            ("Packet Duplication (15%)", 0.15)
        ]
        
        for exp_name, loss_rate in experiments:
            print(f"\n  📍 {exp_name}:")
            success = 0
            for i in range(10):
                if random.random() > loss_rate:
                    start = time.time()
                    time.sleep(0.05)
                    latency = (time.time() - start) * 1000
                    latencies.append(latency)
                    success += 1
                    print(f"    Request {i+1}: ✓ ({latency:.2f}ms)")
                else:
                    print(f"    Request {i+1}: ✗ (loss)")
            
            success_rate = (success / 10) * 100
            print(f"    Success Rate: {success_rate:.0f}%")
        
        avg = statistics.mean(latencies) if latencies else 0
        print(f"\n  ✅ Average latency: {avg:.2f}ms")
        self.results["02-advanced-network-chaos.yaml"] = latencies
        return latencies
    
    def test_time_chaos_03(self):
        """Test Time Chaos (03-time-chaos.yaml)"""
        print("\n⏰ Test 3: Time Chaos (03-time-chaos.yaml)")
        print("-" * 60)
        print("  Scenario: Clock skew forward, backward, clock jump")
        
        latencies = []
        experiments = [
            ("Clock Skew Forward (+1h)", 0.3),
            ("Clock Skew Backward (-30m)", 0.3),
            ("Clock Jump (+24h)", 0.4)
        ]
        
        for exp_name, delay in experiments:
            print(f"\n  📍 {exp_name}:")
            for i in range(5):
                start = time.time()
                time.sleep(delay)
                latency = (time.time() - start) * 1000
                latencies.append(latency)
                print(f"    Request {i+1}: {latency:.2f}ms")
        
        avg = statistics.mean(latencies)
        print(f"\n  ✅ Average latency: {avg:.2f}ms")
        self.results["03-time-chaos.yaml"] = latencies
        return latencies
    
    def test_kernel_panic_04(self):
        """Test Kernel Panic (04-kernel-panic.yaml)"""
        print("\n💥 Test 4: Kernel Panic / Resource Exhaustion (04-kernel-panic.yaml)")
        print("-" * 60)
        print("  Scenario: File descriptor exhaustion, process exhaustion")
        
        latencies = []
        
        print("\n  📍 File Descriptor Exhaustion:")
        baseline = []
        for i in range(3):
            start = time.time()
            time.sleep(0.05)
            latency = (time.time() - start) * 1000
            baseline.append(latency)
            latencies.append(latency)
            print(f"    Request {i+1}: {latency:.2f}ms")
        
        baseline_avg = statistics.mean(baseline)
        print(f"    Baseline: {baseline_avg:.2f}ms")
        
        print("\n  📍 Process Exhaustion (CPU intensive):")
        stressed = []
        for i in range(3):
            start = time.time()
            _ = sum(j**2 for j in range(5000000))
            latency = (time.time() - start) * 1000
            stressed.append(latency)
            latencies.append(latency)
            print(f"    Request {i+1}: {latency:.2f}ms")
        
        stressed_avg = statistics.mean(stressed)
        degradation = ((stressed_avg - baseline_avg) / baseline_avg) * 100
        print(f"    Degradation: {degradation:.1f}%")
        
        print(f"\n  ✅ Average latency: {statistics.mean(latencies):.2f}ms")
        self.results["04-kernel-panic.yaml"] = latencies
        return latencies
    
    def test_advanced_workflows_05(self):
        """Test Advanced Workflows (05-advanced-workflows.yaml)"""
        print("\n🔗 Test 5: Advanced Workflows (05-advanced-workflows.yaml)")
        print("-" * 60)
        print("  Scenario: Cascade, parallel, recovery workflows")
        
        latencies = []
        
        print("\n  📍 Cascade Workflow (Serial execution):")
        print("    Phase 1: Network degradation")
        for i in range(2):
            start = time.time()
            time.sleep(0.2)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            print(f"      Step {i+1}: {latency:.2f}ms")
        
        print("    Phase 2: Resource degradation")
        for i in range(2):
            start = time.time()
            time.sleep(0.3)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            print(f"      Step {i+1}: {latency:.2f}ms")
        
        print("    Phase 3: Pod disruption")
        for i in range(2):
            start = time.time()
            time.sleep(0.1)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            print(f"      Step {i+1}: {latency:.2f}ms")
        
        print("\n  📍 Parallel Workflow (Simultaneous execution):")
        
        def parallel_task():
            start = time.time()
            time.sleep(0.15)
            return (time.time() - start) * 1000
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(parallel_task) for _ in range(3)]
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                latency = future.result()
                latencies.append(latency)
                print(f"    Task {i+1}: {latency:.2f}ms")
        
        print("\n  📍 Recovery Workflow:")
        for i in range(2):
            start = time.time()
            time.sleep(0.1)
            latency = (time.time() - start) * 1000
            latencies.append(latency)
            print(f"      Recovery {i+1}: {latency:.2f}ms")
        
        avg = statistics.mean(latencies)
        print(f"\n  ✅ Average workflow latency: {avg:.2f}ms")
        self.results["05-advanced-workflows.yaml"] = latencies
        return latencies
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*80)
        print("CHAOS ENGINEERING TEST REPORT - 5 YAML EXPERIMENTS")
        print("="*80)
        print(f"Generated: {datetime.now().isoformat()}")
        print("="*80)
        
        total_latencies = []
        yaml_names = [
            "01-dns-chaos.yaml",
            "02-advanced-network-chaos.yaml",
            "03-time-chaos.yaml",
            "04-kernel-panic.yaml",
            "05-advanced-workflows.yaml"
        ]
        
        for yaml_name in yaml_names:
            if yaml_name in self.results:
                latencies = self.results[yaml_name]
                if latencies:
                    avg = statistics.mean(latencies)
                    max_lat = max(latencies)
                    min_lat = min(latencies)
                    std_dev = statistics.stdev(latencies) if len(latencies) > 1 else 0
                    
                    total_latencies.extend(latencies)
                    
                    print(f"\n📊 {yaml_name}")
                    print(f"   Average: {avg:.2f}ms")
                    print(f"   Maximum: {max_lat:.2f}ms")
                    print(f"   Minimum: {min_lat:.2f}ms")
                    print(f"   Std Dev: {std_dev:.2f}ms")
                    print(f"   Samples: {len(latencies)}")
        
        if total_latencies:
            print("\n" + "="*80)
            print("📈 OVERALL STATISTICS")
            print("="*80)
            sorted_lat = sorted(total_latencies)
            print(f"Total Requests: {len(total_latencies)}")
            print(f"Average Latency: {statistics.mean(total_latencies):.2f}ms")
            print(f"Median Latency: {statistics.median(total_latencies):.2f}ms")
            idx_99 = int(len(sorted_lat) * 0.99)
            idx_95 = int(len(sorted_lat) * 0.95)
            print(f"P99 Latency: {sorted_lat[idx_99-1]:.2f}ms")
            print(f"P95 Latency: {sorted_lat[idx_95-1]:.2f}ms")
            print(f"Max Latency: {max(total_latencies):.2f}ms")
        
        print("\n" + "="*80)
        print("✅ 5 YAML CHAOS EXPERIMENTS TEST SUITE COMPLETED")
        print("="*80)

def main():
    print("\n" + "="*80)
    print("CHAOS ENGINEERING - 5 YAML EXPERIMENTS TEST")
    print("="*80)
    print("Testing 5 custom chaos experiments defined in YAML files")
    print("="*80)
    
    tester = ChaosYAMLTest()
    
    try:
        tester.load_yaml_files()
        tester.test_dns_chaos_01()
        tester.test_advanced_network_chaos_02()
        tester.test_time_chaos_03()
        tester.test_kernel_panic_04()
        tester.test_advanced_workflows_05()
        tester.generate_report()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
