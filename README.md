[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name:

surname:

group:

## How to start the app


## How to execute tests

### Unit Tests
```bash
python -m pytest tests/unit/ -v
```

### API Tests (requires Flask running)
```bash
# Start Flask
export FLASK_APP=src/api.py
flask run

# In another terminal
python -m pytest tests/unit/test_transfer_api.py -v
```

### Performance Tests (requires Flask running)
```bash
# Start Flask
export FLASK_APP=src/api.py
flask run

# In another terminal
python -m pytest tests/perf/ -v
```

### All tests with coverage
```bash
python -m coverage run --source=src -m pytest
python -m coverage report
```