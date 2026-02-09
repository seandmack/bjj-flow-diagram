# BJJ Flow Diagram Testing Framework

Automated testing framework using pytest and Playwright for the BJJ Flow Diagram application.

## Directory Structure

```
bjj-flow-diagram/
├── index.html              # Your BJJ Flow Diagram
├── armbar-mount.gif        # Demo GIF
├── README.md               # Project README
└── tests/                  # Test framework (this directory)
    ├── conftest.py         # Shared fixtures
    ├── pytest.ini          # Pytest config
    ├── requirements.txt    # Dependencies
    ├── setup_tests.sh      # Setup script (Mac/Linux)
    ├── setup_tests.bat     # Setup script (Windows)
    ├── setup_tests.py      # Setup script (Universal)
    ├── test_smoke.py       # Smoke tests
    ├── test_counters.py    # Counter tests
    ├── test_interactions.py # Interaction tests
    └── TEST_README.md      # This file
```

## Setup

### In GitHub Codespaces (or Linux/Mac)

```bash
cd tests
chmod +x setup_tests.sh
./setup_tests.sh
```

### On Windows

```cmd
cd tests
setup_tests.bat
```

### Universal (Any Platform)

```bash
cd tests
python setup_tests.py
```

### Quick Setup (All Platforms)

**Option 1: Using Python script (Recommended)**
```bash
python setup_tests.py
```

**Option 2: Platform-specific scripts**

**Windows:**
```cmd
setup_tests.bat
```

**Mac/Linux:**
```bash
chmod +x setup_tests.sh
./setup_tests.sh
```

### Manual Setup

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

**Mac/Linux (Terminal):**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
playwright install chromium
```

## Running Tests

### Start Local Server (Required)

**From the repository root directory** (not from tests/):

```bash
# Terminal 1 - start from repository root
python3 -m http.server 8000
```

Keep this running while tests execute.

### Run Tests

**From the tests/ directory:**

```bash
# Terminal 2 - navigate to tests directory
cd tests

# Activate virtual environment
source venv/bin/activate  # Mac/Linux/Codespaces
# OR
venv\Scripts\activate     # Windows

# Run tests
pytest -m smoke          # Quick smoke tests
pytest test_counters.py  # Counter tests
pytest                   # All tests
```

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Run only smoke tests
pytest test_smoke.py

# Run only counter tests
pytest test_counters.py

# Run only interaction tests
pytest test_interactions.py
```

### Run Tests by Marker

```bash
# Run only smoke tests (quick validation)
pytest -m smoke

# Run only visual tests (layout and positioning)
pytest -m visual

# Run only interaction tests (user actions)
pytest -m interaction

# Run all except slow tests
pytest -m "not slow"
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test

```bash
pytest test_counters.py::test_armbar_counters_exist
```

## Test Reports

After running tests, view the HTML report:

```bash
open test-reports/report.html
```

Screenshots of failed tests are saved to `test-reports/screenshots/`

## Test Structure

```
.
├── conftest.py              # Shared fixtures and helpers
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Python dependencies
├── test_smoke.py           # Basic smoke tests
├── test_counters.py        # Counter-specific tests
└── test_interactions.py    # User interaction tests
```

## Writing New Tests

### Basic Test Template

```python
import pytest
from conftest import wait_for_diagram_ready

@pytest.mark.visual
def test_my_feature(page):
    """Test description."""
    wait_for_diagram_ready(page)
    
    # Your test logic here
    assert page.is_visible('selector')
```

### Using Fixtures

- `browser` - Session-scoped browser instance
- `page` - Function-scoped page for each test
- `screenshot_on_failure` - Auto-capture screenshots on failures

### Helper Functions

Available in `conftest.py`:

- `wait_for_diagram_ready(page)` - Wait for diagram to load
- `get_element_position(page, selector)` - Get element bounding box
- `check_overlap(box1, box2)` - Check if two boxes overlap

## Test Markers

- `@pytest.mark.smoke` - Quick validation tests
- `@pytest.mark.visual` - Layout and visual tests
- `@pytest.mark.interaction` - User interaction tests
- `@pytest.mark.slow` - Longer-running tests

## Configuration

### Change Base URL

Edit `conftest.py`:

```python
BASE_URL = "http://localhost:8000/bjj-flow-diagram.html"
```

### See Browser During Tests

Edit `conftest.py`:

```python
browser = p.chromium.launch(
    headless=False,  # Change to False
    slow_mo=500      # Slow down actions
)
```

## Continuous Integration

To run tests in CI/CD:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: playwright install chromium
      - run: python3 -m http.server 8000 &
      - run: pytest
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-reports
          path: test-reports/
```

## Troubleshooting

### "Connection refused" Error

Make sure the local server is running:
```bash
python3 -m http.server 8000
```

### Tests Timeout

Increase timeout in `conftest.py`:
```python
page.set_default_timeout(10000)  # 10 seconds
```

### Can't Find Elements

Add waits:
```python
page.wait_for_selector('.my-element', timeout=5000)
```

## Tips

1. **Run smoke tests first** to catch major issues quickly
2. **Use `-v` flag** for detailed output
3. **Check screenshots** in test-reports/screenshots/ when tests fail
4. **Run specific tests** during development to save time
5. **Use markers** to organize test runs

## Next Steps

- Add visual regression testing with screenshot comparison
- Add performance tests (load time, interaction speed)
- Add accessibility tests (ARIA labels, keyboard navigation)
- Integrate with CI/CD pipeline
