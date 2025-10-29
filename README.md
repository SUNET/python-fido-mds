# python-fido-mds

FIDO Alliance Metadata Service (MDS) in a Python package with WebAuthn attestation verification.

[![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

This package provides:

- **FIDO Metadata Service (MDS)** - Bundled and regularly updated FIDO Alliance authenticator metadata
- **Attestation Verification** - Comprehensive WebAuthn attestation format support
- **Type Safety** - Full Pydantic models for type-safe metadata and attestation handling
- **Production Ready** - Used in production environments for WebAuthn authentication

## Features

### Attestation Format Support

- ✅ **Android Key** - Full KeyMint 4.0 support with origin and purpose validation
- ✅ **Packed** - Standard packed attestation format
- ✅ **TPM** - Trusted Platform Module attestation
- ✅ **Android SafetyNet** - Legacy Android attestation (via fido2 library)
- ✅ **Apple Anonymous** - Apple device attestation
- ✅ **FIDO U2F** - Universal 2nd Factor attestation
- ✅ **None** - Self attestation

### Validation Features

For **Android Key** attestation, validates:
- Signature over authenticatorData and clientDataHash
- Public key matching between certificate and credential
- Attestation challenge matches client data hash
- Authorization list compliance (no allApplications field)
- Origin field presence (KM_ORIGIN_GENERATED)
- Purpose field presence (KM_PURPOSE_SIGN)

### FIDO Metadata Service

- Regularly updated authenticator metadata from FIDO Alliance
- Certificate chain verification
- Metadata statement validation
- Support for status reports

## Installation

```bash
pip install fido-mds
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/SUNET/python-fido-mds.git
cd python-fido-mds

# Create and activate virtual environment
python3 -m venv /path/to/virtualenv
source /path/to/virtualenv/bin/activate

# Install development dependencies
pip install -r test_requirements.txt
```

## Quick Start

### Basic Attestation Verification

```python
from fido_mds import FidoMetadataStore
from fido_mds.models.webauthn import Attestation

# Initialize metadata store
mds = FidoMetadataStore()

# Parse attestation object and client data
attestation = Attestation.from_base64(attestation_object_b64)
client_data = decode_client_data(client_data_b64)

# Verify attestation
try:
    result = mds.verify_attestation(attestation, client_data)
    print(f"✅ Attestation verified: {result.attestation_type}")
except Exception as e:
    print(f"❌ Verification failed: {e}")
```

### Android Key Attestation

```python
from fido_mds.models.attestation import AndroidKeyAttestation
import hashlib

# Create verifier
verifier = AndroidKeyAttestation()

# Prepare data
client_data_hash = hashlib.sha256(client_data).digest()

# Verify
result = verifier.verify(
    statement=attestation.attestation_obj.att_stmt,
    auth_data=attestation.attestation_obj.auth_data,
    client_data_hash=client_data_hash
)
```

## Documentation

- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Comprehensive development guide including:
  - Setup and installation
  - Development workflow
  - Testing guidelines
  - Code quality standards
  - Architecture overview
  - **Special LLM section** for AI-assisted development

## Architecture

```
fido-mds/
├── models/
│   ├── attestation.py    # Attestation format implementations
│   ├── fido_mds.py       # FIDO MDS models
│   └── webauthn.py       # WebAuthn models
├── data/                 # Bundled metadata
├── tests/                # Test suite
│   ├── data.py          # Test attestation objects
│   └── test_*.py        # Test modules
├── helpers.py           # Utility functions
└── metadata_store.py    # Main API
```

### Key Components

- **FidoMetadataStore** - Main entry point for attestation verification
- **AndroidKeyAttestation** - Android Key attestation format implementation
- **Attestation Models** - Pydantic models for type-safe data handling
- **Metadata Service** - FIDO Alliance metadata management

## Requirements

- Python 3.8 or higher (tested with 3.13.3)
- fido2 >= 2.0.0
- pydantic >= 2.0
- cryptography
- pyOpenSSL
- asn1crypto (for Android Key attestation)

## Development

### Running Tests

```bash
# Activate virtualenv
source /path/to/virtualenv/bin/activate

# Run all tests
make test

# Run specific test
pytest src/fido_mds/tests/test_verify.py -v
```

### Code Quality

```bash
# Format code
make reformat

# Type checking
make typecheck

# Run all checks
make reformat && make typecheck && make test
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed development guidelines.

## WebAuthn Specification Compliance

This package implements attestation verification according to:

- [WebAuthn Level 2 Specification](https://www.w3.org/TR/webauthn-2/)
- [Android Key Attestation](https://source.android.com/docs/security/features/keystore/attestation)
- [FIDO Metadata Service](https://fidoalliance.org/metadata/)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Run all quality checks (`make reformat && make typecheck && make test`)
5. Submit a pull request

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed contribution guidelines.

## Testing

The test suite includes real attestation objects from various authenticators:

- YubiKey 4/5 (FIDO U2F and Packed formats)
- Apple devices (iPhone, MacBook)
- Android devices (Google Pixel 8a with Android Key)
- TPM attestation

All test data is sourced from actual WebAuthn registrations to ensure real-world compatibility.

## License

BSD 3-Clause License. See [LICENSE](LICENSE) file for details.

## Credits

- **Author**: Johan Lundberg (lundberg@sunet.se)
- **Organization**: SUNET (Swedish University Computer Network)
- **Repository**: https://github.com/SUNET/python-fido-mds

## References

- [WebAuthn Specification](https://www.w3.org/TR/webauthn-2/)
- [FIDO Alliance Metadata Service](https://fidoalliance.org/metadata/)
- [Android KeyStore Attestation](https://source.android.com/docs/security/features/keystore/attestation)
- [python-fido2 Library](https://github.com/Yubico/python-fido2)
- [duo-labs/py_webauthn](https://github.com/duo-labs/py_webauthn)

## Changelog

### Recent Updates

#### Android Key Attestation Enhancement
- ✅ Complete Android Key attestation implementation
- ✅ Origin field validation (tag 702)
- ✅ Purpose field validation (tag 1)
- ✅ KeyDescription ASN.1 parsing
- ✅ Authorization list validation
- ✅ Full WebAuthn spec compliance

#### Documentation
- ✅ Comprehensive DEVELOPMENT.md with LLM guidelines
- ✅ Updated README with usage examples
- ✅ Architecture documentation

## Support

For issues, questions, or contributions:
- **Issues**: https://github.com/SUNET/python-fido-mds/issues
- **Email**: lundberg@sunet.se

---

**Note**: This package bundles FIDO Alliance metadata. Please ensure you comply with the FIDO Alliance Metadata Service Terms of Use.