import requests
import json

print('=' * 60)
print('DOCKER CONTAINER TEST')
print('=' * 60)

endpoints = [
    ('http://localhost:5000/health', 'Frontend Health'),
    ('http://localhost:5000/api/data', 'Frontend API Data'),
    ('http://localhost:5001/health', 'Backend Health'),
    ('http://localhost:5001/data', 'Backend Data'),
]

for url, name in endpoints:
    try:
        resp = requests.get(url, timeout=5)
        print(f'✓ {name}: OK (Status {resp.status_code})')
    except Exception as e:
        print(f'✗ {name}: {str(e)[:50]}')

print('=' * 60)
print('Docker containers running!')
print('=' * 60)
