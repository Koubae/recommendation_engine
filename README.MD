Recommendation Engine
=====================

_Recommendation Engine is a Python API with MongoDB_

### QuickStart

#### Prerequisites

- [uv](https://docs.astral.sh/uv/guides/install-python/) (Installed by Make command `init-venv` if not present)
- `python3.13` | I suggest to use [pyenv](https://github.com/pyenv/pyenv) and then install python via
  `pyenv install 3.13` Command
- Linux/macOS or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) on Windows
- [GNU Make](https://www.gnu.org/software/make/)

```bash
make quickstart
```

Go to http://127.0.0.1:8000

### Run locally

To run the app locally, use this command:

```bash
make run
```

Development
-----------

### Code quality

Run

```bash
make quality-checks 
```

### Tests

There are available the following commands:

```bash
# unit
make test-unit
# integration
make test-integration
# All tests
make tests

# Unit with HTML coverage
make test-unit-coverage
```
