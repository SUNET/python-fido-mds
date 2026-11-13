# -*- coding: utf-8 -*-
from copy import deepcopy
from typing import Any, Dict

from fido_mds.models.fido_mds import MetadataEntry

__author__ = "ylle"

# The shape of a password manager in the FIDO Metadata Service: a software authenticator without
# userVerificationDetails and attachmentHint (Dashlane's entry, shortened).
SOFTWARE_AUTHENTICATOR: Dict[str, Any] = {
    "aaguid": "531126d6-e717-415c-9320-3d9aa6981239",
    "statusReports": [{"status": "NOT_FIDO_CERTIFIED", "effectiveDate": "2026-09-30"}],
    "timeOfLastStatusChange": "2026-09-30",
    "metadataStatement": {
        "legalHeader": "https://fidoalliance.org/metadata/metadata-statement-legal-header/",
        "aaguid": "531126d6-e717-415c-9320-3d9aa6981239",
        "description": "Dashlane Password Manager",
        "authenticatorVersion": 1,
        "protocolFamily": "fido2",
        "schema": 3,
        "upv": [],
        "authenticationAlgorithms": ["secp256r1_ecdsa_sha256_raw"],
        "publicKeyAlgAndEncodings": ["ecc_x962_raw"],
        "attestationTypes": ["none"],
        "keyProtection": ["software"],
        "matcherProtection": ["software"],
        "tcDisplay": [],
        "attestationRootCertificates": [],
    },
}


def test_software_authenticator_without_user_verification_details_and_attachment_hint():
    entry = MetadataEntry.model_validate(SOFTWARE_AUTHENTICATOR)

    statement = entry.metadata_statement
    assert statement.description == "Dashlane Password Manager"
    assert statement.key_protection == ["software"]
    assert statement.user_verification_details == []
    assert statement.get_user_verification_details() == []
    assert statement.attachment_hint == []


def test_attachment_hint_and_user_verification_details_are_kept_when_present():
    data = deepcopy(SOFTWARE_AUTHENTICATOR)
    data["metadataStatement"]["attachmentHint"] = ["internal"]
    data["metadataStatement"]["userVerificationDetails"] = [[{"userVerificationMethod": "passcode_internal"}]]

    statement = MetadataEntry.model_validate(data).metadata_statement

    assert statement.attachment_hint == ["internal"]
    assert [uvd.user_verification_method for uvd in statement.get_user_verification_details()] == ["passcode_internal"]
