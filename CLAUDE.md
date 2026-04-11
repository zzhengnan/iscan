# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**iscan** is a Python CLI tool and library that scans a Python project's source files and reports all third-party packages and standard library modules found in import statements, along with their occurrence counts. It has no external runtime dependencies — it uses only the stdlib `ast` module for parsing.

## Commands

**Run tests:**
```bash
pytest -vvv
```

**Run a single test:**
```bash
pytest iscan/tests/test_scan.py::test_function_name -vvv
```

**Type checking:**
```bash
mypy ./iscan/
```

**Linting:**
```bash
flake8
isort --check-only .
```

**Install with all dev dependencies:**
```bash
pip install .['dev']
```

**Pre-commit hooks (flake8 + isort):**
```bash
pre-commit run --all-files
```

## Architecture

The package has two core modules:

### `iscan/scan.py`
The main scanning pipeline:
1. `cli()` / `main()` — CLI entry point, parses args
2. `run()` — public API function, orchestrates the full scan
3. `scan_directory()` — walks a directory, parses each `.py` file's AST, returns a flat list of raw import names
4. `ImportScanner` — `ast.NodeVisitor` subclass that handles `import X` and `from X import Y` (skips relative imports)
5. `get_base_name()` — strips submodule paths (e.g. `os.path` → `os`)
6. `separate_third_party_from_std_lib()` (from `std_lib.py`) — splits results into two buckets
7. `sort_counter()` / `show_result()` — sorting and display

### `iscan/std_lib.py`
Contains `STD_LIB_BY_VERSION` — a hardcoded dict of stdlib module names keyed by Python version string (2.7 through 3.13). `STD_LIB` is the union of all versions. `get_std_lib()` is a utility (requires optional deps) for scraping the Python docs to regenerate these lists.

### Test structure
- `iscan/tests/test_package/` — a small fake Python project used as a scan fixture
- `iscan/tests/test_modules/` — individual `.py` files covering different import scenarios (absolute, relative, mixed)
- Tests use `pytest.mark.parametrize` heavily

## Configuration

- **flake8**: max line length 120, ignores `F401` (unused imports in `__init__.py`)
- **isort**: configured in `setup.cfg`
- **mypy**: runs on `./iscan/` directory; strict type hints are expected throughout
- **CI**: GitHub Actions runs mypy + pytest on Python 3.10–3.14 (`.github/workflows/run-tests.yml`)
