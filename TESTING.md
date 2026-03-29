# Testing Guide - Condominium Management Agent

## Overview

The test suite provides comprehensive coverage of Phase 1 components with unit and integration tests using pytest, mocks, and fixtures.

## Test Structure

```
tests/
├── __init__.py              # Test package
├── conftest.py              # Shared fixtures and configuration
├── test_config.py           # Configuration tests
├── test_gmail_tools.py      # Gmail API integration tests
├── test_sheets_tools.py     # Google Sheets integration tests
├── test_mcp_servers.py      # MCP server tests
└── test_agent.py            # Agent orchestration tests
```

## Running Tests

### Quick Start

**Linux/macOS:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

**Windows:**
```bash
run_tests.bat
```

### Manual Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=html

# Run specific test file
pytest tests/test_config.py -v

# Run specific test class
pytest tests/test_gmail_tools.py::TestGmailClient -v

# Run specific test
pytest tests/test_config.py::TestSettings::test_settings_load_from_env -v
```

## Test Coverage

### Configuration Tests (`test_config.py`)

Tests the `Settings` class:
- ✅ Load environment variables
- ✅ Sheet ID configuration
- ✅ API key validation
- ✅ File path handling
- ✅ Default values
- ✅ Required field validation

**Example:**
```bash
pytest tests/test_config.py -v
```

### Gmail Tools Tests (`test_gmail_tools.py`)

Tests the `GmailClient` class:
- ✅ OAuth authentication flow
- ✅ Send email (plain, HTML, with CC/BCC)
- ✅ Read emails (with filters)
- ✅ Reply to emails in threads
- ✅ Mark emails as read
- ✅ Error handling

**Example:**
```bash
pytest tests/test_gmail_tools.py::TestGmailClient::test_send_email -v
```

### Sheets Tools Tests (`test_sheets_tools.py`)

Tests the `SheetsClient` class:
- ✅ Read sheet data (full or range)
- ✅ Write sheet data
- ✅ Append rows
- ✅ Get residents list
- ✅ Get overdue quotas
- ✅ Log incidents
- ✅ Query incidents with filters

**Example:**
```bash
pytest tests/test_sheets_tools.py::TestSheetsClient::test_get_residents -v
```

### MCP Server Tests (`test_mcp_servers.py`)

Tests both MCP servers:
- ✅ Server initialization
- ✅ Tool discovery
- ✅ Tool execution
- ✅ Result formatting (JSON)
- ✅ Error handling
- ✅ Unknown tool handling

**Example:**
```bash
pytest tests/test_mcp_servers.py::TestGmailMCPServer -v
```

### Agent Tests (`test_agent.py`)

Tests the main `CondominiumAgent` class:
- ✅ Agent initialization
- ✅ Tool conversion for API
- ✅ Tool call processing (Gmail)
- ✅ Tool call processing (Sheets)
- ✅ Unknown tool handling

**Example:**
```bash
pytest tests/test_agent.py::TestCondominiumAgent::test_agent_initialization -v
```

## Fixtures (conftest.py)

Pre-built test data and mocks:

### `temp_env_file`
Creates a temporary `.env` file for testing.

```python
def test_something(temp_env_file):
    # File has all required environment variables
    assert temp_env_file.exists()
```

### `test_settings`
Provides a `Settings` instance with test values.

```python
def test_config(test_settings):
    assert test_settings.anthropic_api_key == "test-key-12345"
```

### `mock_gmail_service`
Mocked Gmail API service with realistic responses.

```python
def test_email(mock_gmail_service):
    # Service already configured with expected responses
    gmail.service = mock_gmail_service
```

### `mock_sheets_service`
Mocked Google Sheets API service.

```python
def test_sheet(mock_sheets_service):
    sheets.service = mock_sheets_service
```

### Sample Data Fixtures

- `sample_email`: Example email object
- `sample_residents`: List of resident records
- `sample_overdue_quotas`: Overdue quota examples
- `sample_incidents`: Incident examples

## Coverage Reports

After running tests with coverage, open the HTML report:

```bash
# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=html

# Open report (macOS)
open htmlcov/index.html

# Open report (Linux)
xdg-open htmlcov/index.html

# Open report (Windows)
start htmlcov\index.html
```

## Mocking Strategy

Tests use `unittest.mock` to mock external dependencies:

### Mocking Google APIs

```python
from unittest.mock import patch, MagicMock

@patch("src.tools.gmail_tools.discovery.build")
def test_gmail(mock_build):
    mock_service = MagicMock()
    mock_build.return_value = mock_service

    # Test code here
```

### Mocking Authentication

```python
@patch("os.path.exists", return_value=False)
@patch("builtins.open", create=True)
@patch("pickle.dump")
def test_auth(mock_dump, mock_open, mock_exists):
    # Test code here
```

## Test Markers

Mark tests for organization:

```python
@pytest.mark.unit
def test_configuration():
    pass

@pytest.mark.integration
def test_agent_with_apis():
    pass

@pytest.mark.slow
def test_long_operation():
    pass
```

Run tests by marker:

```bash
pytest -m unit          # Run only unit tests
pytest -m integration   # Run only integration tests
pytest -m "not slow"    # Run all except slow tests
```

## CI/CD Integration

To run tests in CI/CD pipeline:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest tests/ -v --cov=src --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
```

## Common Issues

### Import Errors
```
ModuleNotFoundError: No module named 'src'
```
**Solution:** Ensure you're running from project root and `src/` directory exists.

### Credential Errors
Tests mock authentication, so no real credentials needed. If you see credential errors:
```bash
# Make sure mock patches are applied
@patch("src.tools.gmail_tools.discovery.build")
```

### Settings Not Loading
```
pydantic_core._pydantic_core.ValidationError
```
**Solution:** Check `temp_env_file` fixture has all required variables in `conftest.py`.

## Adding New Tests

1. **Create test file:** `tests/test_new_feature.py`
2. **Import fixtures:** `from tests.conftest import ...`
3. **Write test class:** `class TestNewFeature:`
4. **Run tests:** `pytest tests/test_new_feature.py -v`

Example:

```python
# tests/test_new_feature.py
import pytest
from src.new_module import NewClass

class TestNewClass:
    def test_initialization(self, test_settings):
        obj = NewClass(test_settings)
        assert obj is not None

    def test_method(self, mock_gmail_service):
        # Test code
        pass
```

## Best Practices

1. **Isolate Tests:** Use fixtures instead of shared state
2. **Mock External APIs:** Never call real Google APIs in tests
3. **Test Edge Cases:** Empty data, errors, invalid inputs
4. **Clear Names:** Use descriptive test names
5. **One Assertion:** Keep tests focused
6. **DRY Fixtures:** Share common setup in conftest.py

## Performance

- Unit tests: < 100ms each
- Full suite: < 5 seconds
- With coverage report: < 10 seconds

## Next Steps

- Add integration tests with real APIs (when credentials available)
- Add performance/load tests
- Add security tests (credential handling)
- Add E2E tests for complete workflows
