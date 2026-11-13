# Requirements of the release job

`publish-to-pypi.yml` and `run-tests.yaml` install these with `--require-hashes --only-binary :all:`, so the versions and the files
are fixed and no setup script runs.

- `requirements-bootstrap.in` / `.txt`: `uv`, installed with pip.
- `requirements-release.in` / `.txt`: what the job needs to update the metadata (`scripts/requirements.txt`), to
  run the tests (the package's dependencies and `pytest`) and to build.
- `requirements-test.in` / `.txt`: what the test and type check jobs of `run-tests.yaml` need (the release
  requirements and `mypy`).
- `requirements-audit.in` / `.txt`: `pip-audit`, used by `audit.yml`.

The `.in` files are the inputs and the `.txt` files are generated. Run from this directory:

```
for name in bootstrap release test audit; do
  uv pip compile --universal --generate-hashes --python-version 3.10 requirements-$name.in -o requirements-$name.txt
done
```

This keeps the versions already in the `.txt` files and only adds what changed in the `.in` files. To pick up new
releases of the dependencies (for example to fix a vulnerability that `audit.yml` reports), add `--upgrade` to
the command, or `--upgrade-package <name>` to upgrade a single package.

Keep `requirements-release.in` in step with the dependencies in `pyproject.toml` and `scripts/requirements.txt`.

`audit.yml` checks every Monday, and whenever these files change, that the locked versions have no known
vulnerabilities, and that they install, on Python 3.10 and on the latest 3.x (each is audited separately, because
some locked versions are only used on 3.10). Dependabot (`.github/dependabot.yml`)
proposes updates of the locked versions and of the GitHub Actions.

The requirements of `pip-audit` itself (`requirements-audit.txt`) are audited on the latest 3.x only. For Python 3.10
the newest `filelock` is 4.1.0, which has known vulnerabilities that are fixed only in versions that need Python 3.11
(Python 3.10 is end of life), so that check could never pass there.
