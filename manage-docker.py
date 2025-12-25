#!/usr/bin/env python3
"""
Chaos Engineering Docker Setup & Startup Script
Automated Docker Compose management for chaos testing
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

class ChaosDockerManager:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.docker_compose_file = self.project_dir / "docker-compose.yml"
    
    def run_command(self, cmd, description=""):
        """Run shell command"""
        try:
            if description:
                print(f"\n▶ {description}")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Error: {result.stderr}")
                return False
            if result.stdout:
                print(result.stdout)
            return True
        except Exception as e:
            print(f"❌ Exception: {e}")
            return False
    
    def check_docker(self):
        """Verify Docker is installed and running"""
        print("\n📦 Checking Docker Installation...")
        result = subprocess.run("docker --version", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker is not installed or not in PATH")
            return False
        print(f"✓ {result.stdout.strip()}")
        return True
    
    def check_docker_compose(self):
        """Verify Docker Compose is installed"""
        print("\n📦 Checking Docker Compose Installation...")
        result = subprocess.run("docker-compose --version", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker Compose is not installed")
            return False
        print(f"✓ {result.stdout.strip()}")
        return True
    
    def check_ports(self):
        """Check if required ports are available"""
        print("\n🔌 Checking Port Availability...")
        
        ports = {5000: "Frontend", 5001: "Backend"}
        available = True
        
        for port, service in ports.items():
            try:
                result = subprocess.run(
                    f'netstat -ano | findstr ":{port}"',
                    shell=True,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"⚠️  Port {port} ({service}) appears to be in use")
                    available = False
                else:
                    print(f"✓ Port {port} ({service}) available")
            except:
                print(f"✓ Port {port} ({service}) available")
        
        return available
    
    def build_images(self):
        """Build Docker images"""
        print("\n🔨 Building Docker Images...")
        return self.run_command(
            "docker-compose build",
            "Building frontend and backend images..."
        )
    
    def start_containers(self):
        """Start Docker containers"""
        print("\n🚀 Starting Docker Containers...")
        return self.run_command(
            "docker-compose up -d",
            "Starting services with docker-compose..."
        )
    
    def wait_for_services(self, timeout=30):
        """Wait for services to be healthy"""
        print(f"\n⏳ Waiting for services to be healthy (timeout: {timeout}s)...")
        
        endpoints = [
            ("http://localhost:5000/health", "Frontend"),
            ("http://localhost:5001/health", "Backend"),
        ]
        
        start_time = time.time()
        all_healthy = False
        
        while time.time() - start_time < timeout:
            all_healthy = True
            for url, name in endpoints:
                try:
                    resp = requests.get(url, timeout=2)
                    if resp.status_code == 200:
                        print(f"  ✓ {name} healthy")
                    else:
                        print(f"  ⏳ {name} not ready (status: {resp.status_code})")
                        all_healthy = False
                except:
                    print(f"  ⏳ {name} not responding yet...")
                    all_healthy = False
            
            if all_healthy:
                print("\n✅ All services are healthy!")
                return True
            
            time.sleep(2)
        
        print("\n⚠️  Services did not become healthy in time")
        return False
    
    def check_container_status(self):
        """Check container status"""
        print("\n📊 Container Status:")
        return self.run_command(
            "docker-compose ps",
            "Getting container status..."
        )
    
    def show_logs(self):
        """Show recent container logs"""
        print("\n📋 Container Logs (Last 10 lines):")
        self.run_command("docker-compose logs --tail=10")
    
    def run_tests(self):
        """Run chaos engineering tests"""
        print("\n🧪 Running Chaos Engineering Tests...")
        return self.run_command(
            f"python {self.project_dir / 'test-docker-chaos.py'}",
            "Running comprehensive chaos test suite..."
        )
    
    def run_monitoring(self):
        """Run Docker monitoring"""
        print("\n📈 Running Docker Monitoring...")
        return self.run_command(
            f"python {self.project_dir / 'monitor-docker.py'}",
            "Collecting Docker metrics..."
        )
    
    def interactive_menu(self):
        """Interactive menu"""
        while True:
            print("\n" + "=" * 70)
            print("CHAOS ENGINEERING - DOCKER MANAGEMENT")
            print("=" * 70)
            print("\n1. Check Prerequisites (Docker, ports)")
            print("2. Build Docker Images")
            print("3. Start Containers")
            print("4. Stop Containers")
            print("5. View Container Status")
            print("6. View Container Logs")
            print("7. Run Chaos Tests")
            print("8. Run Docker Monitoring")
            print("9. Full Setup (Build + Start + Tests)")
            print("0. Exit")
            print("-" * 70)
            
            choice = input("\nSelect option (0-9): ").strip()
            
            if choice == "1":
                self.check_docker()
                self.check_docker_compose()
                self.check_ports()
            elif choice == "2":
                self.build_images()
            elif choice == "3":
                if self.start_containers():
                    self.wait_for_services()
            elif choice == "4":
                self.run_command("docker-compose down", "Stopping containers...")
            elif choice == "5":
                self.check_container_status()
            elif choice == "6":
                self.show_logs()
            elif choice == "7":
                self.run_tests()
            elif choice == "8":
                self.run_monitoring()
            elif choice == "9":
                self.check_docker()
                self.check_docker_compose()
                self.check_ports()
                if self.build_images():
                    if self.start_containers():
                        if self.wait_for_services():
                            self.run_tests()
                            self.run_monitoring()
            elif choice == "0":
                print("\n👋 Goodbye!")
                break
            else:
                print("\n⚠️  Invalid option")

def main():
    manager = ChaosDockerManager()
    
    # Check if running with arguments
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "start":
            print("🚀 Quick start sequence...\n")
            if manager.check_docker() and manager.check_docker_compose():
                if manager.start_containers():
                    manager.wait_for_services()
                    manager.run_tests()
        
        elif command == "stop":
            print("⛔ Stopping containers...\n")
            manager.run_command("docker-compose down", "Stopping services...")
        
        elif command == "test":
            print("🧪 Running tests...\n")
            manager.run_tests()
        
        elif command == "monitor":
            print("📈 Monitoring...\n")
            manager.run_monitoring()
        
        elif command == "build":
            print("🔨 Building...\n")
            manager.build_images()
        
        elif command == "status":
            print("📊 Status...\n")
            manager.check_container_status()
        
        elif command == "logs":
            print("📋 Logs...\n")
            manager.show_logs()
        
        elif command == "help":
            print("""
Usage: python manage-docker.py [COMMAND]

Commands:
  start      - Start containers and run tests
  stop       - Stop containers
  build      - Build Docker images
  status     - Show container status
  logs       - Show container logs
  test       - Run chaos tests
  monitor    - Run Docker monitoring
  help       - Show this help message
  (none)     - Interactive menu

Examples:
  python manage-docker.py start
  python manage-docker.py test
  python manage-docker.py
""")
        else:
            print(f"❌ Unknown command: {command}\nUse 'python manage-docker.py help'")
    else:
        # Interactive mode
        manager.interactive_menu()

if __name__ == "__main__":
    main()
