# Testing

Guide to running and writing tests for ghdesk.

---

## Running Tests

### Full Test Suite

```bash
python -m pytest tests/ -v -W default --tb=short
```

**Requirements:**

- All tests must pass
- Zero warnings

### Quick Run

```bash
pytest tests/ -q
```

### Specific Test File

```bash
pytest tests/test_git_operations.py -v
```

### Specific Test

```bash
pytest tests/test_git_operations.py::TestGitRepositoryBasic::test_name_from_path -v
```

---

## Test Structure

### Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_git_operations.py   # GitRepository tests
└── test_logging_config.py   # Logging tests
```

### Naming Conventions

- Test files: `test_<module>.py`
- Test classes: `Test<Feature>`
- Test methods: `test_<method>_<scenario>_<expected>`

Example:
```python
class TestGitRepositoryBasic:
    def test_name_from_path(self, git_repo):
        assert git_repo.name == "test_repo"

    def test_current_branch_default(self, git_repo):
        assert git_repo.current_branch == "main"
```

---

## Writing Tests

### Test Structure (AAA Pattern)

```python
def test_get_modified_files_returns_list(self, git_repo, tmp_path):
    # Arrange
    test_file = tmp_path / "test_repo" / "new_file.txt"
    test_file.write_text("content")

    # Act
    modified = git_repo.get_modified_files()

    # Assert
    assert isinstance(modified, list)
```

### Using Fixtures

Fixtures provide reusable test setup in `conftest.py`:

```python
@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary git repository for testing."""
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    
    repo = git.Repo.init(repo_path)
    
    # Configure git
    with repo.config_writer() as config:
        config.set_value("user", "email", "test@test.com")
        config.set_value("user", "name", "Test User")
    
    # Initial commit
    readme = repo_path / "README.md"
    readme.write_text("# Test Repo")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    
    git_repository = GitRepository(str(repo_path))
    
    yield git_repository
    
    # Cleanup
    git_repository.close()
```

### Fixture Cleanup

Always clean up resources:

```python
yield git_repository

# Teardown - close to avoid ResourceWarnings
git_repository.close()
```

---

## Test Categories

### Unit Tests

Test individual functions/methods in isolation:

```python
class TestGitRepositoryStatus:
    def test_is_dirty_false_when_clean(self, git_repo):
        assert git_repo.is_dirty is False

    def test_is_dirty_true_with_changes(self, git_repo, tmp_path):
        test_file = tmp_path / "test_repo" / "new.txt"
        test_file.write_text("content")
        assert git_repo.is_dirty is True
```

### Integration Tests

Test component interactions:

```python
def test_load_repo_details_integration(tmp_path):
    """Test that load_repo_details combines git and gh data."""
    # Setup git repo
    # Mock GHWrapper
    # Call load_repo_details
    # Verify combined result
```

---

## Mocking

### Mocking External Commands

For `GHWrapper` tests, mock `subprocess.run`:

```python
from unittest.mock import patch, MagicMock

def test_is_authenticated_true(self):
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Logged in to github.com"
        )
        # ... test code
```

### Mocking Git Operations

For UI tests, mock the `GitRepository`:

```python
def test_repo_detail_loads_data(self, mocker):
    mock_git_repo = mocker.Mock()
    mock_git_repo.current_branch = "main"
    mock_git_repo.is_dirty = False
    # ... use mock in test
```

---

## Test Data

### Temporary Files

Use `tmp_path` fixture for file operations:

```python
def test_with_files(self, tmp_path):
    test_file = tmp_path / "data.txt"
    test_file.write_text("content")
    # ... test code
```

### Test Repositories

Create minimal git repos for testing:

```python
def create_test_repo(path):
    """Create a minimal valid git repository."""
    repo = git.Repo.init(path)
    (path / "README.md").write_text("# Test")
    repo.index.add(["README.md"])
    repo.index.commit("Initial commit")
    return repo
```

---

## Coverage

### Running with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=core --cov=ui --cov-report=html
```

### Coverage Goals

| Layer | Target |
|-------|--------|
| Core | 80%+ |
| UI | 50%+ (harder to unit test) |

---

## Continuous Integration

Tests run automatically on:

- Every push
- Every pull request

CI configuration ensures:

- Tests pass on Python 3.8+
- No warnings
- Pylint score meets threshold

---

## Debugging Tests

### Verbose Output

```bash
pytest tests/ -v --tb=long
```

### Print Statements

```bash
pytest tests/ -s  # Shows print statements
```

### Drop into Debugger

```python
def test_something(self):
    import pdb; pdb.set_trace()
    # ... test code
```

Or with pytest:

```bash
pytest tests/ --pdb  # Drops into debugger on failure
```

---

## Common Test Patterns

### Testing Exceptions

```python
def test_invalid_repo_raises(self, tmp_path):
    with pytest.raises(git.InvalidGitRepositoryError):
        GitRepository(str(tmp_path / "not_a_repo"))
```

### Testing Return Types

```python
def test_get_branches_returns_list(self, git_repo):
    branches = git_repo.branches
    assert isinstance(branches, list)
    assert all(isinstance(b, str) for b in branches)
```

### Parameterized Tests

```python
@pytest.mark.parametrize("visibility,expected", [
    ("public", "public"),
    ("private", "private"),
])
def test_visibility_options(self, visibility, expected):
    # ... test code
```
