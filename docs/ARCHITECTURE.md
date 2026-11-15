# credit_application_model architecture

## Source map

This diagram maps source folders/files actually present in the reviewed commit. It describes code organisation, not a verified live network topology.

```mermaid
flowchart TD
  R["credit_application_model"]
  N0["Release and reference files"]
  R --> N0
```

## Entry points

No runnable entry point was established in the reviewed source.

## Integration and deployment context

For internal users, the wider system context is maintained in the Ostrich system-blueprints engineering hub. Public demo/installer repositories expose their own source/release context only.

Runtime calls, trust boundaries, exposed URLs, identity controls, data storage and residency must be checked against the chosen release's actual code and environment configuration before drawing security conclusions. Repository/source dependencies do not establish an enabled integration.

## Reviewed source

- [requirements.txt](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/requirements.txt)
- [README.md](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/README.md)
- [inference.py](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/inference.py)
- [entrypoint.sh](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/entrypoint.sh)
- [parameters.json](https://github.com/Ostrich-AI/credit_application_model/blob/30d66553c134175e4763f11df127b2b626b2f81d/parameters.json)

Review date: 2026-11-15. Missing topology/configuration evidence is requested through the central agency handover draft rather than separate forms.
