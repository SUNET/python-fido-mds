# Requirements of the release job

`publish-to-pypi.yml` installs these with `--require-hashes --only-binary :all:`, so the versions and the files
are fixed and no setup script runs.

- `requirements-bootstrap.in` / `.txt`: `uv`, installed with pip.
- `requirements-release.in` / `.txt`: what the job needs to update the metadata (`scripts/requirements.txt`), to
  run the tests (the package's dependencies and `pytest`) and to build.
- `requirements-audit.in` / `.txt`: `pip-audit`, used by `audit.yml`.

The `.in` files are the inputs and the `.txt` files are generated. To update the locked versions (and to pick up
new releases of the dependencies), run from this directory:

```
for name in bootstrap release audit; do
  uv pip compile --universal --generate-hashes --python-version 3.10 requirements-$name.in -o requirements-$name.txt
done
```

Keep `requirements-release.in` in step with the dependencies in `pyproject.toml` and `scripts/requirements.txt`.

`audit.yml` checks every Monday, and whenever these files change, that the locked versions have no known
vulnerabilities, and that they install on Python 3.10 and on the latest 3.x. Dependabot (`.github/dependabot.yml`)
proposes updates of the locked versions and of the GitHub Actions.
