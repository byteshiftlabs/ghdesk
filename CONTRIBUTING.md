# Contributing to ghdesk

Thank you for considering contributing to ghdesk!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ghdesk.git
   cd ghdesk
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure GitHub CLI is installed and authenticated:
   ```bash
   gh auth login
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints where practical
- Keep modules under 500 lines
- Run pylint before submitting (minimum score: 9.0)

```bash
python -m pylint **/*.py
```

## Testing

Run the test suite before submitting changes:

```bash
python -m pytest tests/ -v -W default --tb=short
```

All tests must pass with zero warnings.

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear, descriptive commits
3. Ensure all tests pass and pylint score is acceptable
4. Update documentation if needed
5. Submit a pull request with a clear description of changes

## Project Structure

```
ghdesk/
├── main.py              # Application entry point
├── core/                # Business logic (no UI dependencies)
│   ├── gh_wrapper.py    # GitHub CLI wrapper
│   ├── git_operations.py
│   └── github/          # GitHub API modules
├── ui/                  # PyQt6 interface layer
│   ├── main_window.py
│   └── themes/          # Color themes
└── tests/               # Test suite
```

## Reporting Issues

When reporting bugs, please include:
- Operating system and version
- Python version
- Steps to reproduce
- Expected vs actual behavior

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
