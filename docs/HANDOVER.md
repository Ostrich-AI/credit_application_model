# credit_application_model handover guide

## Purpose and source

Public demonstration credit-application model and inference assets.

Reviewed source ref: `30d66553c134175e4763f11df127b2b626b2f81d`; default branch: `main`. No staging image-to-source mapping was established for this repository.

## Prerequisites and setup

Python version from pyproject.toml or the Dockerfile; isolated virtual environment; approved synthetic configuration.

```bash
python -m venv .venv
# Activate the virtual environment for your operating system.
python -m pip install -r requirements.txt
```


## Configuration

Use the source settings/Helm configuration and existing guides below. A complete environment-variable contract has not been independently established.

## Tests and verification

Test dependencies or files in source are not evidence of a passing run. See source test folders/workflows for declared commands.

Run appropriate tests in an isolated environment with approved configuration and keep the run URL, source ref and results. Some declared lint/test scripts modify files or clean caches; inspect before executing.

## Deployment and rollback

Review Dockerfiles, workflows and the owner-confirmed GitOps/IaC source. Record image digest, environment, migration revision, smoke checks and rollback limitation. Deployment credentials, cloud state and data restoration are outside a Git-only source checkout. Do not run reset/drop/re-index actions against live systems from a copied example.

## Recovery and continuity

Before handover acceptance, verify source/dependency availability, company administration, secret custody, data/config backups and a tested restore. A new engineer must demonstrate setup and a representative journey without undocumented vendor assistance. Record unresolved steps with named owner/date.

## Exact questions to close

1. Is the source/ref above the correct supported version? If different, provide its repository and commit.
2. Which configured image is running now? Provide the image digest and environment.
3. Which documented setup/rollback/restore step has been demonstrated most recently? Link the existing evidence.
4. Which dependencies or accounts remain under vendor control?

## Existing evidence

- [README.md](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/README.md)
