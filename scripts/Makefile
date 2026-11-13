CERT_URL=http://secure.globalsign.com/cacert/root-r3.crt
MDS_URL=https://mds.fidoalliance.org

# -f: an HTTP error (the FIDO service rate limits with 429) fails instead of being saved as the downloaded file
# --retry: retry transient errors (timeouts, 429, 5xx)
CURL=$(shell which curl) -sSfL --retry 5 --retry-delay 30
UV=$(shell which uv)

globalsign_root_r3.der:
	$(CURL) -o globalsign_root_r3.der $(CERT_URL)

fido_alliance_mds.jwt:
	$(CURL) -o fido_alliance_mds.jwt ${MDS_URL}

metadata.json: globalsign_root_r3.der fido_alliance_mds.jwt
	$(UV) run update_metadata.py > metadata.json

apple_webauthn_root_ca.pem:
	$(CURL) -o apple_webauthn_root_ca.pem https://www.apple.com/certificateauthority/Apple_WebAuthn_Root_CA.pem

google_hardware_attestation_root_ca.json:
	$(CURL) -o google_hardware_attestation_root_ca.json https://android.googleapis.com/attestation/root

iana_cose_algs.csv:
	$(CURL) -o iana_cose_algs.csv https://www.iana.org/assignments/cose/algorithms.csv

cose_algs: iana_cose_algs.csv
	$(UV) run python3 -c "from csv import DictReader; print({item.get('Value'): item.get('Name') for item in DictReader(open('./iana_cose_algs.csv'))})"

update_package_data: metadata.json apple_webauthn_root_ca.pem google_hardware_attestation_root_ca.json
	cp metadata.json apple_webauthn_root_ca.pem google_hardware_attestation_root_ca.json ../src/fido_mds/data/

clean:
	rm -f metadata.json globalsign_root_r3.der fido_alliance_mds.jwt iana_cose_algs.csv google_hardware_attestation_root_ca.json apple_webauthn_root_ca.pem

all: metadata.json apple_webauthn_root_ca.pem google_hardware_attestation_root_ca.json

# do not leave a half written or empty file behind when a download or the metadata update fails
.DELETE_ON_ERROR:

.DEFAULT_GOAL:= all
.PHONY: all
