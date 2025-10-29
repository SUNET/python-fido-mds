# Development Guide

This document provides comprehensive guidance for developing python-fido-mds.

## Table of Contents

- [Setup](#setup)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Architecture](#architecture)
- [Contributing](#contributing)
- [LLM Development Guidelines](#llm-development-guidelines)

## Setup

### Prerequisites

- Python 3.13.3 or later
- `uv` package manager (recommended) or `pip`
- Git

### Initial Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd python-fido-mds
```

2. Create and activate virtual environment:
```bash
# The project uses a dedicated virtualenv
python3 -m venv /home/lundberg/python-environments/python-fido-mds
source /home/lundberg/python-environments/python-fido-mds/bin/activate
```

3. Install dependencies:
```bash
# Install development dependencies
make dev_sync_deps

# Or manually with pip
pip install -r test_requirements.txt
```

### Project Structure

```
python-fido-mds/
├── src/
│   └── fido_mds/
│       ├── models/          # Data models (Pydantic)
│       │   ├── attestation.py    # Attestation format implementations
│       │   ├── fido_mds.py       # FIDO MDS models
│       │   └── webauthn.py       # WebAuthn models
│       ├── data/            # Bundled metadata
│       ├── tests/           # Test suite
│       │   ├── data.py           # Test data (attestation objects)
│       │   └── test_*.py         # Test modules
│       ├── helpers.py       # Utility functions
│       └── metadata_store.py     # Main API
├── scripts/             # Utility scripts
├── requirements.txt     # Runtime dependencies
├── test_requirements.txt # Development dependencies
├── Makefile            # Common development tasks
└── pyproject.toml      # Project metadata
```

## Development Workflow

### Essential Commands

Always activate the virtualenv first:
```bash
source /home/lundberg/python-environments/python-fido-mds/bin/activate
```

Then use these make targets:

```bash
# Run all quality checks (recommended before committing)
make reformat && make typecheck && make test

# Individual commands
make reformat    # Format code with ruff
make typecheck   # Type check with mypy
make test        # Run test suite with pytest
make build       # Build distribution packages
```

### Typical Development Cycle

1. **Make changes** to code in `src/fido_mds/`
2. **Run tests** frequently: `make test`
3. **Check types** before committing: `make typecheck`
4. **Format code** before committing: `make reformat`
5. **Commit** with descriptive message

### Adding New Features

1. **Write tests first** in `src/fido_mds/tests/`
2. **Implement feature** in appropriate module
3. **Update models** if data structures change
4. **Run all checks**: `make reformat && make typecheck && make test`
5. **Update documentation** as needed

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest src/fido_mds/tests/test_verify.py

# Run specific test
pytest src/fido_mds/tests/test_verify.py::test_verify

# Run with verbose output
pytest src/fido_mds/tests/ -v

# Run with coverage
pytest src/fido_mds/tests/ --cov=fido_mds
```

### Test Data

Test data (attestation objects) are stored in `src/fido_mds/tests/data.py`:

- Real attestation objects from various authenticators
- Base64-encoded attestation objects and client data
- Organized by device type (YubiKey, iPhone, Android, etc.)

When adding new test data:
1. Ensure it's from a real, valid attestation
2. Document the source and device
3. Add corresponding test case
4. Verify it works with `make test`

## Code Quality

### Type Checking

The project uses mypy for static type checking:

```bash
make typecheck
```

All code must:
- Have type hints for function parameters and return values
- Pass mypy checks without errors
- Use appropriate type imports from `typing`

### Code Formatting

The project uses ruff for formatting and linting:

```bash
make reformat
```

Ruff will:
- Sort and organize imports
- Remove unused imports
- Format code according to project standards
- Check for common issues

### Code Style Guidelines

- **Follow PEP 8** (enforced by ruff)
- **Type hints required** for all functions
- **Docstrings required** for public APIs
- **Comments** for complex logic only
- **Error handling** - use specific exceptions
- **Logging** - use module-level logger

Example:
```python
from logging import getLogger
from typing import Optional

logger = getLogger(__name__)

def process_attestation(data: bytes, format: str) -> Optional[dict]:
    """
    Process an attestation object.
    
    Args:
        data: Raw attestation bytes
        format: Attestation format identifier
        
    Returns:
        Parsed attestation dict or None if invalid
        
    Raises:
        InvalidData: If data is malformed
    """
    try:
        # Implementation
        pass
    except ValueError as e:
        logger.error(f"Failed to process attestation: {e}")
        raise InvalidData(f"Invalid attestation data: {e}")
```

## Architecture

### Key Components

#### FidoMetadataStore

Main entry point for attestation verification:

```python
from fido_mds import FidoMetadataStore

mds = FidoMetadataStore()
mds.verify_attestation(attestation, client_data)
```

#### Attestation Implementations

Located in `src/fido_mds/models/attestation.py`:

- `AndroidKeyAttestation` - Android Key attestation format
- Other formats use `fido2` library implementations

Each implementation:
1. Verifies signature
2. Validates public keys
3. Checks certificate extensions
4. Returns `AttestationResult`

#### Models

Using Pydantic for data validation:

- `FidoMD` - FIDO Metadata Service structure
- `MetadataEntry` - Individual authenticator metadata
- `Attestation` - WebAuthn attestation object
- `AttestationStatement` - Attestation statement data

### Design Patterns

- **Strategy Pattern** - Different attestation formats
- **Factory Pattern** - Attestation format selection
- **Validation** - Pydantic models for data validation
- **Separation of Concerns** - Models, verification, helpers

## Contributing

### Pull Request Process

1. Create feature branch from `main`
2. Make changes with tests
3. Run all quality checks
4. Commit with clear messages
5. Push and create pull request
6. Ensure CI passes

### Commit Messages

Follow conventional commits:

```
feat: add support for new attestation format
fix: correct signature verification in Android Key
docs: update development guide
test: add test cases for edge conditions
refactor: extract KeyDescription parsing to method
```

## LLM Development Guidelines

> **Special Section for LLM Assistants**
>
> This section provides specific guidelines for LLM-assisted development on this project.

### Environment Setup for LLMs

**Always use the correct virtualenv:**

```bash
source /home/lundberg/python-environments/python-fido-mds/bin/activate
```

**Verify environment before starting:**
```bash
which python  # Should show: /home/lundberg/python-environments/python-fido-mds/bin/python
python --version  # Should show: Python 3.13.3
```

### Required Workflow for LLMs

**MANDATORY:** After completing ANY code changes, run:

```bash
cd /home/lundberg/projects/python-fido-mds && \
source /home/lundberg/python-environments/python-fido-mds/bin/activate && \
make reformat && make typecheck && make test
```

This ensures:
- ✅ Code is properly formatted
- ✅ Type checking passes
- ✅ All tests pass
- ✅ No regressions introduced

### Code Modification Patterns

When modifying code, follow these patterns:

#### Pattern 1: Adding New Feature

```bash
# 1. View existing code
view src/fido_mds/models/attestation.py

# 2. Make changes with str_replace
str_replace path="..." old_str="..." new_str="..."

# 3. Run quality checks
make reformat && make typecheck && make test

# 4. Verify specific tests
pytest src/fido_mds/tests/test_verify.py -v
```

#### Pattern 2: Fixing Issues

```bash
# 1. Identify issue
pytest src/fido_mds/tests/test_verify.py -v

# 2. View problematic code
view src/fido_mds/models/attestation.py 100 120

# 3. Fix with surgical str_replace
str_replace path="..." old_str="..." new_str="..."

# 4. Verify fix
make test
```

#### Pattern 3: Refactoring

```bash
# 1. Run tests to establish baseline
make test

# 2. Make refactoring changes
str_replace ...

# 3. Verify behavior unchanged
make test

# 4. Check types still pass
make typecheck
```

### Common LLM Pitfalls to Avoid

❌ **Don't:**
- Skip running `make reformat && make typecheck && make test`
- Use broad `except Exception` catches
- Modify code without viewing context first
- Make assumptions about existing code
- Create files without checking if they exist
- Use wrong Python environment

✅ **Do:**
- Always activate virtualenv first
- Run full test suite after changes
- Use specific exception types
- View code before modifying
- Verify changes with tests
- Keep changes minimal and surgical
- Check file existence before creating
- Use `str_replace` for existing files, not `create`

### Testing Guidelines for LLMs

**Always test your changes:**

```bash
# Quick verification
make test

# Detailed test output
pytest src/fido_mds/tests/ -v

# Test specific functionality
pytest src/fido_mds/tests/test_verify.py::test_verify -k android

# Test with different verbosity
pytest src/fido_mds/tests/ -vv -s
```

**Verify test data changes:**
```python
# Test that new data can be parsed
from fido_mds.tests.data import PIXEL_8A
from fido_mds.models.webauthn import Attestation

att = Attestation.from_base64(PIXEL_8A[0])
print(f"Format: {att.fmt}")
print(f"Algorithm: {att.att_statement.alg}")
```

### Type Checking for LLMs

**Common type issues and fixes:**

```python
# Issue: Optional not handled
def process(data: AuthenticatorData) -> bytes:
    return data.credential_data.public_key  # Error if credential_data is None

# Fix: Check for None
def process(data: AuthenticatorData) -> bytes:
    if not data.credential_data:
        raise InvalidData("Missing credential data")
    return data.credential_data.public_key

# Issue: Union type not narrowed
ext.value.value  # Error: ExtensionType has no attribute 'value'

# Fix: Use isinstance check
if isinstance(ext.value, UnrecognizedExtension):
    ext_value = ext.value.value
else:
    raise InvalidData("Unexpected extension type")
```

### Documentation for LLMs

**When documenting code:**

```python
def method(param: bytes, other: str) -> None:
    """
    One-line summary.
    
    Detailed description if needed. Can span multiple lines
    and explain the purpose, algorithm, or important details.
    
    Args:
        param: Description of param
        other: Description of other
        
    Returns:
        Description of return value
        
    Raises:
        InvalidData: When validation fails
        ValueError: When input is malformed
    """
```

### Integration with Existing Code

**Follow existing patterns:**

```python
# Existing pattern in TpmAttestation:
try:
    pub_key.verify(data, signature)
except _InvalidSignature:
    raise InvalidSignature("Verification failed")

# Your code should follow same pattern:
try:
    cose_key.verify(att_to_be_signed, sig)
except _InvalidSignature:
    logger.exception("Failed to verify attestation signature")
    raise InvalidSignature("Signature verification failed")
```

### Debugging Tips for LLMs

**Check imports:**
```bash
# Verify imports work
python -c "from fido_mds.models.attestation import AndroidKeyAttestation; print('OK')"
```

**Test specific functionality:**
```bash
# Quick validation of changes
PYTHONPATH=src python -c "
from fido_mds.tests.data import PIXEL_8A
from fido_mds.models.webauthn import Attestation
att = Attestation.from_base64(PIXEL_8A[0])
print(f'✓ Parsed: {att.fmt}')
"
```

**Check test output:**
```bash
# Detailed test output
pytest src/fido_mds/tests/test_verify.py -vv --tb=short
```

### Quality Checklist for LLMs

Before completing work, verify:

- [ ] Virtualenv activated: `/home/lundberg/python-environments/python-fido-mds/`
- [ ] `make reformat` passes
- [ ] `make typecheck` passes with 0 errors
- [ ] `make test` passes with all tests passing
- [ ] No broad exception catches (avoid `except Exception`)
- [ ] Type hints added to all functions
- [ ] Docstrings added to public methods
- [ ] Code follows existing patterns
- [ ] Changes are minimal and surgical
- [ ] Test data is valid and documented

### Example LLM Session

```bash
# 1. Start with correct environment
source /home/lundberg/python-environments/python-fido-mds/bin/activate
cd /home/lundberg/projects/python-fido-mds

# 2. View code to understand context
view src/fido_mds/models/attestation.py

# 3. Make changes
str_replace path="src/fido_mds/models/attestation.py" \
  old_str="..." \
  new_str="..."

# 4. Run quality checks
make reformat
make typecheck
make test

# 5. Verify specific functionality
pytest src/fido_mds/tests/test_verify.py::test_verify -v

# 6. Done! All checks pass ✅
```

### Summary for LLMs

**Golden Rules:**
1. Always use virtualenv: `/home/lundberg/python-environments/python-fido-mds/`
2. Always run: `make reformat && make typecheck && make test`
3. View before modifying
4. Keep changes minimal
5. Follow existing patterns
6. Use specific exceptions
7. Add type hints
8. Test thoroughly

---

## Additional Resources

- [FIDO Metadata Service](https://fidoalliance.org/metadata/)
- [WebAuthn Specification](https://www.w3.org/TR/webauthn-2/)
- [Android Key Attestation](https://source.android.com/docs/security/features/keystore/attestation)
- [python-fido2 Library](https://github.com/Yubico/python-fido2)

## License

See LICENSE file in the repository root.
