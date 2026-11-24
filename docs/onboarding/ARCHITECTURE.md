# Component architecture

```mermaid
flowchart TD
  I[Synthetic input] --> A[Inference script]
  P[Parameters] --> A
  M[Model asset] --> A
  A --> O[Prediction output]
```

Conceptual source-oriented view, not a verified deployment diagram. Consult the README code map and configuration catalogue for concrete entrypoints. Provider connections depend on the selected feature and environment.
