from __future__ import annotations

import argparse
import os
import sys
import warnings
from pathlib import Path

import joblib
import pandas as pd

warnings.filterwarnings("ignore")


def _install_numpy_core_shim() -> None:
    """
    Compatibility shim for models pickled with NumPy versions that reference
    internal modules under `numpy._core.*`.
    """
    try:
        import numpy.core as np_core  # type: ignore
    except Exception:
        return

    sys.modules.setdefault("numpy._core", np_core)

    for sub in (
        "multiarray",
        "numeric",
        "_multiarray_umath",
        "umath",
        "overrides",
        "_dtype",
        "_ufunc_config",
        "_exceptions",
        "_internal",
    ):
        try:
            mod = __import__(f"numpy.core.{sub}", fromlist=["*"])
        except Exception:
            continue
        sys.modules.setdefault(f"numpy._core.{sub}", mod)


def _resolve_output_csv_path(output: str) -> Path:
    """
    If `output` looks like a directory (no file suffix, or ends with '/'),
    write `output.csv` inside it. Otherwise treat it as a file path.
    """
    p = Path(output)
    if output.endswith(os.sep) or p.suffix == "":
        return p / "output.csv"
    return p


def _load_payload(model_path: str):
    try:
        return joblib.load(model_path)
    except ModuleNotFoundError as e:
        # Example failure: ModuleNotFoundError: No module named 'numpy._core'
        if getattr(e, "name", "") == "numpy._core" or "numpy._core" in str(e):
            _install_numpy_core_shim()
            return joblib.load(model_path)
        raise


def run_inference(input_csv: str, model_path: str, output: str) -> Path:
    payload = _load_payload(model_path)

    if isinstance(payload, dict) and "pipeline" in payload:
        pipeline = payload["pipeline"]
        label_inverse_map = payload.get("label_inverse_map")
        label_map_applied = bool(payload.get("label_map_applied", False))
    else:
        pipeline = payload
        label_inverse_map = None
        label_map_applied = False

    df_x = pd.read_csv(input_csv)
    empty_cols = []
    for col in df_x.columns:
        series = df_x[col]
        if series.dtype == "object":
            series = series.replace(r"^\s*$", pd.NA, regex=True)
        if series.isna().all():
            empty_cols.append(col)

    if empty_cols:
        df_x = df_x.drop(columns=empty_cols)
        print(f"INFO: ignored fully empty columns: {empty_cols}")

    preds = pipeline.predict(df_x)

    if label_map_applied and isinstance(label_inverse_map, dict):
        preds = pd.Series(preds).map(label_inverse_map).to_numpy()

    out_df = pd.DataFrame({"Class": preds})

    output_csv = _resolve_output_csv_path(output)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_csv, index=False)
    print(f"SUCCESS: created {output_csv}")
    return output_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="dataset/input.csv",
        help="Path to input features CSV (default: dataset/input.csv)",
    )
    parser.add_argument(
        "--model", default="model/model.pkl", help="Path to trained model.pkl"
    )
    parser.add_argument(
        "--output",
        default="output/output.csv",
        help="Output directory (recommended) or output CSV path",
    )
    args = parser.parse_args()

    run_inference(input_csv=args.input, model_path=args.model, output=args.output)


if __name__ == "__main__":
    main()
