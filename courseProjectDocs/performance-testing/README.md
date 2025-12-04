# Performance Testing

## Spike Test Commands

### Install Locust
```bash
pip install locust
```

### Run Tests

Terminal 1 - Start MkDocs server:
```bash
hatch run docs:serve
```

Terminal 2 - Start Locust:
```bash
cd courseProjectCode/performance-testing
locust -f locustfile.py --host=http://127.0.0.1:8000
```

Open http://localhost:8089 for the Locust web UI.

### Spike Test Steps

1. Start with 25 users, spawn rate 25
2. Wait 30 seconds
3. Click "Edit" → change to 125 users, spawn rate 125
4. Wait 60 seconds
5. Click "Edit" → change back to 25
